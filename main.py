import pandas as pd


file_csv = "SuperMarket_Analysis.csv"

def read_file_csv(csv):
    df = pd.read_csv(csv)
    return df

def counts_data(df):
    counts_data = df['City'].value_counts()
    print(counts_data)

print(counts_data(read_file_csv(file_csv)))




