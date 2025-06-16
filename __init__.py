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

@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')

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
def monhistogramme():
    return render_template("histogramme.html")

@app.route('/commits/')
def commits():
    return render_template('commits.html')

@app.route('/api/commits/minutes')
def get_commit_minutes():
    url = "https://api.github.com/repos/aboubakar97/5MCSI_Metriques/commits"
    response = requests.get(url)
    data = response.json()

    minutes_list = []

    for commit in data:
        try:
            date_str = commit['commit']['author']['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes_list.append(date_obj.minute)
        except Exception as e:
            continue

    # Compter combien de commits ont été faits à chaque minute (0-59)
    commit_counts = Counter(minutes_list)
    commit_data = [{"minute": m, "count": commit_counts[m]} for m in range(60)]

    return jsonify(commit_data)
  
if __name__ == "__main__":
  app.run(debug=True)
