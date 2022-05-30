import requests
from datetime import datetime
from collections import defaultdict


def get_json_response(mode, crypto=None, in_fiat=None):
    url = "https://api.coingecko.com/api/v3/simple/price"
    if mode == 1:  # daily tweet
        params = {
            "ids": "bitcoin,ethereum",
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_last_updated_at": "true"
        }

    elif mode == 2:  # responds if mentioned
        params = {
            "ids": f"{crypto}",
            "vs_currencies": f"{in_fiat}",
            "include_24hr_change": "true",
            "include_last_updated_at": "true"
        }

    response = requests.get(url, params)
    try:
        info = response.json()
    except Exception as e:
        print(e)
    else:
        return info


def convert_timestamp(data):
    return datetime.fromtimestamp(data).strftime("%d-%m-%y %H:%M:%S")


def convert_response_to_relevant_dict(r, mode, crypto_name=None, in_fiat=None):  # TODO: turn modes 1 & 2 into 1
    if mode == 1:
        btc_change, eth_change = r["bitcoin"]["usd_24h_change"], r["ethereum"]["usd_24h_change"]
        r["bitcoin"]["usd_24h_change"], r["ethereum"]["usd_24h_change"] = round(btc_change, 2), round(eth_change, 2)

        btc_update, eth_update = r["bitcoin"]["last_updated_at"], r["ethereum"]["last_updated_at"]
        btc_timestamp, eth_timestamp = convert_timestamp(btc_update), convert_timestamp(eth_update)
        r["bitcoin"]["last_updated_at"], r["ethereum"]["last_updated_at"] = btc_timestamp, eth_timestamp

        btc_and_eth = defaultdict(dict)
        btc_and_eth["btc"], btc_and_eth["eth"] = r["bitcoin"], r["ethereum"]

        return dict(btc_and_eth)
    elif mode == 2:
        crypto_change = r[crypto_name][f"{in_fiat}_24h_change"]
        r[crypto_name][f"{in_fiat}_24h_change"] = round(crypto_change, 2)

        crypto_update = r[crypto_name]["last_updated_at"]
        crypto_timestamp = convert_timestamp(crypto_update)
        r[crypto_name]["last_updated_at"] = crypto_timestamp

        crypto = defaultdict(dict)
        crypto[crypto_name] = r[crypto_name]

        return dict(crypto)
    return None


def get_relevant_data(mode, crypto_name=None, in_fiat=None):
    if mode == 1:  # daily tweet
        r = get_json_response(mode)  # response
        converted = convert_response_to_relevant_dict(r, 1)

        btc_change, eth_change = converted['btc']['usd_24h_change'], converted['eth']['usd_24h_change']
        if btc_change < 0:
            btc_change = f"🔻24hr ➡️ {btc_change}"
        else:
            btc_change = f"🔺24hr ➡️ {btc_change}"

        if eth_change < 0:
            eth_change = f"🔻24hr ➡️ ️{eth_change}"
        else:
            eth_change = f"🔺24hr ➡️ ️{eth_change}"

        msg = f"BTC price at {converted['btc']['last_updated_at']}: {converted['btc']['usd']} {btc_change}\n\n"
        msg += f"ETH price at {converted['eth']['last_updated_at']}: {converted['eth']['usd']} {eth_change}"

        return msg

    elif mode == 2:  # responds if mentioned
        r = get_json_response(mode, crypto_name, in_fiat)  # response
        converted = convert_response_to_relevant_dict(r, 2, crypto_name, in_fiat)

        crypto_change = converted[crypto_name][f'{in_fiat}_24h_change']
        if crypto_change < 0:
            change = f"🔻24hr ➡️ {crypto_change}"
        else:
            change = f"🔺24hr ➡️ {crypto_change}"

        msg = f"{crypto_name} price at {converted[crypto_name]['last_updated_at']}: {converted[crypto_name][in_fiat]} {change}\n\n"

        return msg


print(get_relevant_data(1))  # test mode 1
print()
print(get_relevant_data(2, "solana", "usd"))  # test mode 2
