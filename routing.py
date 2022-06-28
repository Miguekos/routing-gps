import os
import geocoder
import haversine as hs

def marcar_distancia():
    # set the coordinates / geocodes
    location_delhi = (28.7041, 77.1025)
    location_bangalore = (12.9716, 77.5946)

    # calculate the distance
    h_distance = hs.haversine(location_delhi, location_bangalore)

    # Print the result with a message
    print('The distance between Delhi and Bangalore is -', round(h_distance, 2), 'km')


marcar_distancia()

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
