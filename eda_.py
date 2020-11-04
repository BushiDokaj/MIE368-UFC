import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

stats = pd.read_csv(r'DataStorage\\cleaned_fight_stats.csv')

# get fights that ended in a submission
stats_sub = stats[(stats.Method == 'Submission')]

sub_fighters = stats_sub.M_NAME.tolist()
sub_fighters_uni = stats_sub.M_NAME.unique()
sub_counts = dict.fromkeys(sub_fighters_uni)

for f in sub_fighters_uni:
    sub_counts[f] = sub_fighters.count(f)

top_sub = dict(Counter(sub_counts).most_common(15))

plt.bar(top_sub.keys(), top_sub.values(), color='teal')
plt.xlabel('Fighter')
plt.xticks(rotation=12)
plt.ylabel('Count')
plt.title('Count of Submission Victories per Fighter')
plt.grid(True, alpha=0.3)
plt.show()

# get fights that ended in a KO/TKO
stats_ko = stats[(stats.Method == 'KO/TKO')]

ko_fighters = stats_ko.M_NAME.tolist()
ko_fighters_uni = stats_ko.M_NAME.unique()
ko_counts = dict.fromkeys(ko_fighters_uni)

for f in ko_fighters_uni:
    ko_counts[f] = ko_fighters.count(f)

top_ko = dict(Counter(ko_counts).most_common(15))

# plt.bar(top_ko.keys(), top_ko.values(), color='teal')
# plt.xlabel('Fighter')
# plt.xticks(rotation=12)
# plt.ylabel('Count')
# plt.title('Count of KO/TKO victories per fighter')
# plt.grid(True, alpha=0.3)
# plt.show()

# get fights that ended in a decision and the main fighter won
stats_dec = stats[((stats.Method == 'Decision - Unanimous') | (stats.Method == 'Decision - Split')) & (stats.M_RES == '1')]

# get fights that ended in a decision in a 3 round fight
stats_dec_3 = stats_dec[(stats_dec.ROUNDS == 3)]
print('There are {} 3 round fights that went to a decision'.format(stats_dec_3.shape[0]))

# get fights that ended in a decision in a 5 round fight
stats_dec_5 = stats_dec[(stats_dec.ROUNDS == 5)]
print('There are {} 5 round fights that went to a decision'.format(stats_dec_5.shape[0]))

# comparison of td and strikes in winning 3-round decision fights
# plt.scatter(stats_dec_3.M_SIG_STR_SUCC, stats_dec_3.M_TD_SUCC, c='tab:blue')
# plt.xlabel('Significant Strikes Landed in the Fight')
# plt.ylabel('Take-downs Landed in the Fight')
# plt.title('Comparison of Takedowns to Significant Strikes in Winning 3-Round Fights')
# plt.grid(True, alpha=0.3)
# plt.show()

# comparison of td and strikes in winning 5-round decision fights
# plt.scatter(stats_dec_5.M_SIG_STR_SUCC, stats_dec_5.M_TD_SUCC, c='tab:red')
# plt.xlabel('Significant Strikes Landed in the Fight')
# plt.ylabel('Take-downs Landed in the Fight')
# plt.title('Comparison of Takedowns to Significant Strikes in Winning 5-Round Fights')
# plt.grid(True, alpha=0.3, alpha=0.3)
# plt.show()

# histogram of striking in a 3 round decision
# plt.hist(stats_dec_3.M_SIG_STR_SUCC, bins=25, color='sienna')
# plt.xlabel('Number of Significat Strikes Landed in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Significant Strikes in a 3 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()

# # histogram of striking in a 5 round decision
# plt.hist(stats_dec_5.M_SIG_STR_SUCC, bins=25, color='tab:green')
# plt.xlabel('Number of Significat Strikes Landed in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Significant Strikes in a 5 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()

# histogram of take-downs in a 3 round decision
# plt.hist(stats_dec_3.M_TD_SUCC, bins=20, color='tab:orange')
# plt.xlabel('Number of Take-downs Landed in the Fight')
# plt.ylabel('Count of Occurences')
# plt.title('Histogram of Take-downs in a 3 round fight')
# plt.grid(True, alpha=0.3)
# plt.show()

# # histogram of take-downs in a 5 round decision
# plt.hist(stats_dec_5.M_TD_SUCC, bins=15, color='tab:purple')
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
