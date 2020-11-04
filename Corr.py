import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

pd.set_option('display.max_columns', 46)
df = pd.read_csv(r'DataStorage\\cleaned_fight_stats.csv')
df = df.iloc[:, 1:]
df = pd.get_dummies(df, columns=['Method'])
# Split the data
X_train, X_val, y_train, y_val = train_test_split(df.drop(columns=['M_RES']), df.M_RES, test_size = 0.3, random_state = 1)


# Make a dataframe for the training data
df_train = X_train.join(y_train)

corr_matrix = df_train.corr()

corr_matrix.to_csv(r'DataStorage\\correlation.csv')