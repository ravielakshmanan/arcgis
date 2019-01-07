import os
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

@app.route('/')
def load_home():
	return render_template("index.html")

@app.route('/render_map')
def render_map():
	return render_template("mapbox.html")

if __name__ == '__main__':
   app.run(host='127.0.0.1', port=8080, debug=True)
   # app.run(host='0.0.0.0', port=8080, debug=True)