import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

df = pd.read_csv('C:\\Users\\bushi\\Desktop\\University\\Year 3\\Courses\\MIE368\\MIE368-UFC\\DataStorage\\clustering_stats.csv')
cl_df = df.iloc[:, 1:]
cl_df = cl_df.fillna(0)

expanded = pd.read_csv(r'clustering_stats.csv')
expanded = pd.concat([expanded, df])
expanded = expanded.drop_duplicates(ignore_index=True)
ex_df = expanded.iloc[:, 1:]
ex_df = ex_df.fillna(0)


mdk_k_means = KMeans(n_init = 50, n_clusters=5, random_state = 2)

# Fit the model to the training set
mdk_k_means.fit(cl_df)

# Get cluster assignments for each data point
clK = mdk_k_means.labels_

# output clusters to files
orig_cl = pd.DataFrame(df['M_NAME'])
orig_cl['Cluster'] = clK

predictions = mdk_k_means.predict(ex_df)
pred_cl = pd.DataFrame(expanded['M_NAME'])
pred_cl['Cluster'] = predictions
fighters_cl = pd.concat([orig_cl, pred_cl])
fighters_cl = fighters_cl.drop_duplicates(ignore_index=True)
print(fighters_cl)

fighters_cl.to_csv(r'fighter_clusters.csv')
