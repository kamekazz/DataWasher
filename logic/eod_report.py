import pandas as pd

def count_eod_production(uploaded_file):
    """
    Process the uploaded file to count EOD production metrics.

    Args:
        uploaded_file: A file-like object containing the CSV data.

    Returns:
        A tuple containing:
            - message: A status message or error description.
            - units_picked: Total units picked.
            - units_bundled: Total units bundled.
            - units_folded: Total units folded.
    """
    
    if not uploaded_file or not uploaded_file.filename:
        return None, None, None, None

    try:
        df = pd.read_csv(uploaded_file)

        # Check for required columns
        if 'Units Picked' not in df.columns or 'Units Bundled' not in df.columns or 'Units Folded' not in df.columns:
            return "Required columns not found", None, None, None

        units_picked = int(df['Units Picked'].sum())
        units_bundled = int(df['Units Bundled'].sum())
        units_folded = int(df['Units Folded'].sum())

        return "Data processed successfully", units_picked, units_bundled, units_folded

    except Exception as e:
        return f"Error processing file: {str(e)}", None, None, None


def count_total_pick(uploaded_file):
    """Calculate total units picked from a CSV file.

    The CSV must contain ``Transaction ID`` and ``Quantities`` columns. Rows
    with a ``Transaction ID`` containing ``ATML``, ``AMZL``, ``AMXL``, ``TBA`` or
    ``wholesale`` are ignored. The remaining ``Quantities`` values are summed
    and returned as an integer.
    """

    if not uploaded_file or not uploaded_file.filename:
        return None, None

    try:
        df = pd.read_csv(uploaded_file)

        required_cols = {"Transaction ID", "Quantity"}
        if not required_cols.issubset(df.columns):
            return None, "Required columns not found"

        mask = ~df["Transaction ID"].astype(str).str.contains(
            "ATML|AMZL|AMXL|TBA|wholesale|Wholesale|MIXED|LTL|all carriers", case=False, na=False
        )

        total = int(df.loc[mask, "Quantity"].sum())
        return total, f"Processed {uploaded_file.filename}"
    except Exception as exc:
        return None, f"Error processing file: {exc}"
