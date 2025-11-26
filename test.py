import pandas as pd
import requests

def get_journals_for_model():
    response = requests.get("http://127.0.0.1:8000/journals/dataframe")
    data = response.json()
    df = pd.DataFrame(data)
    return df

# Use it in your model
df = get_journals_for_model()
print(df.head(10))
print(f"Shape: {df.shape}")