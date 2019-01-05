import string
from math import isnan
from pprint import pprint as pp

import numpy as np
import pandas as pd
from tqdm import tqdm

from clients.seatGeek import SEAT_GEEK_CLI
from clients.ticketMaster import TICKETMASTER_CLI
from scrapeSC import SCData


class ScrapeTicketData():
    """
    Scrape ticket data from ticketing APIS..
    seatgeek, ticketmaster, etc
    """
    def __init__(self, client="SG", eventPath="eventDF.csv", mapPath="platformMapDF.csv", shouldReadData=False):
        self.SG = SEAT_GEEK_CLI()
        self.TM = TICKETMASTER_CLI()
        self.eventsPath = eventPath
        self.mapPath = mapPath
        self.scArtistDF = SCData().artistDF
        self.platformArtistMapDF = self.readOrCreateMapDF(shouldReadData)
        self.eventsListDF = self.readOrCreateEventsDF()
        self.setClient(client)
        self.numArtistsMatched = 0
        tqdm.pandas()
    
    def readOrCreateMapDF(self, shouldReadData):
        if shouldReadData:
            return self.scArtistDF[["Name", "scID"]]
        else:
            return pd.read_csv(self.mapPath, index_col=0)
    
    def readOrCreateEventsDF(self):
        try:
            return pd.read_csv(self.eventsPath, index_col=0)
        except:
            return pd.DataFrame()
    
    def setClient(self, client):
        self.clientName = client
        if client == "SG":
            self.client = self.SG
        elif client == "TM":
            self.client = self.TM
    
    def getArtistPlatformID(self, name):
        performers = self.client.getPerformerLiteFromName(name)
        ID, name = None, None
        if len(performers) > 0: 
            self.numArtistsMatched += 1
            ID, name = performers[0].get("id"), performers[0].get("name")
        return pd.Series([ID, name])
    
    def fillIDCell(self, row):
        if type(row[f"{self.clientName}_id"]) == float and isnan(row[f"{self.clientName}_id"]):
            return self.getArtistPlatformID(row["query_name"])
        else:
            return pd.Series([row[f"{self.clientName}_id"], row[f"{self.clientName}_name"]])

    def fillArtistIDs(self):
        print(f"Filling artist data after manual fixes")
        clientCols = [f"{self.clientName}_id", f"{self.clientName}_name"]
        self.platformArtistMapDF[clientCols] = self.platformArtistMapDF.progress_apply(self.fillIDCell, axis=1)
        self.pickleMapDF()
        
    def getAllArtistPlatformIDs(self):
        print(f"Matching artists to {self.clientName} IDs")
        self.numArtistsMatched = 0
        clientCols = [f"{self.clientName}_id", f"{self.clientName}_name"]
        self.platformArtistMapDF[clientCols] = self.platformArtistMapDF["Name"].progress_apply(self.getArtistPlatformID)
        print(f"Matched {self.numArtistsMatched} artists to {self.clientName} IDs")
        self.formatNames()
        self.pickleMapDF()
    
    def formatNames(self):
        def formatName(name):
            name = name.lower().strip()
            wordsToStrip = ["official", "music", "records"]
            for word in wordsToStrip:
                name = name.replace(word, "")
            return name
        self.platformArtistMapDF["query_name"] = self.platformArtistMapDF["Name"].progress_apply(formatName)

    def getArtistEvents(self, artist):
        return self.client.getEventsForPerformer(artist[f"{self.clientName}_id"])

    def getAllEvents(self):
        print(f"Fetching {self.clientName} events for all artists")
        events = self.platformArtistMapDF[10:20].apply(self.getArtistEvents, axis=1)
        events = [j for i in events for j in i]
        newEventsDF = pd.DataFrame(events)
        self.eventsListDF = self.eventsListDF.append(newEventsDF)
        self.pickleEvents()

    def pickleMapDF(self):
        print("Pickling data")
        self.platformArtistMapDF.to_csv(self.mapPath)
    
    def pickleEvents(self):
        print("Pickling data")
        self.eventsListDF.to_csv(self.eventsPath)
    
if __name__ == "__main__":
    x = ScrapeTicketData(client="TM")
    x.getAllEvents()
