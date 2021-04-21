from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


year = 2021
url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html#all_expanded_standings".format(year)
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')


soup.findAll('tr', limit=2)
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:]

print(headers)

rows = soup.findAll('tr')[1:]

print(rows)