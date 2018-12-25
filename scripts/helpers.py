import datetime

def getDateStr():
    now = datetime.datetime.now()
    return f"{now.month}/{now.day}/{now.year}"