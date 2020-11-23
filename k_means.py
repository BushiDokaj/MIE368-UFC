import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt
import matplotlib.cm as cm

df = pd.read_csv(r'DataStorage\\clustering_stats.csv')
cl_df = df.iloc[:, 1:]
cl_df = cl_df.fillna(0)
print(cl_df.var(axis=0))

cols = list(cl_df.columns.values)

distortions = []
K = range(3,9)
for c in K:
    # Create a subplot with 1 row and 2 columns
    fig, ax1 = plt.subplots(1, 1)
    fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(cl_df) + (c + 1) * 10])
    
    mdk_k_means = KMeans(n_init = 50, n_clusters=c, random_state = 2)

    # Fit the model to the training set
    mdk_k_means.fit(cl_df)

    # Get cluster assignments for each data point
    clK = mdk_k_means.labels_

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed clusters
    silhouette_avg = silhouette_score(cl_df, clK)
    print("For n_clusters =", c, "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(cl_df, clK)

    y_lower = 10
    for i in range(c):
        # Aggregate the silhouette scores for samples belonging to cluster i, and sort them
        ith_cluster_silhouette_values = sample_silhouette_values[clK == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.nipy_spectral(float(i) / c)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters.")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhouette score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    plt.suptitle(("Silhouette analysis for KMeans clustering on sample data "
                  "with n_clusters = %d" % c),
                 fontsize=14, fontweight='bold')

    plt.savefig(r'DataStorage\\Clusters\\silhouette_'+str(c)+'.png')
# Labeling the clusters
# centers = mdk_k_means.cluster_centers_

# plt.show()



# output clusters to files
# fighters_cl = pd.DataFrame(df['M_NAME'])
# fighters_cl['Cluster'] = clK
# fighters_cl.to_csv(r'DataStorage\\Clusters\\'+str(c)+'clusters.csv')

# getting the predictions for the new data
# predictions = mdk_k_means.predict(test)
# pred_cl = pd.DataFrame(testing['M_NAME'])
# pred_cl['Cluster'] = predictions
# pred_cl.to_csv(r'expanded_data\\clusters\\'+str(c)+'test.csv')


# plotting the centroid for each cluster for each k-value
    # fig, axs = plt.subplots(len(Centroids), sharex=True, figsize=(14,30))
    # main_title = 'Location of Centroids in Each Cluster ('+str(c)+' Clusters)'
    # fig.suptitle(main_title)

    # for i in range(0, len(Centroids)):
    #     axs[i].bar(cols, Centroids[i], color='teal')
    #     title = 'Centroid Values in Cluser ' + str(i)
    #     axs[i].set_title(title)
    #     axs[i].set_ylabel('Count')
    #     axs[i].set_xlabel('Centroid Data Points')
    #     axs[i].tick_params(labelrotation=30)
    #     axs[i].grid(True, alpha=0.3)


    # fig.savefig(r'DataStorage\\Clusters\\'+str(c)+'clusters.png')


# testing = pd.read_excel(r'expanded_data\\testing.xlsx')
# test = testing.iloc[:, 1:]
# test = test.fillna(0)


# getting distortions for elbow plot
# distortions.append(mdk_k_means.inertia_)
# getting the elbow plot to help with selecting a k-value
# plt.figure(figsize=(16,8))
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('Value of Parameter K')
# plt.ylabel('Distortion')
# plt.title('Elbow Method for Determining the Optimal K Value')
# plt.savefig(r'DataStorage\\Clusters\\elbow_plot.png')