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
		rankings[name][f'{category} Rank'] = i
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
		print(f"{player[1] + 1}. {player[0]} ({player[2]})")

def total(rankings):
	pass


with open('../stats/stats.json', 'r', encoding='utf8') as file:
	stats = json.load(file)
	ranks = make_dict(stats)
	rank(stats, 'PTS', ranks)
	rank(stats, 'AST', ranks)
	print(ranks)