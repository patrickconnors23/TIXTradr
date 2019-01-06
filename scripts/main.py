import json
import pandas as pd
from tqdm import tqdm
from math import isnan
from currency_converter import CurrencyConverter
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from helpers import convertToDollars

class PredictPrice():
    def __init__(self, modelPath="models/linReg.csv"):
        self.SC_data = pd.read_pickle("data/SCFollowers.pkl")
        self.eventData = pd.read_csv("data/eventDF.csv", index_col=0)
        self.idMap = pd.read_csv("data/platformMapDf.csv", index_col=0)
        self.currencies = self.getRates()
        tqdm.pandas()
    
    def getRates(self):
        print(f"Getting exchange rates for tickets")
        currencies = ['EUR', 'AUD', 'GBP', 'NZD', 'MXN', 'CAD', 'USD']
        converter = CurrencyConverter()
        return {x: converter.convert(1, currency=x, new_currency="USD") for x in currencies}

    def trainTestSplit(self):
        pass
    
    def scaleData(self):
        pass
    
    def splitVenue(self):
        pass

    def splitPrice(self, priceDict):
        priceDict = priceDict.replace("None", "\"\"")
        priceDict = json.loads(priceDict.replace("\'","\""))
        return pd.Series([self.convertToDollars(priceDict["minPrice"], priceDict["currency"]), 
            self.convertToDollars(priceDict["maxPrice"], priceDict["currency"])])

    def convertToDollars(self, amt, currency):
        if amt == "":
            return ""
        else:
            return amt * self.currencies[currency]

    def getSCID(self, row):
        query = self.idMap.loc[self.idMap[f"{row['platform']}_id"] == str(row["artistID"])]
        return query.iloc[0]["scID"]

    @staticmethod
    def toStringID(ID):
        return "" if isnan(ID) else str(int(ID))

    def preProcess(self):
        # Get relevant columns from event data
        events = self.eventData[["artistID", "date", "dateAccessed", "id", "platform", "price", "venueName", "city"]]

        # format price
        events[["minPrice", "maxPrice"]] = events["price"].apply(self.splitPrice)
        events = events.drop(columns=["price"])

        events = events.iloc[10:100]

        # Convert sgId to string
        self.idMap["SG_id"] = self.idMap["SG_id"].apply(self.toStringID)

        # Get scID
        events["scID"] = events[["platform", "artistID"]].apply(self.getSCID, axis=1)
        
        # get followers
        print(events)
        return events



if __name__ == "__main__":
    pp = PredictPrice()
    pp.preProcess()