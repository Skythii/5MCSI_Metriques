from flask import Flask, render_template_string, render_template, jsonify 
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

from flask import Flask, render_template

@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def show_commits_chart():
    return render_template("commits.html")

@app.route('/api/commits-per-minute/')
def commits_per_minute():
    url = 'https://api.github.com/repos/Skythii/5MCSI_Metriques/commits'
    response = requests.get(url)
    data = response.json()

    minutes = []
    for commit in data:
        try:
            date_str = commit['commit']['author']['date']
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes.append(dt.minute)
        except Exception as e:
            continue

    count_by_minute = Counter(minutes)
    # On transforme les résultats pour Google Charts
    chart_data = [['Minute', 'Commits']]
    for minute in sorted(count_by_minute):
        chart_data.append([str(minute), count_by_minute[minute]])

    return jsonify(chart_data)

if __name__ == "__main__":
  app.run(debug=True)
