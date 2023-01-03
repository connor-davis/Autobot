import requests

URL = "http://maps.googleapis.com/maps/api/geocode/json"
location = "delhi technological university"
PARAMS = {}

r = requests.get(url=URL, params=PARAMS)

data = r.json()