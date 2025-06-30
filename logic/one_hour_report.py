import pandas as pd


def count_assigned_tasks(uploaded_file):
    """Return a tuple of message and number of assigned tasks.

    The CSV file must contain a column named "Call Status" (case-insensitive).
    """
    if not uploaded_file or not uploaded_file.filename:
        return None, None

    try:
        df = pd.read_csv(uploaded_file)
        status_col = next(
            (c for c in df.columns if c.lower().replace(" ", "") == "status"),
            None,
        )
        if status_col is None:
            return "Required column 'Call Status' not found", None

        assigned_count = int((df[status_col].astype(str).str.lower() == "assigned").sum())
        ready_for_assignment = int((df[status_col].astype(str).str.lower() == "ready for assignment").sum())
        message = f"Processed {uploaded_file.filename}"
        return message, assigned_count , ready_for_assignment
    except Exception as exc:
        return f"Error processing file: {exc}", None
