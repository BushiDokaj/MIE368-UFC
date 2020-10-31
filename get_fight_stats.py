## main file that reads the fight statistics and outputs data source to csv
## raw and unfiltered data scraped from site

import urllib.request
from bs4 import BeautifulSoup
import re
import string
import pandas as pd

url = "http://www.ufcstats.com/fight-details/e7a915f39ecf6db0"

r = urllib.request.urlopen(url).read()
soup = BeautifulSoup(r, 'html.parser')

rounds = int(soup.find_all('i', attrs={'class': 'b-fight-details__text-item'})[0].getText().strip()[24])

out = []
for status in soup.find_all('i', attrs={'class': re.compile('(b-fight-details__person-status)')}):
    out.append(status.getText().strip())

method = []
for child in soup.find_all('i', attrs={'class': 'b-fight-details__text-item_first'})[0].children:
    if child.string.strip() != '':
        method.append(child.string.strip())

stats = []
keep = []
for stat in soup.find_all('p', attrs={'class': 'b-fight-details__table-text'}):
    stats.append(stat.getText().strip())

keep += stats[0:20]
keep += stats[20*(rounds+1): 20*(rounds+2)-2]

print(out)  
print(method)
print(keep)
