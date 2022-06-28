# import requests
# url = 'https://maps.googleapis.com/maps/api/geocode/json'
# params = {'sensor': 'false', 'ADDRESS': 'Peru, Av Santa Elvira 6198'}
# r = requests.get(url, params=params)
# print(r.content)
# results = r.json()['results']
# location = results[0]['geometry']['location']
# print(location['lat'], location['lng'])
# # (37.3860517, -122.0838511)
# from dotenv import load_dotenv
# load_dotenv()
import os

# import googlemaps
import geocoder

ADDRESS = 'Peru, Av Santa Elvira 6198'
g = geocoder.osm(ADDRESS)
# print(g.osm)
# print(g.json)
print(g.latlng)

h = geocoder.arcgis(ADDRESS)
# print(h.json)
print(h.latlng)
# https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com?project=project-id-turnkey-tribute-197809
# https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com?project=project-id-newagent-9enr
# https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com?project=project-id-turnkey-tribute-197809
# https://www.bingmapsportal.com/Announcement
# https://www.bing.com/maps
# https://github.com/DenisCarriere/geocoder

# http://spatial.virtualearth.net/REST/v1/dataflows/listjobs?key=Apk_Ia23b0ieh8DBhryeNWDutidw78njhx6t390_yj-Sma8ioncr6vEUJYXGfQhX&output=json
# t = geocoder.google('Peru, Av Santa Elvira 6198')
t = geocoder.google(ADDRESS, key=os.getenv('GOOGLE_API_KEY'))
# print(t.geojson)
print(t.latlng)
# print(t.json)
# print(t.current_result)
# print(t.error)
# print(t.url)


e = geocoder.bing(ADDRESS, key=os.getenv('BING_KEY'))
# print(e.json)
print(e.latlng)
