import time

import requests

import env


def get_latlng(road_address, place_name):
    try:
        lat, lng = get_latlng_with_kakao(road_address, place_name)
        if lat and lng:
            return lat, lng
    except:
        pass
    try:
        lat, lng = get_lanlng_with_google(road_address)
        if lat and lng:
            return lat, lng
    except:
        pass
    print('주소를 찾지 못했습니다. 수동으로 넣어주세요.')
    return None, None


def get_latlng_with_kakao_by_name(place_name):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=%s' % place_name
    headers = {'Authorization': 'KakaoAK %s' % env.KAKAO_API_KEY}
    cnt = 0
    address_data = None
    while not cnt > 3:
        try:
            address_data = requests.get(url, headers=headers).json()
            time.sleep(0.5)
            break
        except Exception as e:
            print(e)
            cnt += 1
            continue
    if address_data is None or not len(address_data['documents']):
        print('[Kakao] 가게 이름를 찾지 못했습니다. 이름: [%s]' % place_name)
        return None, None
    if len(address_data['documents']) != 1:
        for document in address_data['documents']:
            if document['place_name'] == place_name:
                return document['y'], document['x']
        return None, None
    document = address_data['documents'][0]
    return document['y'], document['x']


def get_latlng_with_kakao_by_road_address(road_address, place_name):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query=%s' % road_address
    headers = {'Authorization': 'KakaoAK %s' % env.KAKAO_API_KEY}
    cnt = 0
    address_data = None
    while not cnt > 3:
        try:
            address_data = requests.get(url, headers=headers).json()
            time.sleep(0.5)
            break
        except Exception as e:
            print(e)
            cnt += 1
            continue
    if address_data is None or not len(address_data['documents']):
        print('[Kakao] 주소를 찾지 못했습니다. 주소: [%s]' % road_address)
        return None, None
    for document in address_data['documents']:
        if document['place_name'] == place_name:
            return document['y'], document['x']
    result = address_data['documents'][0]
    return result['y'], result['x']


def get_latlng_with_kakao(road_address, place_name):
    lat, lng = get_latlng_with_kakao_by_name(place_name)
    if lat and lng:
        return lat, lng
    return get_latlng_with_kakao_by_road_address(road_address, place_name)


def get_lanlng_with_google(road_address):
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
        print('[Google] 주소를 찾지 못했습니다. 주소: [%s]' % road_address)
        return None, None

    lat = round(float(address_data['results'][0]['geometry']['location']['lat']), 6)
    lng = round(float(address_data['results'][0]['geometry']['location']['lng']), 6)
    return lat, lng
