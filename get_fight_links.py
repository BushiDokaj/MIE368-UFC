import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re

fightlist = []

links_df = pd.read_csv(r'DataStorage\\fighter_details_links.csv', index_col=0)
links = links_df.iloc[:,0]
fighters = links.index.values.tolist()

for i in range(0, len(links)):
    url = links[i]

    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')

    for link in soup.find_all('a', attrs={'href': re.compile('(fight-details)')}):
        fight =  [fighters[i], link.get('href')]
        fightlist.append(fight)

table = pd.DataFrame(fightlist, columns=['Name', 'Link'])
table.to_csv(r'DataStorage\\fight_details_links.csv', index=False)