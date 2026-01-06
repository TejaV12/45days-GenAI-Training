import pandas as pd
import os
from datetime import datetime

def generate_report(prompt: str, responses: dict):
    os.makedirs("data/comparsion_reports", exist_ok=True)
    rows=[]
    for model, output in responses.items():
        rows.append({
            "Models":model ,
            "Prompt":prompt ,
            "Responses":output,
            "Timestamp": datetime.now().strftime
            ("%Y-%m-%d %H:%M:%S")
        })
    df=pd.DataFrame(rows)
    df.to_csv("data/comparsion_reports/report.csv",index=False)
    
    return "data/comparsion_reports/report.csv"