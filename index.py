from flask import Flask, request, jsonify, render_template
import tweepy
import json
from passwords import TKEY, TSECRET, TTOKEN, TASECRET

ckey = TKEY
csecret = TSECRET
atoken = TTOKEN
asecret = TASECRET

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)

app = Flask(__name__)

emerg = ['fire', 'help', 'earthquake', 'house', 'world', 'street', 'evacuation', \
	'hit', 'shaking', 'aftershock', 'safe', 'disaster', 'evacuate', 'evacuated' \
	'tsunami', 'flood', 'flooding', 'volcano', 'eruption', 'massive', 'killed', \
	'dead', 'people running', 'damage', 'damaged', 'destroyed']

geos = [ [ 30.16064, -97.76967 ], [ 30.16465073, -97.44488504 ], [ 30.20226566, -97.66722505 ], [ 30.240064, -97.716409 ], [ 30.13382, -97.6414099 ], [ 30.144502, -96.39806 ] ]

@app.route('/_map', methods=['POST', 'GET'])
def map():
	lat = request.args.get("lat", '')
	long = request.args.get("long", '')
	#results =  api.search(geocode = lat+","+long+",50km",count=100)
	
	for status in tweepy.Cursor(api.search, geocode="30,-97,50km", count=100).items():
		for word in emerg:
			if " " + word + " " in status.text:
				if status.geo:
					geos.append(status.geo['coordinates'])
					print(geos)
					break

	return render_template('out.html')


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html')


@app.route('/out/')
def out():	
	return render_template('out.html') 


@app.route('/out/geodata')
def geodata():
	return jsonify(geos)
