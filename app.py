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

    text = """
        Welcome to Goat Grade
        enter year in url
        Example: /season/2023
        an <a href="https://asboyer.com" target="_blank">@asboyer</a> production
        """

    return text.strip()

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
        update = False
        # last_day = int(open("last_update.txt", "r").readlines()[0])
        
        in_season = current_month in NBA_SEASON
        current_year_og = current_month in [10, 11, 12] and current_year + 1 == year
        current_year_alt = current_month in [1, 2, 3, 4, 5, 6] and current_year == year

        if in_season and (current_year_og or current_year_alt): 
            update = True
            # f = open("last_update.txt", "w")
            # f.write(current_day + "\n" + today.strftime("%b %d %Y %H:%M:%S"))

        elif not os.path.exists(f'stats/raw_stats{year}.json'):
            update = True
        
        GOAT_GRADE(year, update=update, folder="grades/", file_name=f"gg_{str(year)}")  


    except TypeError:
        return f"{year} is not a valid season!"

    return render_template("goat.html", year=year)

@app.route("/data/<name>")
def data(name):
    if os.path.exists(f'grades/{name}'):
        f = open(f'grades/{name}')
        data = json.load(f)
        return data
        