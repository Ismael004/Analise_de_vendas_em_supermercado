import pandas as pd
import plotly.express as px

file_csv = "SuperMarket_Analysis.csv"

def read_file_csv(csv):
    df = pd.read_csv(csv)
    return df

def counts_data(df):
    counts_data = df[df['City'].value_counts()]
    return counts_data

df1 = counts_data(read_file_csv(file_csv))

print(df1.columns())
#grafico = px.bar(counts_data(read_file_csv(file_csv)), x = 'Name', y = 'count')





