# -*- coding: utf-8 -*-
import json
import urllib
import math
import pymysql
import time
import requests

developer_key = 'GIFBZ-V3XAP-Q7VDO-L5TYS-DOJX3-VTBK4' # 这里为你申请的开发者key


def address_to_coordinate(address):
    """
    通过地址获取经纬度
    :param address:
    :return:
    """
    base = "http://apis.map.qq.com/ws/geocoder/v1/?address={}&key={}".format(address, developer_key)  # 地址解析，地址转坐标
    response = requests.get(base)
    answer = response.json()
    print(answer)
    if (answer['status'] == 0):
        data = {
            'lng': answer['result']['location']["lng"],  # 经度
            'lat': answer['result']['location']["lat"]  # 纬度
        }
    else:
        data = {
            'lng': ' ',
            'lat': ' '
        }
    # print(data)
    return data


def _getLocation(lat, lng):
    """
    使用腾讯地图(GCJ02坐标系)
    根据经纬度获取当前地址
    :param lat:
    :param lng:
    :return:
    """
    base = "http://apis.map.qq.com/ws/geocoder/v1/?location={},{}&key={}&get_poi=0".format(lat, lng, developer_key)
    response = requests.get(base)
    answer = response.json()
    print(answer)
    if (answer['status'] == 0):
        address = ''
        recommend = ''
        rough = ''
        if 'result' in answer['result']:
            result = answer['result']
            if 'address' in result:
                address = result["address"]  # 地址
            formatted_addresses = result['formatted_addresses']
            if 'formatted_addresses' in formatted_addresses:
                if 'recommend' in formatted_addresses:
                    recommend = formatted_addresses["recommend"]  # 经过腾讯地图优化过的描述方式，更具人性化特点
                if 'rough' in formatted_addresses:
                    rough = formatted_addresses["rough"]  # 大致位置，可用于对位置的粗略描述

        data = {
            'recommend': recommend,  # 经过腾讯地图优化过的描述方式，更具人性化特点
            'rough': rough,  # 大致位置，可用于对位置的粗略描述
            'address': address  # 地址
        }
    else:
        data = {
            'recommend': '', #经过腾讯地图优化过的描述方式，更具人性化特点
            'rough': '', #大致位置，可用于对位置的粗略描述
            'address': ' '  # 地址
        }

    return data


def _translate(lat, lng, type):
    """
    坐标转换
    :param lat: 纬度
    :param lng: 经度
    :param type: 坐标类型 1 GPS坐标 2 sogou经纬度 3 baidu经纬度 4 mapbar经纬度 5 [默认]腾讯、google、高德坐标 6 sogou墨卡托
    :return:
    """
    base = "https://apis.map.qq.com/ws/coord/v1/translate?locations={},{}&type={}&key={}".format(lat, lng, type, developer_key)
    response = requests.get(base)
    answer = response.json()
    print(answer)
    if (answer['status'] == 0):
        data = {
            'lng': answer['locations'][0]['lng'],  # 经度
            'lat': answer['locations'][0]['lat'] # 纬度
        }
    else:
        data = {
            'lng': 'err',
            'lat': 'err'
        }

    return data


if __name__ == '__main__':
    lng = 116.63322638749825
    lat = 39.85193164177295
    address = "北海公园"
    # type坐标类型 1 GPS坐标 2 sogou经纬度 3 baidu经纬度 4 mapbar经纬度 5 [默认]腾讯、google、高德坐标 6 sogou墨卡托
    _translate(lat,lng,1)
    _getLocation(lat, lng)
    address_to_coordinate(address)