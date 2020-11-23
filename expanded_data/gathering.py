import pandas as pd
import string

alpha = list(string.ascii_lowercase)
frames = []
for letter in alpha:
    frames.append(pd.read_csv(r'data_per_letter\\'+letter+"_fight_stats.csv", index_col=0))

master_df = pd.concat(frames)
master_df = master_df.reset_index(drop=True)
master_df.to_csv('all_fights.csv', index=False)
