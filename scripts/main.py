from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


year = 2021
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')


soup.findAll('tr', limit=2)
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:]


rows = soup.findAll('tr')[1:]

stats = {}

for i in range(len(rows)):
	if len(rows[i].findAll('td')) > 0:
		h = 0
		name = rows[i].findAll('td')[0].getText()
		stats[name] = {}
		for td in rows[i].findAll('td'):
			stats[name][headers[h]] = td.getText()
			h += 1


json_object = json.dumps(stats, indent = 4)
print(json_object)
# print(stats['Bradley Beal']['PTS'])
