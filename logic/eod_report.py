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