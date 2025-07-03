import os
import pandas as pd
import requests

FEDEX_OAUTH_URL = "https://apis.fedex.com/oauth/token"
FEDEX_TRACK_URL = "https://apis.fedex.com/track/v1/trackingnumbers"


class FedExAPIError(Exception):
    pass


def _get_oauth_token():
    """Fetch OAuth token using client credentials."""
    client_id = os.getenv("FEDEX_CLIENT_ID")
    client_secret = os.getenv("FEDEX_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise FedExAPIError("FedEx API credentials not configured")

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    resp = requests.post(FEDEX_OAUTH_URL, data=data, timeout=10)
    if resp.status_code != 200:
        raise FedExAPIError(f"OAuth request failed: {resp.status_code} {resp.text}")
    return resp.json().get("access_token")


def fetch_tracking_statuses(tracking_numbers):
    """Return a list of dicts with tracking_number and status keys."""
    if not tracking_numbers:
        return []

    token = _get_oauth_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    statuses = []
    for start in range(0, len(tracking_numbers), 30):
        batch = tracking_numbers[start : start + 30]
        body = {
            "trackingInfo": [
                {"trackingNumberInfo": {"trackingNumber": num}}
                for num in batch
            ]
        }
        resp = requests.post(
            FEDEX_TRACK_URL, json=body, headers=headers, timeout=10
        )
        if resp.status_code != 200:
            raise FedExAPIError(
                f"Track request failed: {resp.status_code} {resp.text}"
            )

        data = resp.json()
        results = data.get("output", {}).get("completeTrackResults", [])
        for item in results:
            track_data = item.get("trackResults", [{}])[0]
            num = track_data.get("trackingNumber")
            status = (
                track_data.get("latestStatusDetail", {}).get("statusByLocale", "Unknown")
            )
            statuses.append({"tracking_number": num, "status": status})

    return statuses


def process_tracking_csv(uploaded_file):
    """Parse uploaded CSV and return message and rows with tracking/status."""
    if not uploaded_file or not uploaded_file.filename:
        return "No file uploaded", None
    try:
        df = pd.read_csv(uploaded_file)
        track_col = next(
            (c for c in df.columns if c.strip().lower() == "tracking number"),
            None,
        )
        if track_col is None:
            return "Column 'Tracking Number' not found", None

        tracking_numbers = df[track_col].astype(str).tolist()
        statuses = fetch_tracking_statuses(tracking_numbers)
        rows = [
            {"Tracking Number": s["tracking_number"], "Status": s["status"]}
            for s in statuses
        ]

        return f"Processed {uploaded_file.filename}", rows
    except FedExAPIError as exc:
        return str(exc), None
    except Exception as exc:
        return f"Error processing file: {exc}", None


def process_single_tracking_number(tracking_number):
    """Return status for a single tracking number."""
    if not tracking_number:
        return "Tracking number required", None
    try:
        statuses = fetch_tracking_statuses([tracking_number])
        return "Success", statuses[0] if statuses else None
    except FedExAPIError as exc:
        return str(exc), None
    except Exception as exc:
        return f"Error fetching status: {exc}", None
