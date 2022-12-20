from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

# scraping

year = 1950

def scrape(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")  
    
    headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]
    headers = headers[1:]

    rows = soup.findAll('tr')[1:]

    stats = {}
    for i in range(len(rows)):
        tds = rows[i].findAll("td")
        if len(tds) > 0:
            name = tds[0].getText()
            try:
                if stats[name] != {}:
                    h = 0
                    player_dict = {}
                    for td in tds:
                        header = headers[h]
                        if header == 'MP' and 'advanced' in url:
                            header = 'TMP'
                        stats[name][header] = td.getText()
                    if player_dict["Tm"] == "TOT":
                        stats[name] = player_dict
                    else:
                        pass
            except:
                stats[name] = {}
                h = 0
                for td in tds:
                    header = headers[h]
                    if header == 'MP' and 'advanced' in url:
                        header = 'TMP'
                    stats[name][header] = td.getText()
                    h += 1
    return stats

reg_stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
adv_stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"

try:
    reg_stats = scrape(reg_stats_url)
    adv_stats = scrape(adv_stats_url)
except:
    print(f'{year} season not found')

for player in reg_stats:
    reg_stats[player].update(adv_stats[player])

with open('stats.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(reg_stats, ensure_ascii=False, indent =4))


with open('stats.json', 'r', encoding='utf8') as file:
    stats = json.load(file)

# ranking

ranks = {}
for player in stats:
    ranks[player] = {}

categories = ["PTS", "AST", "TRB", "FG%", "FT%", "3P%", "STL", "BLK", "MP", "PER", "TS%", "WS", "BPM"]

def rank(category):
    category_rankings = []
    for player in stats:
        if stats[player][category] != "":
            category_rankings.append([player, float(stats[player][category])])
        else:
            category_rankings.append([player, 0])
    category_rankings = sorted(category_rankings, key=lambda x: x[1])
    category_rankings.reverse()

    for i in range(len(category_rankings)):
        name = category_rankings[i][0]
        value = category_rankings[i][1]
        ranks[name][category] = i + 1

for category in categories:
    rank(category)

for player in ranks:
    score = 0
    for category in ranks[player]:
        score += ranks[player][category]
    ranks[player]['grade'] = score

final_ranks = []
for player in ranks:
    final_ranks.append([player, int(ranks[player]['grade'])])
final_ranks = sorted(final_ranks, key=lambda x: x[1])

#__________

final_string = ""
for i in range(len(final_ranks)):
    name = final_ranks[i][0]
    grade = final_ranks[i][1]
    if i == len(final_ranks) - 1:
        final_string += f"{str(i + 1)}. {name} (score: {str(grade)})"
    else:
        final_string += f"{str(i + 1)}. {name} (score: {str(grade)})\n"  

with open('ranks.json', 'w+', encoding='utf8') as file:
    file.write(json.dumps(ranks, ensure_ascii=False, indent =4))

with open('final.txt', 'w+', encoding='utf8') as file:
    file.write(final_string)
