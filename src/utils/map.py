import time

import requests

import env


def get_latlng_by_address(road_address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (road_address, env.GOOGLE_MAP_KEY)
    print(road_address)
    cnt = 0
    address_data = None
    while not cnt > 3:
        try:
            address_data = requests.get(url).json()
            time.sleep(0.5)
            break
        except Exception as e:
            print(e)
            cnt += 1
            continue
    if address_data is None or not len(address_data['results']):
        print('주소를 찾지 못했습니다. 수동으로 넣어주세요. 주소: [%s]' % road_address)
        return None, None

    lat = round(float(address_data['results'][0]['geometry']['location']['lat']), 6)
    lng = round(float(address_data['results'][0]['geometry']['location']['lng']), 6)
    return lat, lng
