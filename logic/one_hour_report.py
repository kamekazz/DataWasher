import json
import pandas as pd


def process_one_hour_report_file(uploaded_file):
    """Process uploaded CSV file for the 1-hour report using the new structure.

    Returns a tuple of
        (message,
         ready_to_assign,
         assign_count,
         transaction_table,
         chart_labels,
         chart_values,
         child_percentage)
    """
    if not uploaded_file or not uploaded_file.filename:
        return None, None, None, None, None, None, None

    try:
        df = pd.read_csv(uploaded_file)

        # Identify status and transaction columns
        status_col = next((c for c in df.columns if c.lower() == 'status'), None)
        transaction_col = next((c for c in df.columns if c.lower() == 'transaction'), None)

        if status_col is None or transaction_col is None:
            return 'Required columns not found', None, None, None, None, None, None

        # Counts for specific status values
        status_counts = df[status_col].value_counts()
        ready_to_assign = int(status_counts.get('Ready For Assignment', 0))
        assign_count = int(status_counts.get('Assigned', 0))

        # Counts per transaction
        transactions = df[transaction_col].value_counts()
        transaction_table = [
            {'transaction': t, 'count': int(c)} for t, c in transactions.items()
        ]

        chart_labels = json.dumps(transactions.index.tolist())
        chart_values = json.dumps([int(v) for v in transactions.values])



        message = f"Processed {uploaded_file.filename}"
        return (message,
                ready_to_assign,
                assign_count,
                transaction_table,
                chart_labels,
                chart_values,
                )
    except Exception as exc:
        return f"Error processing file: {exc}", None, None, None, None, None, None
