import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import GridSearchCV

df = pd.read_csv('C:\\Users\\bushi\\Desktop\\University\\Year 3\\Courses\\MIE368\\MIE368-UFC\\DataStorage\\clustering_stats.csv')
cl_df = df.iloc[:, 1:]
cl_df = cl_df.fillna(0)

params_to_search = {'covariance_type': ['full', 'tied', 'diag', 'spherical'], 'n_init': [1,2,3,4,5], 'init_params': ['kmeans', 'random']}

GM = GaussianMixture(max_iter=100,n_components = 5,random_state=0)

search = GridSearchCV(GM, params_to_search, refit=False, cv=5)
search.fit(cl_df)

s_score = search.cv_results_['mean_test_score']
index = s_score.argmax()
selected_params = search.cv_results_['params'][index]
print(selected_params)
opt_GM = GM.set_params(**selected_params)

opt_GM.fit(cl_df)

preds = opt_GM.predict(cl_df)
probs = opt_GM.predict_proba(cl_df)
clusters = ['0', '1', '2', '3', '4']
probs_df = pd.DataFrame(probs, columns=clusters)

orig_cl = pd.DataFrame(df['M_NAME'])
orig_cl['Cluster'] = preds
final = pd.concat([orig_cl, probs_df], axis=1)
final.to_csv('GM.csv')

