import requests
from decimal import Decimal
from core.exceptions.banxico import ErrorGettingExchangeRateException
from core.helpers.cache import Cache

TOKEN = "3ba2156dd89c00e899cf1527457b73e89b68431f3fc613c0fbd415478e5aa368"


def authenticate():
    return TOKEN


"""
It gets the exchange rate from the Banxico API, caches it for a long time, and returns it
:return: A decimal object with the exchange rate
"""


@Cache.cached(prefix="get_usd_exchange_rate", ttl=1000000)
async def get_exchange_rate():
    url = (
        "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
    )
    params = {"token": authenticate()}
    try:
        result = requests.get(url, params)
        rate = result.json()["bmx"]["series"][0]["datos"][0]["dato"]
        decimal_rate = Decimal(rate)
    except Exception as error:
        print(error)
        raise ErrorGettingExchangeRateException
    return decimal_rate
