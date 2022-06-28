# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pygeocoder import Geocoder
# loc = Nominatim(user_agent="GetLoc")
# geolocator = Nominatim(user_agent="GetLoc")
# from geopy.distance import geodesic

def print_hi(name):
    results = Geocoder.geocode("Av Sta Elvira 6198")
    print(results[0].coordinates)
    # location = geolocator.geocode("Av Sta Elvira 6198")
    # print(location.address)
    # print((location.latitude, location.longitude))
    # print(location.raw)
    #
    # location2 = geolocator.geocode("peru Av Alfredo Mendiola 3900")
    # print(location2.address)
    # print((location2.latitude, location2.longitude))
    # print(location2.raw)


    # Use a breakpoint in the code line below to debug your script.

    # calle = (location.latitude, location.longitude)
    # catedral = (location2.latitude, location2.longitude)
    # print(geodesic(calle, catedral).kilometers)
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
