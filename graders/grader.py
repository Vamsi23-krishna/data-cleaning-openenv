import pandas as pd 

def compute_score(df, clean_df):
    total = df.size
    comparison = (df == clean_df) | (df.isnull() & clean_df.isnull())
    correct = comparison.sum().sum()
    score = correct / total
    return score 

def compute_detailed_score(df, clean_df):
    scores = {}
    for col in df.columns:
        total = len(df[col])
        comparison = (df[col] == clean_df[col] | (
            df[col].isnull() & clean_df[col].isnull())
        )
        correct = comparison.sum()
        scores[col] = correct / total 
    overall_score = sum(scores.values()) / len(scores)
    return overall_score, scores 