import json, os

def rank(stats, category, rankings):
	rank = []
	for player in stats:
		if stats[player][category] != "":
			rank.append([player, float(stats[player][category])])
		else:
			rank.append([player, 0])
	rank = sorted(rank, key=lambda x: x[1])
	rank.reverse()
	add_to_dict(rank, rankings, category)

def add_to_dict(rank, rankings, category):
	total_players = len(rank)
	for i in range(total_players):
		name = rank[i][0]
		value = rank[i][1]
		rankings[name][f'{category} Rank'] = i + 1
		rankings[name][category] = value

def make_dict(stats):
	rankings = {}
	for player in stats:
		rankings[player] = {}

	return rankings

def print_rank(rankings, category):
	order = []
	for player in rankings:
		order.append([player, rankings[player][f'{category} Rank'], rankings[player][category]])
	order = sorted(order, key=lambda x: x[1])
	for player in order:
		print(f"{player[1]}. {player[0]} ({player[2]})")

def total(rankings, categories, file):
	totals = []
	for player in rankings:
		total = []
		total.append(player)
		total.append(0)
		for category in categories:
			total[1] += rankings[player][f'{category} Rank']
		totals.append(total)
	order = []
	order = sorted(totals, key=lambda x: x[1])
	for i in range(len(order)):
		file.write(f"<strong>{i + 1}. {order[i][0]}</strong> <em> (Total: {order[i][1]} [")
		for j in range(len(categories)):
			file.write(f"<strong>{categories[j]}</strong> rank: {rankings[order[i][0]][f'{categories[j]} Rank']}")
			if j != len(categories) - 1:
				file.write(", ")
		file.write("])</em> <br>\n")

with open('../stats/stats.json', 'r', encoding='utf8') as file:
	with open('../stats/advancedstats.json', 'r', encoding='utf8') as file2:
		cats = ['PTS', 'AST', 'TRB', 'FG%', 'FT%', '3P%', 'STL', 'BLK', 'MP', 'PER', 'TS%', 'WS', 'BPM']
		stats = json.load(file)
		advanced_stats = json.load(file2)
		for player in stats:
			stats[player].update(advanced_stats[player])
		ranks = make_dict(stats)
		for cat in cats:
			rank(stats, cat, ranks)
		with open('../templates/index.html', 'w+', encoding='utf8') as text:
			text.write('''
<!DOCTYPE html>
<html>
<head>

<title>Goat Grade</title>
</head>

<body>

Who is the best basketball player in the world? <br>
<br>
<strong>Here are our rankings (based off of rankings in <em> bolded </em> stat categories)</strong>:
<br>
<br>
''')	
		
			total(ranks, cats, text)

			text.write('''</body>
</html>''')