## getting a link for each fighters personal page
## This script loops through the letters of the alphabet to get a url for each page that lists fighters
## Then it reads the page to get the links to each fighters personal page

import urllib.request
from bs4 import BeautifulSoup
import re
import string
import pandas as pd

alpha = list(string.ascii_lowercase)

fighters = []

for letter in alpha:
    url = 'http://www.ufcstats.com/statistics/fighters?char=' + letter + '&page=all'

    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')

    for link in soup.find_all('a', attrs={'href': re.compile('(fighter-details)')}):
        fighters.append(link.get('href'))

table = pd.DataFrame(fighters, columns=['Link'])
table.to_csv(r'DataStorage\\fighter_details_links.csv', index=False)