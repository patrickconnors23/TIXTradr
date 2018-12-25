import pickle
import heapq as HQ
import numpy as np 
import pandas as pd
from tqdm import tqdm
from soundCloud import SC_CLI

class ScrapeSCData():
    def __init__(self, data=None):
        self.test = ""
        self.client = SC_CLI()
        self.artists = set()
        if data:
            pass
        else:
            initialArtistData = self.scrapeArtists()
            self.pickleArtistData(initialArtistData)
        
    def scrapeArtists(self, limit=1000):
        """
        Get X most popular artists on SC
        """
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
        pbar = tqdm(total=1000)

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
                    "numFollowers": -int(fCount),
                    "Name": artist.username
                }
                artistDF = artistDF.append(row, ignore_index=True)
                following = self.client.getFollowing(artist.id)
                for user in following.collection:
                    try:
                        HQ.heappush(q, (-int(user.followers_count), len(q)+counter, user))
                    except:
                        print("ERROR", user.username)
        
        pbar.close()

        return artistDF
    
    def pickleArtistData(self, df):
        df.to_pickle("SCFollowers.pkl")



if __name__ == "__main__":
    ScrapeSCData()