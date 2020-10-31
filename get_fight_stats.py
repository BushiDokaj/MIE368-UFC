## main file that reads the fight statistics and outputs data source to csv
## raw and unfiltered data scraped from site

import urllib.request
from bs4 import BeautifulSoup
import re
import string
import pandas as pd

cols = ['Method', 'ROUNDS', 'TIME', 'M_RES', 'M_NAME', 'M_KD', 'M_SIG_STR', 'M_SIG_STR_P', 'M_TOTAL_STR', 'M_TD',
        'M_TD_P','M_SUB_ATT', 'M_REV', 'M_CTRL', 'M_HEAD', 'M_BODY', 'M_LEG', 'M_DIST', 'M_CLIN', 'M_GROUND',
        'OP_RES', 'OP_NAME', 'OP_KD', 'OP_SIG_STR', 'OP_SIG_STR_P', 'OP_TOTAL_STR', 'OP_TD','OP_TD_P', 'OP_SUB_ATT',
        'OP_REV', 'OP_CTRL', 'OP_HEAD', 'OP_BODY', 'OP_LEG', 'OP_DIST', 'OP_CLIN','OP_GROUND']

rows = []

fights_df = pd.read_csv(r'DataStorage\\fight_details_links.csv')
for r in range(0, len(fights_df)):

        url = fights_df.iloc[r]['Link']
        print(url)
        Name = fights_df.iloc[r]['Name']

        r = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r, 'html.parser')
        try:
                # get the time the last round lasted to
                time = soup.find_all('i', attrs={'class': 'b-fight-details__text-item'})[1].getText().strip()[23:27]

                # get the total number of rounds that happened
                rounds = int(soup.find_all('i', attrs={'class': 'b-fight-details__text-item'})[0].getText().strip()[24])

                # storing the outcome of each fighter (L/W)
                out = []
                for status in soup.find_all('i', attrs={'class': re.compile('(b-fight-details__person-status)')}):
                        out.append(status.getText().strip())

                # getting the method that the fight was finished in 
                method = []
                for child in soup.find_all('i', attrs={'class': 'b-fight-details__text-item_first'})[0].children:
                        if child.string.strip() != '':
                                method.append(child.string.strip())

                # getting the list of statistics that we need for the total fight
                stats = []
                keep = []
                for stat in soup.find_all('p', attrs={'class': 'b-fight-details__table-text'}):
                        stats.append(stat.getText().strip())

                keep += stats[0:20]
                keep += stats[20*(rounds+1)+6: 20*(rounds+2)-2]

                fighter_1 = []
                fighter_1.append(out[0])
                fighter_2 = []
                fighter_2.append(out[1])

                for i in range(0, len(keep), 2):
                        fighter_1.append(keep[i])
                        fighter_2.append(keep[i+1])

                total_time = str((rounds-1)*5 + int(time.split(':')[0])) + ':' + time.split(':')[1]

                row = []
                row.append(method[1])
                row.append(rounds)
                row.append(total_time)
                if len(re.findall('('+Name.replace(' ','|')+')', fighter_1[1])) >=2:
                        row.extend(fighter_1)
                        row.extend(fighter_2)
                if len(re.findall('('+Name.replace(' ','|')+')', fighter_2[1])) >=2:
                        row.extend(fighter_2)
                        row.extend(fighter_1)
                if len(row) == 71:
                        print('Row too long')
                        print(row)
                        break
                rows.append(row)
        except IndexError:
                print('IndexError with: ' + url)
                continue

stats_df = pd.DataFrame(rows, columns=cols)
stats_df.to_csv(r'DataStorage\\fight_stats.csv')