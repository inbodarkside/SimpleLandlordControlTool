import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')


@app.errorhandler(Exception)
def handle_error(e):
    return render_template('500.html')


@app.route('/', methods=['GET'])
@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        landid = request.form['landid']
        dateend = datetime.today()
        datestart = dateend - timedelta(6)
        r = requests.get(
            'https://api-lok-live.leagueofkingdoms.com/api/stat/land/contribution?landId=' + landid + '&from=' + datestart.strftime(
                "%Y-%m-%d") + '&to=' + dateend.strftime("%Y-%m-%d"))
        data = r.json()
        return render_template("output.html", text=data['contribution'], owner=data['owner'],
                               datestart=datestart.strftime(
                                   "%Y-%m-%d"), dateend=dateend.strftime("%Y-%m-%d"))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug =True)
