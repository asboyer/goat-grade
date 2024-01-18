from flask import Flask, render_template
from goat_grade import GOAT_GRADE, NBA_SEASON
from datetime import datetime
import os, json

app = Flask(__name__)
root = os.path.dirname(__file__)

today = datetime.today()
current_year = today.year
current_month = today.month
current_day = today.day


# MAP OUT THIS WHOLE APP
# PERFECT ALGORITHM / RANKING
# MAKE ALL TIME RANKING
# ADD TEAM STATS
# WORK ON DISPLAY

@app.route("/")
def index():
    text = """
        <span style="font-family: monospace">
        Welcome to Goat Grade!
        <br>
        <br>
        enter year in url
        <br>
        Example: /season/2023
        <br>
        <br>
        """
    curr = f'<a href="/season/{str(current_year)}">current season</a>'    
    text_2 = """
        <br>
        <br>
        <a href="/all_time">all time</a> rankings (work in progress)
        <br>
        <br>
        an <a href="https://asboyer.com" target="_blank">@asboyer</a> production
        </span>
        """

    text = text + curr + text_2

    return text.strip()

# all time seasons
@app.route("/all_time")
def all():
    return open(os.path.join(root, 'r.txt'), 'r').read()

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
        last_day = int(open(os.path.join(root, "last_update.txt"), "r").readlines()[0])
        
        in_season = current_month in NBA_SEASON
        current_year_og = current_month in [10, 11, 12] and current_year + 1 == year
        current_year_alt = current_month in [1, 2, 3, 4, 5, 6] and current_year == year

        if in_season and (current_year_og or current_year_alt) and last_day != current_day: 
            print("Update stats!")
            f = open(os.path.join(root, "last_update.txt"), "w")
            f.write(str(current_day) + "\n" + today.strftime("%b %d %Y %H:%M:%S"))
            update = True

        elif not os.path.exists(os.path.join(root, f'stats/raw_stats{year}.json')):
            print("Update stats!!")
            update = True
        
        GOAT_GRADE(year, update=update, folder=os.path.join(root, 'grades/'), file_name=f"gg_{str(year)}")  

    except TypeError:
        return f"{year} is not a valid season!"

    return render_template("goat.html", year=year)

@app.route("/data/<name>")
def data(name):
    if os.path.exists(os.path.join(root, f'grades/{name}')):
        f = open(os.path.join(root, f'grades/{name}'))
        data = json.load(f)
        return data
