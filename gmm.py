import warnings 
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import silhouette_score
# from google.colab import drive
# drive.mount('drive')
pd.set_option('display.max_columns',50)
#read data and get columns
df = pd.read_csv(r'DataStorage\\clustering_stats.csv')
df.head()

#getting the columns for the model 
columns_df = df.iloc[:, 1:]
columns_df = columns_df.fillna(0)
features = list(columns_df.columns.values)
print(features)

# df = pd.read_csv(r'DataStorage\\fighter_details_links.csv')
# col_df = df.iloc[:, 1:]
# col_df = col_df.fillna(0)
# features = list(col_df.columns.values)

#z-score the data (not needed)
#X = df[features]
#z = StandardScaler()
#X[features] = z.fit_transform(X)

#Concluded on five clusters: fit the model and estimate paramaters
X = df[features]
GM = GaussianMixture(max_iter=100,n_components = 5,n_init=3)
GM.fit(columns_df)
print(GM.weights_)

#silhoutte score
# print ("SILHOUTTE: ", silhouette_score(X, cluster))

cluster = GM.predict(X)
cluster_p = GM.predict_proba(X)
#iterate to create rows and columns to append
rows = []
cluster_vector = np.round(cluster_p.tolist(), 3)
for i in range (0,len(cluster)):
    row = cluster_vector[i].copy()
    row.insert(0,fighters_list[i])
    rows.append(row)
cols = ['Name','p(cluster_1)','p(cluster_2)','p(cluster_3)','p(cluster_4)','p(cluster_5)']

#add to csv file
table = pd.DataFrame(rows, columns=cols)
table.to_csv(r'gmm.csv', index=False)  
# !cp gmm.csv "drive/My Drive/"