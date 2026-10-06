import pandas as pd

file_path = "data/workflows.xlsx"

excel = pd.ExcelFile(file_path)

for sheet in excel.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    print("\n" + "#" * 70)
    print(f"SHEET: {sheet}  |  rows: {len(df)}")
    print("COLUMNS:", df.columns.tolist())

    for i, row in df.iterrows():
        print("\n" + "=" * 70)
        print(f"Row {i + 1}")
        for col in df.columns:
            print(f"\n{col}:\n{row[col]}")