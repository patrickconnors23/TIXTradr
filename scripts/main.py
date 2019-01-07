import json
import pandas as pd
from tqdm import tqdm
from math import isnan
from currency_converter import CurrencyConverter
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer, StandardScaler

from models.linReg import linReg
from helpers import getRates, convertToDollars, getDaysBetween, getDayOfWeek

class PredictPrice():
    def __init__(self, modelPath="models/linReg.csv"):
        self.followerData = pd.read_csv("data/SCFollowers.csv", index_col=0)
        self.eventData = pd.read_csv("data/eventDF.csv", index_col=0)
        self.idMap = pd.read_csv("data/platformMapDf.csv", index_col=0)
        self.currencies = getRates()
        self.processedData = self.preProcess()
        self.model = linReg()
        tqdm.pandas()

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
    def buildXYTestTrain(df, y):
        df = df.loc[df[y].notnull()]
        splitSet = lambda d, l: (d.drop(columns=[l]), d[l])
        train, test = train_test_split(df)
        return splitSet(train, y), splitSet(test, y)

    @staticmethod
    def encodeBinCols(df, cols):
        for col in cols:
            enc = LabelBinarizer()
            X = df[col]
            data = enc.fit_transform(X)
            newCols = pd.DataFrame(data, columns=enc.classes_  )
            df[newCols.columns] = newCols 
            df = df.drop(columns=[col])
        return df

    @staticmethod
    def standardizeCols(df, cols):
        colsToScale = df[cols]
        scaler = StandardScaler()
        df[cols] = scaler.fit_transform(colsToScale)
        return df
    
    def preProcess(self):
        # Get relevant columns from event data
        events = self.eventData[["artistID", "date", "dateAccessed", "id", "platform", "price", "venueName", "city"]]

        # format price
        events[["minPrice", "maxPrice"]] = events["price"].apply(self.splitPrice)
        # Filter for events that haven't been priced yet
        events = events.loc[events["minPrice"] != ""]
        events = events.drop(columns=["price"])

        # Convert sgId to string
        toStringID = lambda ID: "" if isnan(ID) else str(int(ID))
        self.idMap["SG_id"] = self.idMap["SG_id"].apply(toStringID)

        # Get scID
        events["scID"] = events[["platform", "artistID"]].apply(self.getSCID, axis=1)

        # get num followers
        events = pd.merge(events, self.followerData, how="left", on="scID")
        events = events.drop(columns=["Name"])

        # create days until concert column  
        events["daysUntilConcert"] = events.apply(lambda x: getDaysBetween(x["dateAccessed"], x["date"]), axis=1)
        events["dayOfWeek"] = events["date"].apply(getDayOfWeek)

        # Process categorical columns
        events = self.encodeBinCols(events, ["dayOfWeek", "city", "platform", "venueName"])

        # Scale Columns
        numFollowersCols = list(events.filter(regex="numFollowers").columns)
        events = self.standardizeCols(events, numFollowersCols+["daysUntilConcert"])

        # Drop unneeded cols
        events = events.drop(columns=["id", "artistID","date", "dateAccessed", "maxPrice", "scID"])

        # Split into testing and training
        (xTrain, yTrain), (xTest, yTest) = self.buildXYTestTrain(events, "minPrice") 

        return {
            "xTrain": xTrain,
            "yTrain": yTrain,
            "xTest": xTest,
            "yTest": yTest
        }
    
    def trainModel(self):
        X, y = self.processedData.get("xTrain"), self.processedData.get("yTrain")
        self.model.train(X, y)
        self.model.saveModel()
    
    def evaluateModel(self):
        XTest, yTest = self.processedData.get("xTest"), self.processedData.get("yTest")
        self.model.evaluate(XTest, yTest)
    
if __name__ == "__main__":
    pp = PredictPrice()