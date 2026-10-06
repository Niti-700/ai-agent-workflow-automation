import pandas as pd


def read_excel(file_path, sheet_name=0):
    """
    Read an Excel file and return it as a pandas DataFrame.
    """

    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        print(f"Excel loaded successfully: {file_path}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")

        return df

    except Exception as e:
        print(f"Error reading Excel: {e}")
        return None