import os, json

grade_files = os.scandir("grades")

big_data = {}
for g_file in grade_files:
    grades = json.load(open(g_file.path, encoding="utf8"))
    # year = g_file.path.split("_")[-1][0:4]
    # for player in grades.keys():
    #     grades[player]["year"] = year

    # with open(g_file.path, "w+", encoding="utf8") as file:
    #     file.write(json.dumps(grades, ensure_ascii=False, indent =4))
    # if int(g_file.path.split("_")[-1][2:4]) == 59:
    #     continue
    for player in grades.keys():
        print(g_file.path)
        print(player)
        big_data[f'{player.lower().replace(" ", "_")}_{grades[player]["year"]}'] = grades[player]

with open("final.json", "w+", encoding="utf8") as file:
    file.write(json.dumps(big_data, ensure_ascii=False, indent =4))
