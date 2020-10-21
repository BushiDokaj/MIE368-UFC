import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
fightlist = []
with open("DataStorage/fighter_details_links.csv") as csvfile:
    file = csv.reader(csvfile)
    next(file)
    count = 0
    for row in file:
        url = row[0]
        r = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r, 'html.parser')
        for link in soup.find_all('a', attrs={'href': re.compile('(fight-details)')}):
            fightlist.append(link.get('href'))
        count = count + 1
        if count == 4999:
            break

    table = pd.DataFrame(fightlist, columns=['Link'])
    table.to_csv(r'DataStorage\\fight_details_links.csv', index=False)