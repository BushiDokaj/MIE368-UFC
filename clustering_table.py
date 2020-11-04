import pandas as pd
import numpy as np

cols = ['Method', 'ROUNDS', 'TIME', 'M_RES', 'M_NAME', 'M_KD', 'M_SUB_ATT', 'M_REV', 'M_CTRL']

stats = pd.read_csv(r'DataStorage\\cleaned_fight_stats.csv')

stats = pd.get_dummies(stats, columns=['Method'])