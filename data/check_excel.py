
import pandas as pd

file_path = "data/workflows.xlsx"

excel = pd.ExcelFile(file_path)

print("Available sheets:", excel.sheet_names)

for sheet in excel.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)
    print(f"\n--- {sheet} ---")
    print(df.head())
    print("Number of rows:", len(df))