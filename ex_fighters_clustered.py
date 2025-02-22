import pandas as pd
import numpy as np

df_raw = pd.read_csv(r'expanded_data\\cleaned_fight_stats.csv')
df_labels = pd.read_csv(r'expanded_data\\fighter_clusters.csv')
df_clustered = df_raw.copy()
df_clustered['Cluster #'] = np.nan
for index, row in df_labels.iterrows():
    
    df_clustered.loc[df_clustered.M_NAME == row['M_NAME'], 'Cluster #'] = row['Cluster']

df_clustered.to_csv(r'expanded_data\\ex_fighters_clustered.csv')

df_c0 = df_clustered.loc[df_clustered['Cluster #'] == 0]
df_c1 = df_clustered.loc[df_clustered['Cluster #'] == 1]
df_c2 = df_clustered.loc[df_clustered['Cluster #'] == 2]
df_c3 = df_clustered.loc[df_clustered['Cluster #'] == 3]
df_c4 = df_clustered.loc[df_clustered['Cluster #'] == 4]

df_c0.to_csv(r'expanded_data\\clusters\\cluster_0.csv', index=False)
df_c1.to_csv(r'expanded_data\\\clusters\\cluster_1.csv', index=False)
df_c2.to_csv(r'expanded_data\\clusters\\cluster_2.csv', index=False)
df_c3.to_csv(r'expanded_data\\clusters\\cluster_3.csv', index=False)
df_c4.to_csv(r'expanded_data\\clusters\\cluster_4.csv', index=False)
