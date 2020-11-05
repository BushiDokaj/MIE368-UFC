import pandas as pd
import numpy as np

def calculate_seconds(minsec):
  if isinstance(minsec, float):
    return np.nan 
  else:
    m, s = minsec.split(':')
    return int(m) * 60 + int(s)
  
def split_column_first(string_to_split):
  first, second = string_to_split.split(' of ')
  return first

def split_column_second(string_to_split):
  first, second = string_to_split.split(' of ')
  return second

df_raw = pd.read_csv(r'DataStorage\\fight_stats.csv')
df = df_raw.drop('Unnamed: 0',axis=1)

#Replace values
mapping_dict = {"L": 0, "W": 1, '---': np.nan, '--': np.nan, "25:00:00": "25:00", "24:56:00": "24:56", "24:59:00": "24:59", "24:10:00": "24:10"}
df.replace(mapping_dict, inplace=True)
df = df.drop(df[df.M_RES == "D"].index)
df = df.drop(df[df.M_RES == "NC"].index)
df = df.drop(df[df.OP_RES == "D"].index)
df = df.drop(df[df.OP_RES == "NC"].index)

# Convert time into integer seconds
df['TIME'] = df['TIME'].apply(calculate_seconds)
df['M_CTRL'] = df['M_CTRL'].apply(calculate_seconds)
df['OP_CTRL'] = df['OP_CTRL'].apply(calculate_seconds)

# Split 'X of Y' columns into separate 'X' and 'Y' columns
columns_to_split = ['M_SIG_STR', 'M_TOTAL_STR', 'M_TD', 'M_HEAD', 'M_BODY', 'M_LEG', 'M_DIST', 'M_CLIN', 'M_GROUND', 'OP_SIG_STR', 'OP_TOTAL_STR' ,'OP_TD', 'OP_HEAD', 'OP_BODY', 'OP_LEG', 'OP_DIST', 'OP_CLIN', 'OP_GROUND']

for i in columns_to_split:
  first_column = df[i].apply(split_column_first)
  df[i] = pd.to_numeric(first_column)

df.to_csv(r'DataStorage\\cleaned_fight_stats.csv')
