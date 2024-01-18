import os, json

comb_grades = json.load(open("final.json", encoding="utf8"))

ranks = {}
for player in comb_grades.keys():
    ranks[player] = {}

category_rankings = []
for player in comb_grades.keys():
    category_rankings.append([player, float(comb_grades[player]["grade"])])
category_rankings = sorted(category_rankings, key=lambda x: x[1])
category_rankings.reverse()

with open("r.txt", "w+") as f:
    for item in category_rankings:
        f.write(f"{item[0]} -> <a href=\"/season/{item[0].split('_')[-1]}\">{item[1]}</a><br>\n")
