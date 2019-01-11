import os
from flask import Flask, render_template, redirect, request, url_for
from google.cloud import storage
import datetime, json
from pathlib import Path

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './noah_credentials.json'
################################################################
#TODO: REMOVE '/' IF DOWNLOAD FILE DOES NOT WORK
os.environ["CLOUD_STORAGE_BUCKET"] = '/water-noah.appspot.com'
################################################################

data_dictionary = 'data_dictionary.json'
flag = ""
# data_dictionary = 'test.json'

def get_gc_iri_data():
    gcs = storage.Client()
    bucket = gcs.get_bucket(os.environ["CLOUD_STORAGE_BUCKET"])

    blob = bucket.get_blob(data_dictionary)
    blob.download_to_filename(data_dictionary)

    ############################################################
    #TODO: UNCOMMENT BELOW IF DOWNLOAD OF FILE DOES NOT WORK
    # downloaded_blob = blob.download_as_string().decode("utf-8")
    # print(type(downloaded_blob))
    # data = json.loads(downloaded_blob)
    # print(type(data))
    # return data
    ############################################################

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

    #############################################################
    #TODO: COMMENT BELOW IF DOWNLOAD OF FILE DOES NOT WORK
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
    #############################################################

    #############################################################
    #TODO: UNCOMMENT IF DOWNLOAD OF FILE DOES NOT WORK
    # if flag == "":
    #     print(datetime.datetime.now())
    #     json_data = get_gc_iri_data()
    #     print(datetime.datetime.now())
    # flag = "done"
    # key = '(' + lng + lngSign + ', ' + lat + latSign + ')'
    # print(key)
    # if key in json_data:
    #     return str(json_data[key])
    #############################################################

    return "-1"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=True)



# the format is (long,lat): {"dates":[], "data":[]}