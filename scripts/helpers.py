import datetime
from currency_converter import CurrencyConverter

def getDateStr():
    now = datetime.datetime.now()
    return f"{now.month}/{now.day}/{now.year}"

def convertToDollars(amt, currency):
    if currency == "USD":
        return amt
    elif amt == "":
        return ""
    else:
        converter = CurrencyConverter()
        return converter.convert(amt, currency, "USD")
