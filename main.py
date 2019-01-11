import os
from flask import Flask, render_template, redirect, request, url_for
from google.cloud import storage

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './noah_credentials.json'
os.environ["CLOUD_STORAGE_BUCKET"] = 'water-noah.appspot.com'

# data_dictionary = 'data_dictionary.json'
data_dictionary = 'test.json'

def get_gc_iri_data():
    gcs = storage.Client()
    bucket = gcs.get_bucket(os.environ["CLOUD_STORAGE_BUCKET"])

    blob = bucket.get_blob(data_dictionary)
    downloaded_blob = blob.download_as_string().decode("utf-8")

    return downloaded_blob

def find_closest_location(lat, lng):
	# Function to get the closest coordinates
	blob = get_gc_iri_data()


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

    data = find_closest_location(lat, lng);

    return blob

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=8080, debug=True)
   # app.run(host='0.0.0.0', port=8080, debug=True)