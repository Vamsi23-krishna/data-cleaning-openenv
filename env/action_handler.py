import pandas as pd 

def apply_action(df, action):
    if action.action_type == "fill_missing":
        return fill_missing(df, action)
    elif action.action_type == "clean_text":
        return clean_text(df, action)
    elif action.action_type == "normalize_date":
        return normalize_date(df, action)
    elif action.action_type == "convert_salary":
        return convert_salary(df, action)
    elif action.action_type == "remove_duplicates":
        return remove_duplicates(df)
    else:
        raise ValueError("Unknown action")
    

def fill_missing(df, action):
    col = action.column
    if df[col].dtype in ["float64", "int64"]:
        df[col] = df[col].fillna(df[col].mean())
    else:
        df[col] =df[col].fillna("unknown")
    return df 

def clean_text(df, action):
    col = action.column
    df[col] = df[col].astype(str).str.strip().str.lower()
    return df 

def normalize_date(df, action):
    col = action.column
    df[col] = pd.to_datetime(df[col], errors="coerce")
    df[col] = df[col].dt.strftime("%Y-%m-%d")
    return df 

def convert_salary(df, action):
    col = action.column
    df[col] = df[col].astype(str)
    df[col] = df[col].str.replace("$", "", regex=False)
    df[col] = df[col].str.replace("USD", "", regex=False)
    df[col] = df[col].str.strip()
    df[col] = pd.to_numeric(df[col], errors="coerce")

    return df 

def remove_duplicates(df):
    # Consider rows as duplicates based on all columns except 'id'
    if 'id' in df.columns:
        result = df.drop_duplicates(subset=[col for col in df.columns if col != 'id'], keep='first')
    else:
        result = df.drop_duplicates()
    # Reset index to avoid comparison issues
    return result.reset_index(drop=True)

