import pandas as pd

def load_credentials(excel_path):
    df = pd.read_excel(excel_path)

    parent_row = df[df["account_type"] == "parent"].iloc[0]
    parent = {
        "api_key": parent_row["api_key"],
        "api_secret": parent_row["api_secret"],
        "port": 8000
    }

    child_rows = df[df["account_type"] == "child"]
    children = []
    for i, (_, row) in enumerate(child_rows.iterrows(), start=1):
        multiplier = row.get("multiplier", 1)
        multiplier = int(multiplier) if pd.notna(multiplier) else 0
        children.append({
            "api_key": row["api_key"].strip(),
            "api_secret": row["api_secret"].strip(),
            "port": 8000 + i,
            "multiplier": multiplier
        })
    return parent, children
