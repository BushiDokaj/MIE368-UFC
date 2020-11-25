import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

pd.set_option('display.max_columns',50)
def make_models():
    """Makes a dictionary of two untrained models"""

    return {
        'LR_L2': LogisticRegression(random_state=0, solver='liblinear'),
        'LR_L1': LogisticRegression(random_state=0, penalty='l1', solver='liblinear', class_weight='balanced')}


model_names = ("LR_L1", "LR_L2")
cluster_num = ("1","2","3","4","5")
df_indices = pd.MultiIndex.from_product([model_names, cluster_num], names=('model names', 'cluster'))
all_models = pd.DataFrame(index=df_indices, columns=pd.read_csv(r'expanded_data\\clusters\\cluster_0.csv').drop(["M_RES", "M_NAME", "OP_NAME", "TIME", "ROUNDS", "Method", "Unnamed: 0", "Cluster #"], axis=1).columns)
all_models["Score"] = np.nan

cluster0 = pd.read_csv(r'expanded_data\\clusters\\cluster_0.csv').fillna(0)
cluster1 = pd.read_csv(r'expanded_data\\clusters\\cluster_1.csv').fillna(0)
cluster2 = pd.read_csv(r'expanded_data\\clusters\\cluster_2.csv').fillna(0)
cluster3 = pd.read_csv(r'expanded_data\\clusters\\cluster_3.csv').fillna(0)
cluster4 = pd.read_csv(r'expanded_data\\clusters\\cluster_4.csv').fillna(0)


all_clusters = [cluster0,cluster1,cluster2,cluster3,cluster4]

count = 0

for cluster in all_clusters:
    cluster = cluster.replace("", 0)

    count = count + 1
    print(count)
    X_train = cluster.drop(["M_RES", "M_NAME", "OP_NAME", "TIME", "ROUNDS", "Method", "Unnamed: 0", "Cluster #"], axis=1)
    X_train['M_SIG_STR_P'] = X_train['M_SIG_STR_P'].str.rstrip('%').astype('float') / 100.0
    X_train['M_TD_P'] = X_train['M_TD_P'].str.rstrip('%').astype('float') / 100.0
    X_train['OP_SIG_STR_P'] = X_train['OP_SIG_STR_P'].str.rstrip('%').astype('float') / 100.0
    X_train['OP_TD_P'] = X_train['OP_TD_P'].str.rstrip('%').astype('float') / 100.0

    y_train = cluster.M_RES
    models_dict = make_models()
    for model_name in models_dict:
        model = models_dict[model_name]
        X_train.fillna(0, inplace=True)

        model.fit(X_train, y_train)
        score = model.score(X_train, y_train)
        all_models.loc[model_name, str(count)] = (model.coef_, score)
print(all_models)




