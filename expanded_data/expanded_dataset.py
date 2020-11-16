import urllib.request
from bs4 import BeautifulSoup
import re
import string
import pandas as pd
import os

cols = ['Method', 'ROUNDS', 'TIME', 'M_RES', 'M_NAME', 'M_KD', 'M_SIG_STR', 'M_SIG_STR_P', 'M_TOTAL_STR', 'M_TD',
        'M_TD_P','M_SUB_ATT', 'M_REV', 'M_CTRL', 'M_HEAD', 'M_BODY', 'M_LEG', 'M_DIST', 'M_CLIN', 'M_GROUND',
        'OP_RES', 'OP_NAME', 'OP_KD', 'OP_SIG_STR', 'OP_SIG_STR_P', 'OP_TOTAL_STR', 'OP_TD','OP_TD_P', 'OP_SUB_ATT',
        'OP_REV', 'OP_CTRL', 'OP_HEAD', 'OP_BODY', 'OP_LEG', 'OP_DIST', 'OP_CLIN','OP_GROUND']


letters = ['x', 'y', 'z'] 

def get_fighter_links(letter):
    url = "http://www.ufcstats.com/statistics/fighters?char=" + letter + "&page=all"

    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')

    links = []

    for link in soup.find_all('a', attrs={'href': re.compile('(fighter-details)')}):
        if link.get('href') in links:
            continue
        else:
            links.append(link.get('href'))

    return links

def get_fight_links(links):
    fights_map = {}

    for i in range(0, len(links)):
        url = links[i]

        r = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r, 'html.parser')

        name = soup.find_all('span', attrs={'class': "b-content__title-highlight"})[0].getText().strip()

        fights = []

        for link in soup.find_all('a', attrs={'href': re.compile('(fight-details)')}):
            fight = link.get('href')
            fights.append(fight)
        
        fights_map[name] = fights

    return fights_map
    
def get_fight_stats(mapping):
        rows = []

        for key, value in mapping.items():
                Name = key

                for i in range(0, len(value)):
                
                        url = value[i]
                        print(url)

                        r = urllib.request.urlopen(url).read()
                        soup = BeautifulSoup(r, 'html.parser')

                        event = soup.find_all('a', attrs={'href': re.compile('(event-details)')})[0].getText().strip()
                        if len(re.findall('(UFC|WEC|Strikeforce|The Ultimate Fighter)', event)) == 0:
                                print('Not an MMA fight under UFC Rules: ' + url)
                                continue
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
                                        continue
                                rows.append(row)
                        except IndexError:
                                print('IndexError with: ' + url)
                                continue
        stats_df = pd.DataFrame(rows, columns=cols)
        return stats_df

for letter in letters:
        fighters = get_fighter_links(letter)
        fight_mapping = get_fight_links(fighters)
        stats_df = get_fight_stats(fight_mapping)

        stats_df.to_csv(r'data_per_letter\\' + letter + '_fight_stats.csv')