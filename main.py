import os
import sqlalchemy
import logging
from flask import Flask, render_template, redirect, request, url_for
import datetime, json
from collections import defaultdict

app = Flask(__name__)

logger = logging.getLogger()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './mysql_credentials.json'
os.environ["CLOUD_SQL_CONNECTION_NAME"] ='noah-water:us-east4:precipitation'
os.environ["DB_USER"] = 'root'
os.environ["DB_PASS"] = 'y3hsG5O7cDCPv00B'
os.environ["DB_NAME"] = 'prec_anomaly'

# Manage SQL connection pool
db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        database=os.environ["DB_NAME"],
        query={
            'unix_socket': '/cloudsql/{}'.format(os.environ["CLOUD_SQL_CONNECTION_NAME"])
        }
    ),
    pool_size=10,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
)

def get_processed_data(data):
  processed_data_dict = defaultdict(list)
  
  iri_data_list = []
  for lat, long, anomaly, date in data:
    date = date.replace('\r', '')
    coords = "(" + long + ", " + lat + ")"
    anomaly = anomaly
    date = date[8:]
    data_tuple = (coords, anomaly, date)
    iri_data_list.append(data_tuple)

  print("The size of the data list: " + str(len(iri_data_list)))

  for coords, anomaly, date in iri_data_list:
    if coords not in processed_data_dict:
        temp_dict = {'dates': [date], 'data': [anomaly]}
        processed_data_dict[coords] = temp_dict
    else:
        processed_data_dict[coords]['dates'].append(date)
        processed_data_dict[coords]['data'].append(anomaly)

  return processed_data_dict

def get_iri_data_from_gcloud(long, lat):
    
    query = "SELECT * FROM precipitation where latitude = '" + lat + "' AND longitude = '" + long + "'"
    print("About to execute query: " + query)

    with db.connect() as conn:
        anomaly_data = conn.execute(query).fetchall()

        print("The size of data returned: " + str(len(anomaly_data)))

        processed_data_dict = get_processed_data(anomaly_data)

    return processed_data_dict

@app.route('/')
def load_home():
    return render_template("index.html")

@app.route('/render_map')
def render_map():
    return render_template("render_map.html")


@app.route('/onclick', methods=['GET', 'POST'])
def open_dataviz():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    latSign = request.args.get('latSign')
    lngSign = request.args.get('lngSign')

    iri_data = get_iri_data_from_gcloud(lng + lngSign, lat + latSign)

    key = '(' + lng + lngSign + ', ' + lat + latSign + ')'
    print("The coordinates passed are: " + key)
    if key in iri_data:
        return str(iri_data[key])
    
    print("No match found!")    
    return "-1"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)