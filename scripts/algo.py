import json

def rank(stats, category):
	rank = []
	for player in stats:
		rank.append([player, float(stats[player][category])])
	rank = sorted(rank, key=lambda x: x[1])
	rank.reverse()

	return rank

def print_rank(rankings, category):
	for player in rankings:
		print(f"{rankings[player][f'{category} Rank'] + 1}. {player} ({rankings[player][cateogry]})")

with open('../stats/stats.json', 'r', encoding='utf8') as file:
	stats = json.load(file)
	rankings = {}
	point_rank = rank(stats, 'PTS') 

	for i in range(len(point_rank)):
		name = point_rank[i][0]
		points = point_rank[i][1]
		rankings[name] = {}
		rankings[name]['PTS Rank'] = i
		rankings[name]['PTS'] = points

	print_rank(rankings, 'PTS')
