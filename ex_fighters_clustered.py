import pandas as pd
import numpy as np

r'expanded_data\\clustering_stats.csv'

df_raw = pd.read_csv(r'expanded_data\\clustering_stats.csv')
df_labels = pd.read_csv(r'expanded_data\\fighter_clusters.csv')
df_clustered = df_raw.copy()
df_clustered['Cluster #'] = df_labels['Cluster']

df_clustered.to_csv(r'expanded_data\\ex_fighters_clustered.csv')