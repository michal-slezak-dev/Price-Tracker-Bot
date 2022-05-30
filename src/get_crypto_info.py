from datetime import datetime
from collections import defaultdict
from get_api_response import get_json_response


def convert_timestamp(data):
    return datetime.fromtimestamp(data).strftime("%d-%m-%y %H:%M:%S")

def get_24hr_change(r, crypto_name, in_fiat):
    return r[crypto_name][f"{in_fiat}_24h_change"]

def get_last_update(r, crypto_name):
    return r[crypto_name]["last_updated_at"]

def convert_response_to_relevant_dict(mode, crypto_name=None, in_fiat=None):  # TODO: turn modes 1 & 2 into 1
    r = get_json_response(crypto_name, in_fiat)
    if mode == 1:
        btc_change, eth_change = get_24hr_change(r, "bitcoin", "usd"), get_24hr_change(r, "ethereum", "usd")
        r["bitcoin"]["usd_24h_change"], r["ethereum"]["usd_24h_change"] = round(btc_change, 2), round(eth_change, 2)

        btc_update, eth_update = get_last_update(r, "bitcoin"), get_last_update(r, "ethereum")
        btc_timestamp, eth_timestamp = convert_timestamp(btc_update), convert_timestamp(eth_update)
        r["bitcoin"]["last_updated_at"], r["ethereum"]["last_updated_at"] = btc_timestamp, eth_timestamp

        btc_and_eth = defaultdict(dict)
        btc_and_eth["btc"], btc_and_eth["eth"] = r["bitcoin"], r["ethereum"]

        return dict(btc_and_eth)
    elif mode == 2:
        crypto_change = get_24hr_change(r, crypto_name, in_fiat)
        r[crypto_name][f"{in_fiat}_24h_change"] = round(crypto_change, 2)

        crypto_update = get_last_update(r, crypto_name)
        crypto_timestamp = convert_timestamp(crypto_update)
        r[crypto_name]["last_updated_at"] = crypto_timestamp

        crypto = defaultdict(dict)
        crypto[crypto_name] = r[crypto_name]

        return dict(crypto)
    return None


def get_relevant_data(mode, crypto_name=None, in_fiat=None):
    if mode == 1:  # daily tweet
        converted = convert_response_to_relevant_dict(1, "bitcoin,ethereum", "usd")

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
        converted = convert_response_to_relevant_dict(2, crypto_name, in_fiat)

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
