import requests


def get_json_response(crypto=None, in_fiat=None):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": f"{crypto}",
        "vs_currencies": f"{in_fiat}",
        "include_24hr_change": "true",
        "include_last_updated_at": "true"
    }

    response = requests.get(url, params)
    try:
        response = response.json()
    except Exception as e:
        print(e)
    else:
        return response