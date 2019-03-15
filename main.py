import os
import sqlalchemy
import logging
from flask import Flask, render_template, redirect, request, url_for
import datetime, json
from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter

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

def get_processed_trend_data(trends):
    processed_data_dict = defaultdict(list)
    trends = sorted(trends,key=itemgetter(0))

    iri_data_list = []
    for date, long, lat, prec, smoothed, trend in trends:
        date = date.replace('\r', '')
        coords = "(" + long + ", " + lat + ")"
        data_tuple = (coords, prec, smoothed, trend, date)
        iri_data_list.append(data_tuple)

    print("The size of the data list: " + str(len(iri_data_list)))

    for coords, prec, smoothed, trend, date in iri_data_list:
        if coords not in processed_data_dict:
            temp_dict = {'dates': [date], 'prec': [prec], 'smoothed': [smoothed], 'trend': [trend]}
            processed_data_dict[coords] = temp_dict
        else:
            processed_data_dict[coords]['dates'].append(date)
            processed_data_dict[coords]['prec'].append(prec)
            processed_data_dict[coords]['smoothed'].append(smoothed)
            processed_data_dict[coords]['trend'].append(trend)

    sorted_dict = OrderedDict(sorted(processed_data_dict.items(), key=lambda t: t[0]))

    return sorted_dict 

def get_processed_data(data):
    processed_data_dict = defaultdict(list)
    data = sorted(data,key=itemgetter(0))

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

    sorted_dict = OrderedDict(sorted(processed_data_dict.items(), key=lambda t: t[0]))

    return sorted_dict

def get_iri_data_from_gcloud(long, lat, longT, latT):
    
    query = "SELECT * FROM precipitation where latitude = '" + lat + "' AND longitude = '" + long + "'"
    print("About to execute query: " + query)

    # trend_query = "SELECT * FROM precipitation_trend where latitude = '25.575N' AND longitude = '91.85E' and time_range in ('Jul-Sep 1981','Jul-Sep 1982','Jul-Sep 1983','Jul-Sep 1984','Jul-Sep 1985','Jul-Sep 1986','Jul-Sep 1987','Jul-Sep 1988','Jul-Sep 1989','Jul-Sep 1990','Jul-Sep 1991','Jul-Sep 1992','Jul-Sep 1993','Jul-Sep 1994','Jul-Sep 1995','Jul-Sep 1996','Jul-Sep 1997','Jul-Sep 1998','Jul-Sep 1999','Jul-Sep 2000','Jul-Sep 2001','Jul-Sep 2002','Jul-Sep 2003','Jul-Sep 2004','Jul-Sep 2005','Jul-Sep 2006','Jul-Sep 2007','Jul-Sep 2008','Jul-Sep 2009','Jul-Sep 2010','Jul-Sep 2011','Jul-Sep 2012','Jul-Sep 2013','Jul-Sep 2014','Jul-Sep 2015','Jul-Sep 2016','Jul-Sep 2017','Jul-Sep 2018')"
    trend_query = "SELECT * FROM precipitation_trend where latitude = '" + latT + "' AND longitude = '" + longT + "' and time_range in ('Jul-Sep 1981','Jul-Sep 1982','Jul-Sep 1983','Jul-Sep 1984','Jul-Sep 1985','Jul-Sep 1986','Jul-Sep 1987','Jul-Sep 1988','Jul-Sep 1989','Jul-Sep 1990','Jul-Sep 1991','Jul-Sep 1992','Jul-Sep 1993','Jul-Sep 1994','Jul-Sep 1995','Jul-Sep 1996','Jul-Sep 1997','Jul-Sep 1998','Jul-Sep 1999','Jul-Sep 2000','Jul-Sep 2001','Jul-Sep 2002','Jul-Sep 2003','Jul-Sep 2004','Jul-Sep 2005','Jul-Sep 2006','Jul-Sep 2007','Jul-Sep 2008','Jul-Sep 2009','Jul-Sep 2010','Jul-Sep 2011','Jul-Sep 2012','Jul-Sep 2013','Jul-Sep 2014','Jul-Sep 2015','Jul-Sep 2016','Jul-Sep 2017','Jul-Sep 2018')"
    print("About to execute query: " + trend_query)

    with db.connect() as conn:
        anomaly_data = conn.execute(query).fetchall()
        trend_data = conn.execute(trend_query).fetchall()

        print("The size of anomaly data returned: " + str(len(anomaly_data)))
        print("The size of trend data returned: " + str(len(trend_data)))

        processed_data_dict = get_processed_data(anomaly_data)
        processed_trend_dict = get_processed_trend_data(trend_data)

    return processed_data_dict, processed_trend_dict

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
    latT = request.args.get('latT')
    lngT = request.args.get('lngT')
    latSign = request.args.get('latSign')
    lngSign = request.args.get('lngSign')

    iri_data, trend_data = get_iri_data_from_gcloud(lng + lngSign, lat + latSign, lngT + lngSign, latT + latSign)

    key = '(' + lng + lngSign + ', ' + lat + latSign + ')'
    keyT = '(' + lngT + lngSign + ', ' + latT + latSign + ')'
    print("The coordinates passed are: " + key)
    print("The coordinates passed for Trends are: " + keyT)
    
    # if (key in iri_data) AND (key in trend_data):
    if key in iri_data:
        iri_str = str(iri_data[key])
        # keyT = '(91.95E, 25.575N)'
        if keyT in trend_data:
            trend_str = str(trend_data[keyT])
        else:
            trend_str = ""
        viz_data = iri_str + "_" + trend_str
        return str(viz_data)
    
    print("No match found!")    
    return "-1"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)