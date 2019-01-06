import datetime
from currency_converter import CurrencyConverter

def getDateStr():
    now = datetime.datetime.now()
    return f"{now.month}/{now.day}/{now.year}"


def getRates():
    print(f"Getting exchange rates for tickets")
    currencies = ['EUR', 'AUD', 'GBP', 'NZD', 'MXN', 'CAD', 'USD']
    converter = CurrencyConverter()
    return {x: converter.convert(1, currency=x, new_currency="USD") for x in currencies}

def convertToDollars(amt, currency):
    if currency == "USD":
        return amt
    elif amt == "":
        return ""
    else:
        converter = CurrencyConverter()
        return converter.convert(amt, currency, "USD")


def makeDate(date):
    x = date.split("-")
    return datetime.datetime(year=int(x[0]), month=int(x[1]), day=int(x[2]))

def getDaysBetween(date1, date2):
    date1, date2 = makeDate(date1), makeDate(date2)
    return (date2 - date1).days

def getDayOfWeek(date):
    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 
        4: "Friday", 5: "Saturday", 6: "Sunday"}
    date = makeDate(date)
    return days[date.weekday()]
