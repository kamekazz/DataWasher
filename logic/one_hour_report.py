import pandas as pd


def count_assigned_tasks(uploaded_file):
    """Process a 1‑Hour Report CSV file.

    Returns a tuple ``(message, assigned_count, ready_for_assignment,
    transaction_summary, assigned_transaction_summary)`` where both summary
    values are lists of dictionaries with ``transaction``, ``task_details`` and
    ``percentage`` keys. ``transaction_summary`` is calculated using **all**
    rows in the CSV file while ``assigned_transaction_summary`` only includes
    rows where the ``Status`` column is ``Assigned``. The CSV file must include
    a ``Status`` column and, for the summaries, both ``Transaction`` and
    ``No. Of task details`` columns (case-insensitive).
    """

    if not uploaded_file or not uploaded_file.filename:
        return None, None, None, None, None

    try:
        df = pd.read_csv(uploaded_file)
        status_col = next(
            (c for c in df.columns if c.lower().replace(" ", "") == "status"),
            None,
        )
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
        ready_for_assignment = int(
            (
                df[status_col].astype(str).str.lower()
                == "ready for assignment"
            ).sum()
        )
        assigned_df = df[assigned_mask].copy()

        trans_col = next(
            (
                c
                for c in df.columns
                if c.lower().replace(" ", "") == "transaction"
            ),
            None,
        )
        task_details_col = next(
            (
                c
                for c in df.columns
                if c.lower().replace(" ", "")
                in ["no.oftaskdetails", "nooftaskdetails"]
            ),
            None,
        )

        transaction_summary = None
        assigned_transaction_summary = None
        if trans_col and task_details_col:
            summary_df = (
                df.groupby(trans_col)[task_details_col]
                .sum()
                .reset_index()
                .rename(
                    columns={
                        trans_col: "transaction",
                        task_details_col: "task_details",
                    }
                )
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

            assigned_summary_df = (
                assigned_df.groupby(trans_col)[task_details_col]
                .sum()
                .reset_index()
                .rename(
                    columns={
                        trans_col: "transaction",
                        task_details_col: "task_details",
                    }
                )
            )
            assigned_summary_df["task_details"] = assigned_summary_df[
                "task_details"
            ].astype(int)
            assigned_total = assigned_summary_df["task_details"].sum()
            assigned_summary_df["percentage"] = (
                assigned_summary_df["task_details"] / assigned_total * 100
            ).round(2)

            assigned_transaction_summary = assigned_summary_df.to_dict(
                orient="records"
            )
            assigned_transaction_summary.append(
                {
                    "transaction": "Total",
                    "task_details": int(assigned_total),
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
