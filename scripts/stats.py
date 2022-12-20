from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

year = 2023
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:]

rows = soup.findAll('tr')[1:]

stats = {}

for i in range(len(rows)):
	tds = rows[i].findAll('td')
	if len(tds) > 0:
		h = 0
		name = tds[0].getText()
		stats[name] = {}
		for td in tds:
			stats[name][headers[h]] = td.getText()
			h += 1


with open('../stats/stats.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(stats, ensure_ascii=False, indent =4))

# print(stats['Luka Dončić']['PTS'])
