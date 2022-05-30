from datetime import datetime
from collections import defaultdict
from get_api_response import get_json_response


def convert_timestamp(data: int) -> str:  # format timestamp - d-m-y H:M:S f.e. (28-05-22 02:23:03)
    return datetime.fromtimestamp(data).strftime("%d-%m-%y %H:%M:%S")


def get_24hr_change(r: dict, crypto_name: str, in_fiat: str) -> float:  # f.e. 5.234321 -> 5.23
    return round(r[crypto_name][f"{in_fiat}_24h_change"], 2)


def get_last_update(r: dict, crypto_name: str) -> str:  # get formatted date of the last update
    return convert_timestamp(r[crypto_name]["last_updated_at"])


def convert_response_to_relevant_dict(mode: int, crypto_name=None, in_fiat=None) -> dict:
    r = get_json_response(crypto_name, in_fiat)  # get API response
    crypto_dict = defaultdict(dict)  # get a new dict with shortened "crypto" name -> bitcoin => btc etc.
    if mode == 1:
        btc, eth, usd = "bitcoin", "ethereum", "usd"
        r[btc][f"{usd}_24h_change"], r[eth][f"{usd}_24h_change"] = get_24hr_change(r, btc, usd), get_24hr_change(r, eth, usd)

        r[btc]["last_updated_at"], r[eth]["last_updated_at"] = get_last_update(r, btc), get_last_update(r, eth)

        crypto_dict["btc"], crypto_dict["eth"] = r[btc], r[eth]

        return dict(crypto_dict)
    elif mode == 2:
        r[crypto_name][f"{in_fiat}_24h_change"] = get_24hr_change(r, crypto_name, in_fiat)

        r[crypto_name]["last_updated_at"] = get_last_update(r, crypto_name)

        crypto_dict[crypto_name] = r[crypto_name]

        return dict(crypto_dict)


def get_relevant_data(mode: int, crypto_name=None, in_fiat=None) -> str:
    """TODO add a feature that will enable users to see how much crypto they can buy for a particular amount of money"""
    if mode == 1:  # daily tweet
        converted = convert_response_to_relevant_dict(1, "bitcoin,ethereum", "usd")

        btc, eth, usd = "btc", "eth", "usd"
        btc_change, eth_change = converted[btc][f'{usd}_24h_change'], converted[eth][f'{usd}_24h_change']
        if btc_change < 0:
            btc_change = f"🔻24hr ➡️ {btc_change}"
        else:
            btc_change = f"🔺24hr ➡️ {btc_change}"

        if eth_change < 0:
            eth_change = f"🔻24hr ➡️ ️{eth_change}"
        else:
            eth_change = f"🔺24hr ➡️ ️{eth_change}"

        msg = f"BTC price at {converted[btc]['last_updated_at']}: {converted[btc][usd]} {btc_change}\n\n"
        msg += f"ETH price at {converted[eth]['last_updated_at']}: {converted[eth][usd]} {eth_change}"

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
print(get_relevant_data(2, "dogecoin", "usd"))  # test mode 2
