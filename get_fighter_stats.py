## main file that reads the fighter's career statistics and outputs data source to csv
## raw and unfiltered data scraped from site

#imports
import urllib.request
from bs4 import BeautifulSoup
import re
import string
import pandas as pd

#creating the columns and rows to be appended to csv file
cols = ['Name', 'SLpM:', 'Str. Acc.:', 'SApM:', 'Str. Def:', 'TD Avg.:', 'TD Acc.:', 'TD Def.:', 'Sub. Avg.:']
rows = []

#append and create a list of links and fighters
links_df = pd.read_csv(r'DataStorage/fighter_details_links.csv', index_col=0)
links = links_df.iloc[:,0]
fighters = links.index.values.tolist()

#for every fighter, we web scrape their career statistics
for i in range(0, len(links)):
    
    url = links[i]

    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')
    
    data = soup.find("div", {"class": "b-list__info-box-left"}).get_text(strip=True)
    
    #getting rid of the words and just keeping the numbers
    #please do not judge me for my jank code
    data = data.replace('Career statistics:SLpM:','')
    data = data.replace('Str. Acc.:',' ')
    data = data.replace('SApM:',' ')
    data = data.replace('Str. Def:', ' ')
    data = data.replace('TD Avg.:',' ')
    data = data.replace('TD Acc.:',' ')
    data = data.replace('TD Def.:',' ')
    data = data.replace('Sub. Avg.:',' ')
    
    #finally split on white space
    data = data.split()
    #INSERT fighter name
    data.insert(0,fighters[i])
    
    #APPEND the fucking data
    rows.append(data)
    
table = pd.DataFrame(rows, columns=cols)
table.to_csv(r'DataStorage/fighter_stats.csv', index=False)