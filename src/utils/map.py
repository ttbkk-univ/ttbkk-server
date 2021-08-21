import requests

import env


def get_latlng_by_address(road_address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (road_address, env.GOOGLE_MAP_KEY)
    print(url)
    address_data = requests.get(url).json()
    if not len(address_data['results']):
        return None
    lat = round(float(address_data['results'][0]['geometry']['location']['lat']), 6)
    lng = round(float(address_data['results'][0]['geometry']['location']['lng']), 6)
    return lat, lng
