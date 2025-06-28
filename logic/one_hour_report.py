import json
import pandas as pd


def process_one_hour_report_file(uploaded_file):
    """Process uploaded CSV file for the 1-hour report.

    Returns a tuple of (message, table_data, chart_labels, chart_values).
    """
    if not uploaded_file or not uploaded_file.filename:
        return None, None, None, None

    try:
        df = pd.read_csv(uploaded_file)
        # Try to find a column named city or country
        city_col = next((col for col in df.columns if col.lower() in ['city', 'country']), None)
        if not city_col:
            return 'No city column found', None, None, None

        counts = df[city_col].value_counts()
        total = counts.sum()
        table_data = [
            {
                'city': city,
                'customers': int(count),
                'percent': count / total * 100,
            }
            for city, count in counts.items()
        ]
        chart_labels = json.dumps(list(counts.index))
        chart_values = json.dumps(list(counts.values))
        message = f"Processed {uploaded_file.filename}"
        return message, table_data, chart_labels, chart_values
    except Exception as exc:
        return f"Error processing file: {exc}", None, None, None
