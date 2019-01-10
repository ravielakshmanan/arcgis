import os
from flask import Flask, render_template, redirect, request, url_for
from google.cloud import storage

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './noah_credentials.json'
os.environ["CLOUD_STORAGE_BUCKET"] = 'magicgrant.appspot.com'

file_name = 'static/iri_data.csv'

@app.route('/')
def load_home():
	return render_template("index.html")

@app.route('/render_map')
def render_map():

	if not os.path.exists(file_name):
		gcs = storage.Client()
		bucket = gcs.get_bucket(os.environ["CLOUD_STORAGE_BUCKET"])

		blob = bucket.blob('iri_dataset.csv')
		blob.download_to_filename(file_name)

	return render_template("mapbox.html")

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=8080, debug=True)
   # app.run(host='0.0.0.0', port=8080, debug=True)