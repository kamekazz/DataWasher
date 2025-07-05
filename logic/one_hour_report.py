import pandas as pd


def count_assigned_tasks(uploaded_file):
    """Process a 1‑Hour Report CSV file.

    Returns a tuple ``(message, assigned_count, ready_for_assignment,
    transaction_summary, assigned_transaction_summary)`` where
    ``transaction_summary`` and ``assigned_transaction_summary`` are lists of
    dictionaries. ``transaction_summary`` uses the ``No. Of task details``
    column to sum tasks for **all** rows. ``assigned_transaction_summary``
    instead counts the number of rows per transaction for those with
    ``Status`` equal to ``Assigned``. The CSV file must include a ``Status``
    column and, for the first summary, both ``Transaction`` and ``No. Of task
    details`` columns (case-insensitive).
    """

    if not uploaded_file or not uploaded_file.filename:
        return None, None, None, None, None

    try:
        df = pd.read_csv(uploaded_file)

        status_col = None
        for column in df.columns:
            normalized = column.lower().replace(" ", "")
            if normalized == "status":
                status_col = column
                break

        if status_col is None:
            return (
                "Required column 'Call Status' not found",
                None,
                None,
                None,
                None,
            )

        assigned_mask = df[status_col].astype(str).str.lower() == "assigned"
        assigned_count = int(assigned_mask.sum())

        ready_mask = (
            df[status_col].astype(str).str.lower() == "ready for assignment"
        )
        ready_for_assignment = int(ready_mask.sum())

        assigned_df = df[assigned_mask].copy()

        trans_col = None
        for column in df.columns:
            if column.lower().replace(" ", "") == "transaction":
                trans_col = column
                break

        task_details_col = None
        for column in df.columns:
            normalized = column.lower().replace(" ", "")
            if normalized in ["no.oftaskdetails", "nooftaskdetails"]:
                task_details_col = column
                break

        transaction_summary = None
        assigned_transaction_summary = None
        if trans_col and task_details_col:
            grouped = df.groupby(trans_col)[task_details_col].sum()
            summary_df = grouped.reset_index()
            summary_df = summary_df.rename(
                columns={trans_col: "transaction", task_details_col: "task_details"}
            )

            summary_df["task_details"] = summary_df["task_details"].astype(int)
            total_tasks = summary_df["task_details"].sum()
            summary_df["percentage"] = (
                summary_df["task_details"] / total_tasks * 100
            ).round(2)

            transaction_summary = summary_df.to_dict(orient="records")
            transaction_summary.append(
                {
                    "transaction": "Total",
                    "task_details": int(total_tasks),
                    "percentage": 100.0,
                }
            )

            assigned_grouped = assigned_df.groupby(trans_col).size()
            assigned_summary_df = assigned_grouped.reset_index(name="count")
            assigned_summary_df = assigned_summary_df.rename(
                columns={trans_col: "transaction"}
            )
            assigned_total = int(assigned_summary_df["count"].sum())
            assigned_summary_df["percentage"] = (
                assigned_summary_df["count"] / assigned_total * 100
            ).round(2)

            assigned_transaction_summary = assigned_summary_df.to_dict(
                orient="records"
            )
            assigned_transaction_summary.append(
                {
                    "transaction": "Total",
                    "count": assigned_total,
                    "percentage": 100.0,
                }
            )

        message = f"Processed {uploaded_file.filename}"
        return (
            message,
            assigned_count,
            ready_for_assignment,
            transaction_summary,
            assigned_transaction_summary,
        )
    except Exception as exc:
        return f"Error processing file: {exc}", None, None, None, None
