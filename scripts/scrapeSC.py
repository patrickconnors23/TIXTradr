import pickle, random
import heapq as HQ
import numpy as np 
import pandas as pd
from tqdm import tqdm
from clients.soundCloud import SC_CLI
from helpers import getDateStr

class ScrapeSCData():
    def __init__(self, numArtists=0, filePath="SCFollowers.pkl"):
        self.client = SC_CLI()
        self.path = filePath
        if numArtists > 0:
            self.loadArtistsFromSC(numArtists)
        
        self.artistDF = pd.read_pickle(self.path)
    
    def checkHead(self):
        sortedDF = self.artistDF.sort_values(by=['numFollowers 12/25/2018'],
            ascending=False)
        print(sortedDF.head())

    def loadArtistsFromSC(self, numArtists):
        initialArtistData = self.scrapeArtists(numArtists)
        self.pickleArtistData()
        
    def scrapeArtists(self, limit=1000):
        """
        Get X most popular artists on SC
        """
        print(f"Scraping {limit} artists...")
        dateStr = getDateStr()

        # Init queue, seen set, and artist dataframe
        seen = set()
        artistDF = pd.DataFrame()
        q = [] 

        # Generate seeds to start SC BFS
        seeds = self.client.getSeedArtistsForScrape()
        for el in seeds: 
            HQ.heappush(q, (-int(el.followers_count), len(q), el))

        # Limit number of iterations
        counter = 0
        pbar = tqdm(total=limit)

        # Scrape SC most popular artsists
        while q and counter < limit:
            # Pop artist from heap 
            fCount, _, artist = HQ.heappop(q)

            # Add unseen artist to DF
            if artist.id not in seen:
                seen.add(artist.id)
                counter+=1
                pbar.update(1)
                row = {
                    "id": int(artist.id),
                    f"numFollowers {dateStr}": -int(fCount),
                    "Name": artist.username
                }
                artistDF = artistDF.append(row, ignore_index=True)
                following = self.client.getFollowing(artist.id)
                try:
                    for user in following.collection:
                        try:
                            HQ.heappush(q, (-int(user.followers_count), len(q)+random.random(), user))
                        except:
                            print("ERROR", user.username)
                except:
                    print("Follower obj not returned")
        
        pbar.close()
        print("Scraping complete")
        artistDF = artistDF.set_index(["id"])
        artistDF["scID"] = artistDF.index
        return artistDF
    
    def pickleArtistData(self):
        print("Pickling data")
        self.artistData.to_pickle(self.path)
    
    def getCurrentArtistFollows(self):
        dateStr = getDateStr()
        tqdm.pandas()
        print("Updating SC artist data...")
        self.artistDF[f"numFollowers {dateStr}"] = self.artistDF["scID"].progress_apply(lambda x: self.client.getNumFollowers(int(x)))
        self.checkHead()
        self.pickleArtistData()


if __name__ == "__main__":
    ScrapeSCData()