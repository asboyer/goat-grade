import json 
import pandas as pd

with open('../stats/stats.json', 'r', encoding='utf8') as file:
	data = json.load(file)

df = pd.DataFrame(data)

df.to_excel('../stats/stats.xlsx')