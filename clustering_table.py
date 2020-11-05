import pandas as pd
import numpy as np

def sectomin(x):
    return x/60

stats = pd.read_csv(r'DataStorage\\cleaned_fight_stats.csv')

stats = stats.iloc[:, 1:]
stats = stats.drop(['OP_NAME'], axis=1)
stats = pd.get_dummies(stats, columns=['Method'])
stats['M_SIG_STR_P'] = pd.to_numeric(stats['M_SIG_STR_P'].str.rstrip('%'))
stats['M_TD_P'] = pd.to_numeric(stats['M_TD_P'].str.rstrip('%'))

cols_st = list(stats.columns.values)[4:-7]
cols_st.remove('M_SIG_STR_P')
cols_st.remove('M_TD_P')
cols_st.remove('M_CTRL')
cols_st.remove('OP_SIG_STR_P')
cols_st.remove('OP_TD_P')
cols_st.remove('OP_CTRL')

time = stats['TIME'].apply(sectomin)

for col in cols_st:
    stats[col] = stats[col] / time

# main fighters data
# striking_p = stats[['M_NAME', 'M_SIG_STR_P']]
# striking_p = striking_p.groupby('M_NAME').mean()

# takedown_p = stats[['M_NAME', 'M_TD_P']]
# takedown_p = takedown_p.groupby('M_NAME').mean()

control_time = stats[['M_NAME', 'M_CTRL']]
control_time = control_time.groupby('M_NAME').sum().apply(sectomin)

# result_means = stats[['M_NAME', 'M_RES']].groupby('M_NAME').mean()

# oponents data
# striking_p_OP = stats[['OP_NAME', 'OP_SIG_STR_P']]
# striking_p_OP = striking_p_OP.groupby('OP_NAME').mean()

# takedown_p_OP = stats[['OP_NAME', 'OP_TD_P']]
# takedown_p_OP = takedown_p_OP.groupby('OP_NAME').mean()

control_time_OP = stats[['M_NAME', 'OP_CTRL']]
control_time_OP = control_time_OP.groupby('M_NAME').sum().apply(sectomin)

# result_means_OP = stats[['OP_NAME', 'OP_RES']].groupby('OP_NAME').mean()

stats = stats.groupby(['M_NAME']).mean()

stats['M_CTRL'] = control_time['M_CTRL']
stats['OP_CTRL'] = control_time_OP['OP_CTRL']
# stats['M_SIG_STR_P'] = striking_p['M_SIG_STR_P']
# stats['M_TD_P'] = takedown_p['M_TD_P']

stats = stats.drop(['ROUNDS', 'TIME'], axis=1)

stats.to_csv(r'DataStorage\\clustering_stats.csv')