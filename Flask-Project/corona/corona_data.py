import requests
import xmltodict
import json
from pprint import pprint

def get_corona_data(startCreateDt, endCreateDt):
    url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson'
    params = {
        'serviceKey' : 'zQPw1nzo5rn90deHgS2r4p2zBuY/HFgTqAOPW4z3BA8qc+3QJSDm2EuKRB1EbiTRpo66deXJHstqYLWWOFtWbg==',
        'pageNo' : '1',
        'numOfRows' : '10',
        'startCreateDt' : startCreateDt,
        'endCreateDt' : endCreateDt,
    }

    res = requests.get(url, params=params)
    dict_data = xmltodict.parse(res.text)
    json_data = json.dumps(dict_data)
    dict_data = json.loads(json_data)

    totalCount = dict_data['response']['body']['totalCount']
    if totalCount == '0':
        return False

    area_data = dict_data['response']['body']['items']['item']
    area_data.reverse()

    return area_data

if __name__ == '__main__':
    print(get_corona_data(20210423, 20210423))
    print(get_corona_data(20210423, 20210423))