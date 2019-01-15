import os
from flask import Flask, render_template, redirect, request, url_for
from google.cloud import storage
import datetime, json
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './noah_credentials.json'
collection_name = "precipitation_data"
# collection_name = "precipitation_test"

def process_data(doc_ref):
    docs = doc_ref.get()
    data_dict = []
    for doc in docs:
        data_dict.append(doc.to_dict())
    print("The size of the collection is: " + str(len(data_dict)))
    return data_dict

def get_processed_data(dict):
    processed_data_dict = {}
    
    for row in dict:
        coords = "(" + row['Longitude'] + ", " + row['Latitude'] + ")"
        anomaly = row['Precipitation Anomaly']
        date = row['Time'][8:]
        if coords not in processed_data_dict:
            processed_data_dict[coords] = {"dates":[date], "data":[anomaly]}
        else:
            value = processed_data_dict[coords]
            dates_list = value["dates"].append(date)
            data_list = value["data"].append(anomaly)
            processed_data_dict[coords] = {"dates":dates_list, "data":data_list}

    return processed_data_dict


def get_iri_data_from_store(store):
    doc_ref = store.collection(collection_name)
    data_dict = process_data(doc_ref)
    processed_data_dict = get_processed_data(data_dict)
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

    if (not len(firebase_admin._apps)):
        cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        firebase_admin.initialize_app(cred)

        db = firestore.client()
        processed_data_dict = get_iri_data_from_store(db)

    key = '(' + lng + lngSign + ', ' + lat + latSign + ')'
    print("The coordinates passed are: " + key)
    if key in processed_data_dict:
        return str(processed_data_dict[key])
    
    print("No match found!")    
    return "-1"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)