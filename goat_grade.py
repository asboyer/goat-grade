from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import os

root = os.path.dirname(__file__)

NBA_SEASON = [10, 11, 12, 1, 2, 3, 4, 5, 6]

def scrape(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")  
    
    headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]
    headers = headers[1:]

    rows = soup.findAll("tr")[1:]

    stats = {}
    for i in range(len(rows)):
        tds = rows[i].findAll("td")
        if len(tds) > 0:
            name = tds[0].getText()
            try:
                if stats[name] != {}:
                    h = 0
                    for td in tds:
                        header = headers[h]
                        if header == "Tm":
                            team = td.getText()
                        h += 1
                    stats[name]["Tm"].append(team)
            except:
                stats[name] = {}
                h = 0
                for td in tds:
                    header = headers[h]
                    if header == "MP" and "advanced" in url:
                        header = "TMP"
                    stats[name][header] = td.getText()
                    h += 1
                if stats[name]["Tm"] == "TOT":
                    stats[name]["Tm"] = []
    return stats

def get_stats(year, categories, folder):
    reg_stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    adv_stats_url = f"https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"
    try:
        reg_stats = scrape(reg_stats_url)
        adv_stats = scrape(adv_stats_url)
    except:
        raise TypeError("URL")
        return

    for player in list(reg_stats):
        reg_stats[player].update(adv_stats[player])

    old_categories = []

    for i in range(len(categories)):
        category = categories[i]
        if reg_stats[list(reg_stats)[0]][category] == "":
            for player in list(reg_stats):
                del reg_stats[player][category]
            old_categories.append(category)

    for category in old_categories:
        categories.remove(category)

    for player in list(reg_stats):
        try:
            del reg_stats[player]["<0xa0>"]
        except:
            pass
        try:
            if float(reg_stats[player]["G"]) < 10 or float(reg_stats[player]["MP"]) < 10:
                del reg_stats[player]
        except:
            if float(reg_stats[player]["G"]) < 10:
                del reg_stats[player]

    with open(os.path.join(root, f"stats/raw_stats{year}.json"), "w+", encoding="utf8") as file:
        file.write(json.dumps(reg_stats, ensure_ascii=False, indent =4))

    return reg_stats, categories


def GOAT_GRADE(year,
            update=True,
            categories=[
                        "PTS", "AST", "TRB", "FG%", "FT%", "3P%", "STL", "BLK",
                        "MP", "PER", "TS%", "WS", "BPM", "2P%", "OWS", "DWS", 
                        "WS/48", "USG%", "OBPM", "DBPM", "VORP", "eFG%"
                        ],
            all_time_categories=["eFG%", "2P%","FG%", "AST", "PTS", "TS%", "FT%"],
            extra_categories=[],
            folder="",
            file_name="ranks"):

    categories = list(categories + extra_categories)

    if update:
        stats, categories = get_stats(year, categories, folder)
    else:
        # # offline mode
        # if not os.path.exists(f"stats/raw_stats{year}.json", "r", encoding="utf8")

        f = open(os.path.join(root, f"stats/raw_stats{year}.json"), "r", encoding="utf8")
        stats = json.load(f)
        f.close()

        old_categories = []

        for i in range(len(categories)):
            category = categories[i]
            if category not in list(stats[list(stats)[0]]):
                old_categories.append(category)

        for category in old_categories:
            categories.remove(category)

    ranks = {}
    for player in stats:
        ranks[player] = {}

    topster_averages = []

    def rank(category):
        category_rankings = []
        for player in stats:
            if stats[player][category] != "":
                category_rankings.append([player, float(stats[player][category])])
            else:
                category_rankings.append([player, 0])
        category_rankings = sorted(category_rankings, key=lambda x: x[1])
        category_rankings.reverse()

        if category in all_time_categories:
            avg = 0
            topsters = category_rankings[0:10]
            
            for player in topsters:
                avg += player[1]

            topster_averages.append([category, round(avg / 10, 2)])

        for i in range(len(category_rankings)):
            name = category_rankings[i][0]
            value = category_rankings[i][1]
            ranks[name][category] = i + 1

    for category in categories:
        rank(category)

    league_grade = 0
    for t in topster_averages:
        if t[0] in ["PTS", "AST"]:
            league_grade += t[1] / 2
        else:
            league_grade += t[1] * 10

    league_grade = round((league_grade / len(all_time_categories)) * 11, 2)

    for player in ranks:
        score = 0
        for category in ranks[player]:
            score += ranks[player][category]

        # divide total score by all categories used    
        player_grade = score / len(categories)

        # divide by all players then multiply by 100
        player_grade = (player_grade / len(list(stats))) * 100

        # divide score by league grade times 2
        player_grade = player_grade / (league_grade * 2)

        # subtract from 100
        player_grade = 100 - (player_grade * 100)
        player_grade += (5 * (league_grade/100))
        player_grade -= (2.5 - (league_grade/100))
        
        # player_grade = 100 - ((player_grade / league_grade) * )

        ranks[player]["grade"] = round(player_grade, 2)
        ranks[player]["name"] = player.replace("*", "")
        ranks[player]["league_grade"] = league_grade
        ranks[player]["year"] = year
        ranks[player]["games_played"] = int(stats[player]["G"])
        ranks[player]["team"] = stats[player]["Tm"] 

    with open(f"{folder}{file_name}.json", "w+", encoding="utf8") as file:
        file.write(json.dumps(ranks, ensure_ascii=False, indent =4))


if __name__ == "__main__":
    GOAT_GRADE(2023)
