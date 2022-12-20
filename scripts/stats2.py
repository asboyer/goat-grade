from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


year = 2023
url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(year)
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
			header = headers[h]
			if header == 'MP':
				header = 'TMP'
			stats[name][header] = td.getText()
			h += 1


with open('../stats/advancedstats.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(stats, ensure_ascii=False, indent =4))

# print(stats['Luka Dončić']['PTS'])

