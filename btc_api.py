import json

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


def get_btc_api():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'id': '1',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'd61bca4c-e9d3-40b9-8d82-abf9b057ffbd',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        json_data = json.loads(response.text)
        return {'created_at': json_data['status']['timestamp'],
                'usd_price': json_data['data']['1']['quote']['USD']['price'],
                'volume_24h': json_data['data']['1']['quote']['USD']['volume_24h']}
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
