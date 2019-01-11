import os
from flask import Flask, render_template, redirect, request, url_for
from google.cloud import storage
import datetime, json
from pathlib import Path
# import cloudstorage as gcs

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './noah_credentials.json'
os.environ["CLOUD_STORAGE_BUCKET"] = '/water-noah.appspot.com'

data_dictionary = 'data_dictionary.json'
# data_dictionary = 'test.json'

def get_gc_iri_data():
    gcs = storage.Client()
    bucket = gcs.get_bucket(os.environ["CLOUD_STORAGE_BUCKET"])

    blob = bucket.get_blob(data_dictionary)
    blob.download_to_filename(data_dictionary)

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

    # print("Loading data...")

    # filename = os.environ["CLOUD_STORAGE_BUCKET"] + '/' + data_dictionary
    # gcs_file = gcs.open(filename)
    # contents = gcs_file.read()
    # gcs_file.close()
    # print(type(contents))

    myFile = Path(data_dictionary)
    if not myFile.exists():
        print(datetime.datetime.now())
        get_gc_iri_data()
        print(datetime.datetime.now())

    # print("File reading")
    with open(data_dictionary) as f:
        data = json.load(f)
    f.close()
    # print("File read")

    key = '(' + lng + lngSign + ', ' + lat + latSign + ')'
    print(key)
    if key in data:
        return str(data[key])

    return "-1"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)



# the format is (long,lat): {"dates":[], "data":[]}