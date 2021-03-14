import json

def rank(stats, category, rankings):
	rank = []
	for player in stats:
		rank.append([player, float(stats[player][category])])
	rank = sorted(rank, key=lambda x: x[1])
	rank.reverse()

	add_to_dict(rank, rankings, category)

def add_to_dict(rank, rankings, category):
	for i in range(len(rank)):
		name = rank[i][0]
		value = rank[i][1]
		rankings[name] = {}
		rankings[name][f'{category} Rank'] = i
		rankings[name][category] = value

def make_dict(stats):
	rankings = {}
	for player in stats:
		rankings[player] = {}

	return rankings

def print_rank(rankings, category):
	for player in rankings:
		print(f"{rankings[player][f'{category} Rank'] + 1}. {player} ({rankings[player][category]})")

with open('../stats/stats.json', 'r', encoding='utf8') as file:
	stats = json.load(file)
	ranks = make_dict(stats)
	# rankings = {}
	# point_rank = rank(stats, 'PTS') 

	print(ranks)

	# print_rank(rankings, 'PTS')
