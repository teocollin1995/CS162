import requests
from bs4 import BeautifulSoup
import re
import csv

#Setup requestsion info
data = {'authpw':'lets.code'}
session = requests.Session()
#login 
session.post('http://brick.cs.uchicago.edu/Courses/CMSC-16200/2015/pmwiki/pmwiki.php', data=data)

#starting page for finding all changes:
start = 'http://brick.cs.uchicago.edu/Courses/CMSC-16200/2015/pmwiki/pmwiki.php/Profiles/Profiles'
# go to go start:
profiles = session.get(start)
#get bs4 obj of profile pages
profiles_bs4 = BeautifulSoup(profiles.text)
#get sections with links
profiles_list = profiles_bs4.find_all('div')[5]
#get all links to profiles
profiles = [x.get('href') for x in profiles_list.find_all('a')  if 'Profiles' in x.get('href')]
#for collecting all links that someone is likely to change...
all_links = []
#collect them from all the profile pages -- same process as above  - more or less
for x in profiles:
    new_profile = session.get(x)
    link_soup = BeautifulSoup(new_profile.text).find_all(id='wikitext')[0]
    links = link_soup.find_all('a')
    results = [x.get('href') for x in links if 'pmwiki' in x.get('href')]
    all_links += results


all_targets = [x +'?action=diff' for x in list(set(all_links))] # gets the diffrence links from all the links
month_dict = {'January': '1', 'February':'2', 'March':'3'} # for converting dates

all_edits = [] # all edits in form (mdd,editor)

# run through all targets to get all the list of all diffrences
for x in all_targets:
    print(x)
    diff = BeautifulSoup(session.get(x).text)
    # within a history page, get each diffrence entry
    diff_lines = diff.find_all(class_='difftime')
    #all all the diffrences in the format that I want
    for y in diff_lines:
        all_edits.append((month_dict[re.search('[A-Za-z]+',y.a.text).group(0)] + re.search('[A-Za-z]+ [0-9]{0,2}', y.a.text).group(0)[-2:],y.span.text))
        
# sort'em
all_edits.sort()

# open a csv file
f = open('results.csv', 'wt')
# write to a csv
try:
    writer = csv.writer(f)
    writer.writerow(('stamp','user'))
    for x in all_edits:
        writer.writerow(x)
finally:
    f.close()



