import pandas as pd

pd.set_option('display.max_columns', None)


df = pd.read_csv('../data/processed.csv')

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print(df)
