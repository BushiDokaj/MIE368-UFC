import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter

stats = pd.read_csv(r'DataStorage\\cleaned_fight_stats.csv')

def sectomin(x):
    return x/60

def best_plot(stat):
    stat.plot.bar()
    plt.xlabel("Name")
    plt.xticks(rotation=0)
    plt.ylabel(stat.name + " (per minute)")
    plt.title('best ' + stat.name + ' permin')
    plt.show()

def worst_plot(stat):
    stat.plot.bar()
    plt.xlabel("Name")
    plt.xticks(rotation=0)
    plt.ylabel(stat.name + " (per minute)")
    plt.title('worst ' + stat.name + ' permin.png')
    plt.show()

fighter_sums = stats.groupby(["M_NAME"]).sum()

# normalizing the plots for time
fighter_sums["TIME"] = fighter_sums["TIME"].apply(sectomin)
fighter_sums["M_SIG_STR"] = fighter_sums["M_SIG_STR"] / fighter_sums["TIME"]
fighter_sums["M_SUB_ATT"] = fighter_sums["M_SUB_ATT"] / fighter_sums["TIME"]
fighter_sums["M_CLIN"] = fighter_sums["M_CLIN"] / fighter_sums["TIME"]
fighter_sums["M_GROUND"] = fighter_sums["M_GROUND"] / fighter_sums["TIME"]
fighter_sums["M_TD"] = fighter_sums["M_TD"] / fighter_sums["TIME"]

best_strikers = fighter_sums.nlargest(5, ["M_SIG_STR"])["M_SIG_STR"]
best_subs = fighter_sums.nlargest(5, ["M_SUB_ATT"])["M_SUB_ATT"]
best_clinchers = fighter_sums.nlargest(5, ["M_CLIN"])["M_CLIN"]
best_ground = fighter_sums.nlargest(5, ["M_GROUND"])["M_GROUND"]
best_takedown = fighter_sums.nlargest(5, ["M_TD"])["M_TD"]
worst_strikers = fighter_sums.nsmallest(5, ["M_SIG_STR"])["M_SIG_STR"]
worst_subs = fighter_sums.nsmallest(5, ["M_SUB_ATT"])["M_SUB_ATT"]
worst_clinchers = fighter_sums.nsmallest(5, ["M_CLIN"])["M_CLIN"]
worst_ground = fighter_sums.nsmallest(5, ["M_GROUND"])["M_GROUND"]
worst_takedown = fighter_sums.nsmallest(5, ["M_TD"])["M_TD"]

# get a worst plot for a stat
# worst_plot(worst_strikers)

# get a best plot for a stat
best_plot(best_strikers)

# get correlation matrix only for main fighter (clustering)
# df = stats.iloc[:, 1:17]
# df['M_SIG_STR_P'] = pd.to_numeric(df['M_SIG_STR_P'].str.rstrip('%'))
# df['M_TD_P'] = pd.to_numeric(df['M_TD_P'].str.rstrip('%'))
# corr_matrix = df.corr()
# plt.figure(figsize = (16,5))
# sns.heatmap(corr_matrix, annot=True)
# plt.show()

# get correlation matrix only for main fighter and opponent data (regression)
# df = stats.iloc[:, 1:]
# corr_matrix = df.corr()
# plt.figure(figsize = (16,5))
# sns.heatmap(corr_matrix, annot=True)
# plt.show()
# output to file because it is difficult to view plot
# corr_matrix.to_csv(r'DataStorage\\correlation_matrix_regression.csv')

# get fights that ended in a submission
stats_sub = stats[(stats.Method == 'Submission')]

sub_fighters = stats_sub.M_NAME.tolist()
sub_fighters_uni = stats_sub.M_NAME.unique()
sub_counts = dict.fromkeys(sub_fighters_uni)

for f in sub_fighters_uni:
    sub_counts[f] = sub_fighters.count(f)

top_sub = dict(Counter(sub_counts).most_common(15))

# plt.bar(top_sub.keys(), top_sub.values(), color='teal')
# plt.xlabel('Fighter')
# plt.xticks(rotation=12)
# plt.ylabel('Count')
# plt.title('Count of Submission Victories per Fighter')
# plt.grid(True, alpha=0.3)
# plt.show()

# get fights that ended in a KO/TKO
stats_ko = stats[(stats.Method == 'KO/TKO')]

ko_fighters = stats_ko.M_NAME.tolist()
ko_fighters_uni = stats_ko.M_NAME.unique()
ko_counts = dict.fromkeys(ko_fighters_uni)

for f in ko_fighters_uni:
    ko_counts[f] = ko_fighters.count(f)

top_ko = dict(Counter(ko_counts).most_common(15))

plt.bar(top_ko.keys(), top_ko.values(), color='teal')
plt.xlabel('Fighter')
plt.xticks(rotation=12)
plt.ylabel('Count')
plt.title('Count of KO/TKO victories per fighter')
plt.grid(True, alpha=0.3)
plt.show()

# get fights that ended in a decision and the main fighter won
stats_dec = stats[((stats.Method == 'Decision - Unanimous') | (stats.Method == 'Decision - Split')) & (stats.M_RES == 1)]

# get fights that ended in a decision in a 3 round fight
stats_dec_3 = stats_dec[(stats_dec.ROUNDS == 3)]
print('There are {} 3 round fights that went to a decision'.format(stats_dec_3.shape[0]))

# get fights that ended in a decision in a 5 round fight
stats_dec_5 = stats_dec[(stats_dec.ROUNDS == 5)]
print('There are {} 5 round fights that went to a decision'.format(stats_dec_5.shape[0]))

# comparison of td and strikes in winning 3-round decision fights
# plt.scatter(stats_dec_3.M_SIG_STR, stats_dec_3.M_TD, c='tab:blue')
# plt.xlabel('Significant Strikes Landed in the Fight')
# plt.ylabel('Take-downs Landed in the Fight')
# plt.title('Comparison of Takedowns to Significant Strikes in Winning 3-Round Fights')
# plt.grid(True, alpha=0.3)
# plt.show()

# comparison of td and strikes in winning 5-round decision fights
# plt.scatter(stats_dec_5.M_SIG_STR, stats_dec_5.M_TD, c='tab:red')
# plt.xlabel('Significant Strikes Landed in the Fight')
# plt.ylabel('Take-downs Landed in the Fight')
# plt.title('Comparison of Takedowns to Significant Strikes in Winning 5-Round Fights')
# plt.grid(True, alpha=0.3)
# plt.show()

# histogram of striking in a 3 round decision
# plt.hist(stats_dec_3.M_SIG_STR, bins=25, color='sienna')
# plt.xlabel('Number of Significat Strikes Landed in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Significant Strikes in a 3 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()

# # histogram of striking in a 5 round decision
# plt.hist(stats_dec_5.M_SIG_STR, bins=25, color='tab:green')
# plt.xlabel('Number of Significat Strikes Landed in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Significant Strikes in a 5 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()

# histogram of take-downs in a 3 round decision
# plt.hist(stats_dec_3.M_TD, bins=20, color='tab:orange')
# plt.xlabel('Number of Take-downs Landed in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Take-downs in a 3 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()

# # histogram of take-downs in a 5 round decision
# plt.hist(stats_dec_5.M_TD, bins=15, color='tab:purple')
# plt.xlabel('Number of Take-downs Landed in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Take-downs in a 5 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()

# histogram of submissions in a 3 round decision
# plt.hist(stats_dec_3.M_SUB_ATT, bins=10, color='teal')
# plt.xlabel('Number of Submissions Attempted in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Attempted Submissions in a 3 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()

# # histogram of submissions in a 5 round decision
# plt.hist(stats_dec_5.M_SUB_ATT, bins=15, color='goldenrod')
# plt.xlabel('Number of Submissions Attempted in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Attempted Submissions in a 5 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()
