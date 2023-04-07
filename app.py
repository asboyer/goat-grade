from flask import Flask, render_template
from goat_grade import GOAT_GRADE, NBA_SEASON
from datetime import datetime
import os, json

app = Flask(__name__)

today = datetime.today()
current_year = today.year
current_month = today.month
current_day = today.day

@app.route("/")
def index():
    return "enter year in url\nExample: /season/2023"

@app.route("/season/<name>")
def season(name):
    try: 
        year = int(name)
    except:
        if name == "all":
            return "coming soon"
        else:
            return "Invalid url!" 

    try:
        # last_day = int(open("last_update.txt", "r").readlines()[0])
        if (current_month in NBA_SEASON) and ((current_month in [10, 11, 12] and current_year + 1 == year) or (current_month in [1, 2, 3, 4, 5, 6] and current_year == year)):
            GOAT_GRADE(year, folder="goat_grade/", file_name=f"gg_{str(year)}")  
            # f = open("last_update.txt", "w")
            # f.write(current_day + "\n" + today.strftime("%b %d %Y %H:%M:%S"))
        elif not os.path.exists(f'goat_grade/gg_{year}.json'):
            GOAT_GRADE(year, folder="goat_grade/", file_name=f"gg_{str(year)}")  

    except TypeError:
        return f"{year} is not a valid season!"

    return render_template("goat.html", year=year)



@app.route("/data/<name>")
def data(name):
    if os.path.exists(f'goat_grade/{name}'):
        f = open(f'goat_grade/{name}')
        data = json.load(f)
        return data