import os
import pandas as pd
import natsort as ns

df = pd.read_csv(r'C:\Temp\Partitions_Layout.csv', sep=',', engine='python', header=None, skiprows=1)
df = pd.Series.str.split(pat='/', n=-1, expand=False)
#df[1] = pd.Categorical(df[1], ordered=True, categories= ns.natsorted(df[1].unique()))
#df = df.sort_values(1)
df.to_csv(r'C:\Temp\sorting_test.csv', index=True)
