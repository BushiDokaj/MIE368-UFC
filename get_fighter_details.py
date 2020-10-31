## this script gets a link to each personal fighters page
## due to the extensive number of fighters we're only using the top 16 current fighters in every weight division
## the script works for everyone except Chan Sung Jun, so for him we just manually get the link

import urllib.request
from bs4 import BeautifulSoup
import re
import string
import pandas as pd
from random import sample

fighters = pd.read_csv(r'DataStorage\\cur_fighters.csv', squeeze=True)
fighter_links = dict.fromkeys(fighters)

for fighter in fighters:
        names = fighter.split(' ')
        if len(names) == 3:
                q = names[1] + '+' + names[2]
                names[1] = names[1] + ' ' + names[2]
        else:
                q = names[1]
        url = 'http://www.ufcstats.com/statistics/fighters/search?query=' + q + '&page=all'
        
        r = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r, 'html.parser')

        for link in soup.find_all('a', attrs={'href': re.compile('(fighter-details)')}):
                if link.getText().strip() == names[0]:
                        fighter_links[fighter] = link.get('href')
                        break
table = pd.DataFrame.from_dict(fighter_links, orient='index', columns=['Link'])
table.to_csv(r'DataStorage\fighter_details_links.csv')
