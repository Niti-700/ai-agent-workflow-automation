import pandas as pd


def read_csv(file_path):
    """
    Read a CSV file and return it as a pandas DataFrame.
    """

    try:
        df = pd.read_csv(file_path)

        print(f"CSV loaded successfully: {file_path}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")

        return df

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None