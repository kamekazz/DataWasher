import pandas as pd


def count_assigned_tasks(uploaded_file):
    """Process a 1‑Hour Report CSV file.

    Returns a tuple ``(message, assigned_count, ready_for_assignment,
    transaction_summary)`` where ``transaction_summary`` is a list of
    dictionaries with ``transaction`` and ``task_details`` keys.  The
    CSV file must include a ``Status`` column and, for the summary, both
    ``Transaction`` and ``No. Of task details`` columns (case-insensitive).
    """

    if not uploaded_file or not uploaded_file.filename:
        return None, None, None, None

    try:
        df = pd.read_csv(uploaded_file)
        status_col = next(
            (c for c in df.columns if c.lower().replace(" ", "") == "status"),
            None,
        )
        if status_col is None:
            return "Required column 'Call Status' not found", None, None, None

        assigned_count = int((df[status_col].astype(str).str.lower() == "assigned").sum())
        ready_for_assignment = int((df[status_col].astype(str).str.lower() == "ready for assignment").sum())

        trans_col = next(
            (c for c in df.columns if c.lower().replace(" ", "") == "transaction"),
            None,
        )
        task_details_col = next(
            (
                c
                for c in df.columns
                if c.lower().replace(" ", "") in ["no.oftaskdetails", "nooftaskdetails"]
            ),
            None,
        )

        transaction_summary = None
        if trans_col and task_details_col:
            summary_df = (
                df.groupby(trans_col)[task_details_col]
                .sum()
                .reset_index()
                .rename(columns={trans_col: "transaction", task_details_col: "task_details"})
            )
            transaction_summary = summary_df.to_dict(orient="records")

        message = f"Processed {uploaded_file.filename}"
        return message, assigned_count, ready_for_assignment, transaction_summary
    except Exception as exc:
        return f"Error processing file: {exc}", None, None, None
