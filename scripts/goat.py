import requests
from bs4 import BeautifulSoup

URL = 'https://www.espn.com/nba/stats/player/_/table/offensive/sort/avgPoints/dir/desc'
page = requests.get(URL) 

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='fittPageContainer')

rank_elems = results.find_all('tbody', class_='Table__TBODY')

for job_elem in rank_elems:
    tier_elem = rank_elem.find('td', class_='Table__TD')
    name_elem = rank_elem.find('a', class_='AnchorLink') team_elem =
    rank_elem.find('span', class_='pl2 n10 athleteCell__teamAbbrev') if None in
    (tier_elem, name_elem, team_elem): continue print(tier_elem.text.strip())
    print(name_elem.text.strip()) print(team_elem.text.strip()) print()

