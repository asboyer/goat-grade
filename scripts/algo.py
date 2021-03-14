import json

with open('../stats/stats.json', 'r', encoding='utf8') as file:
	stats = json.load(file)
	rankings = {}
	rank = []
	for player in stats:
		rank.append([player, float(stats[player]['PTS'])])
	rank = sorted(rank, key=lambda x: x[1])
	rank.reverse()

	for i in range(len(rank)):
		name = rank[i][0]
		points = rank[i][1]
		rankings[name] = {}
		rankings[name]['PTS Rank'] = i
		rankings[name]['PTS'] = points
	print(rankings)

	