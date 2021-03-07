from urllib.request import urlopen
from bs4 import BeautifulSoup


year = 2021
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')



soup.findAll('tr', limit=2)
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:]


rows = soup.findAll('tr')[1:]


with open('../stats/stats.txt', 'w+', encoding='utf-8') as file:
	for i in range(len(rows)):
		file.write("_________\n")
		h = 0
		# player
		for td in rows[i].findAll('td'):
			# each td is a stat
			file.write(headers[h] + ": " + td.getText() + "\n")
			h += 1

