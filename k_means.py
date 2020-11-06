import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv(r'DataStorage\\clustering_stats.csv')
cl_df = df.iloc[:, 1:]
cl_df = cl_df.fillna(0)

cols = list(cl_df.columns.values)

for c in range(3, 9):
    mdk_k_means = KMeans(n_init = 50, n_clusters=c, random_state = 2)

    # Fit the model to the training set
    mdk_k_means.fit(cl_df)

    # Get cluster assignments for each data point
    clK = mdk_k_means.labels_

    # Get the centroid of each cluster
    Centroids = mdk_k_means.cluster_centers_

    fig, axs = plt.subplots(len(Centroids), sharex=True, figsize=(15,20))
    main_title = 'Location of Centroids in Each Cluster ('+str(c)+' Clusters)'
    fig.suptitle(main_title)

    for i in range(0, len(Centroids)):
        axs[i].bar(cols, Centroids[i], color='teal')
        title = 'Centroid Values in Cluser ' + str(i)
        axs[i].set_title(title)
        axs[i].tick_params(labelrotation=90)
        axs[i].grid(True, alpha=0.3)


    fig.savefig(r'DataStorage\\Clusters\\'+str(c)+'clusters.png')

    fighters_cl = pd.DataFrame(df['M_NAME'])
    fighters_cl['Cluster'] = clK
    fighters_cl.to_csv(r'DataStorage\\Clusters\\'+str(c)+'clusters.csv')

