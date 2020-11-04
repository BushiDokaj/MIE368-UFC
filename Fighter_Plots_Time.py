import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
def sectomin(x):
    return x/60


pd.set_option('display.max_columns', 100)
pd.set_option("display.max_rows", 200)
df = pd.read_csv(r'DataStorage\\cleaned_fight_stats.csv')
df = df.iloc[:, 1:]

# Split the data
X_train, X_val, y_train, y_val = train_test_split(df.drop(columns=['M_RES']), df.M_RES, test_size = 0.3, random_state = 1)


# Make a dataframe for the training data
df_train = X_train.join(y_train)
fighter_sums = df_train.groupby(["M_NAME"]).sum()
fighter_sums["TIME"] = fighter_sums["TIME"].apply(sectomin)
fighter_sums["M_SIG_STR_SUCC"] = fighter_sums["M_SIG_STR_SUCC"] / fighter_sums["TIME"]
fighter_sums["M_SUB_ATT"] = fighter_sums["M_SUB_ATT"] / fighter_sums["TIME"]
fighter_sums["M_CLIN_SUCC"] = fighter_sums["M_CLIN_SUCC"] / fighter_sums["TIME"]
fighter_sums["M_GROUND_SUCC"] = fighter_sums["M_GROUND_SUCC"] / fighter_sums["TIME"]
fighter_sums["M_TD_SUCC"] = fighter_sums["M_TD_SUCC"] / fighter_sums["TIME"]
fighter_sums.to_csv(r'DataStorage\\fightersumstime.csv')

best_strikers = fighter_sums.nlargest(5, ["M_SIG_STR_SUCC"])["M_SIG_STR_SUCC"]
best_subs = fighter_sums.nlargest(5, ["M_SUB_ATT"])["M_SUB_ATT"]
best_clinchers = fighter_sums.nlargest(5, ["M_CLIN_SUCC"])["M_CLIN_SUCC"]
best_ground = fighter_sums.nlargest(5, ["M_GROUND_SUCC"])["M_GROUND_SUCC"]
best_takedown = fighter_sums.nlargest(5, ["M_TD_SUCC"])["M_TD_SUCC"]
worst_strikers = fighter_sums.nsmallest(5, ["M_SIG_STR_SUCC"])["M_SIG_STR_SUCC"]
worst_subs = fighter_sums.nsmallest(5, ["M_SUB_ATT"])["M_SUB_ATT"]
worst_clinchers = fighter_sums.nsmallest(5, ["M_CLIN_SUCC"])["M_CLIN_SUCC"]
worst_ground = fighter_sums.nsmallest(5, ["M_GROUND_SUCC"])["M_GROUND_SUCC"]
worst_takedown = fighter_sums.nsmallest(5, ["M_TD_SUCC"])["M_TD_SUCC"]

bestplots = [best_strikers,best_takedown,best_ground,best_clinchers,best_subs]

for i in bestplots:
    i.plot.bar()
    plt.xlabel("Name")
    plt.ylabel(i.name + " (per minute)")
    plt.savefig(r'DataStorage\\best' + i.name + 'permin.png')

worstplots = [worst_strikers,worst_takedown,worst_ground,worst_clinchers,worst_subs]

for i in worstplots:
    i.plot.bar()
    plt.xlabel("Name")
    plt.ylabel(i.name + " (per minute)")
    plt.savefig(r'DataStorage\\worst' + i.name + 'permin.png')