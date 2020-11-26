import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

pd.set_option('display.max_columns',50)
def make_models():
    """Makes a dictionary of two untrained models"""
    return {
        'LogReg': LogisticRegression(random_state=0, max_iter=5000)}
#     return {
#         'LR_L2': LogisticRegression(random_state=0, max_iter=5000),
#         'LR_L1': LogisticRegression(random_state=0, penalty='l1', solver='liblinear', max_iter=5000, class_weight='balanced'),
#         'LogRegCV': LogisticRegressionCV(penalty='l1', solver='liblinear', max_iter=10000)}


model_names = ['LogReg']
cluster_num = ("1","2","3","4","5")

dropping = ["M_RES", "M_NAME", "OP_NAME", "TIME", "ROUNDS", "Method", "Unnamed: 0", "Cluster #", "OP_RES", "M_KD", "OP_KD"]
df_indices = pd.MultiIndex.from_product([model_names, cluster_num], names=('model names', 'cluster'))
all_models = pd.DataFrame(index=df_indices, columns=pd.read_csv(r'expanded_data\\clusters\\cluster_0.csv').drop(dropping, axis=1).columns)
all_models["Train Score"] = np.nan
all_models["Test Score"] = np.nan
cluster0 = pd.read_csv(r'expanded_data\\clusters\\cluster_0.csv').fillna(0)
cluster1 = pd.read_csv(r'expanded_data\\clusters\\cluster_1.csv').fillna(0)
cluster2 = pd.read_csv(r'expanded_data\\clusters\\cluster_2.csv').fillna(0)
cluster3 = pd.read_csv(r'expanded_data\\clusters\\cluster_3.csv').fillna(0)
cluster4 = pd.read_csv(r'expanded_data\\clusters\\cluster_4.csv').fillna(0)


all_clusters = [cluster0,cluster1,cluster2,cluster3,cluster4]

params_to_search = [{'penalty':['l1'], 'solver':['liblinear', 'saga'], 'class_weight': ['balanced', None], 'C': [1,2,3,4,5]},
{'penalty':['l2'], 'solver': ['newton-cg', 'lbfgs', 'sag'], 'class_weight': ['balanced', None], 'C': [1,2,3,4,5]},
{'penalty': ['elasticnet'], 'solver':['saga'], 'class_weight': ['balanced', None], 'l1_ratio': np.linspace(0,1,10), 'C': [1,2,3,4,5]}]


count = 0

for cluster in all_clusters:

    count = count + 1
    print(count)

    cluster['M_SIG_STR_P'] = cluster['M_SIG_STR_P'].str.rstrip('%').astype('float') / 100.0
    cluster['M_TD_P'] = cluster['M_TD_P'].str.rstrip('%').astype('float') / 100.0
    cluster['OP_SIG_STR_P'] = cluster['OP_SIG_STR_P'].str.rstrip('%').astype('float') / 100.0
    cluster['OP_TD_P'] = cluster['OP_TD_P'].str.rstrip('%').astype('float') / 100.0

    X_train, X_test, y_train, y_test = train_test_split(cluster.drop(columns=dropping), cluster.M_RES, test_size=0.3, random_state=1)
    X_train.fillna(0, inplace=True)
    X_test.fillna(0, inplace=True)
    
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    models_dict = make_models()
    for model_name in models_dict:
        print(model_name)
        model = models_dict[model_name]

        optimized = GridSearchCV(model, params_to_search, scoring=['recall', 'precision'], refit=False, cv=5)
        optimized.fit(X_train, y_train)
        mean_test_precision = optimized.cv_results_['mean_test_precision']
        mean_test_recall = optimized.cv_results_['mean_test_recall']
        s_score = np.add(mean_test_precision, mean_test_recall)
        index = s_score.argmax()
        selected_params = optimized.cv_results_['params'][index]
        print(selected_params)

        opt_model = model.set_params(**selected_params)
        opt_model.fit(X_train, y_train)
        train_score = opt_model.score(X_train, y_train)
        test_score = opt_model.score(X_test, y_test)
        # col = scaler.inverse_transform(opt_model.coef_).tolist()[0]
        col = opt_model.coef_.tolist()[0]
        col.append(train_score)
        col.append(test_score)
        all_models.loc[model_name, str(count)] = tuple(col)
all_models.to_csv(r'expanded_data\\logistic_regression.csv')




