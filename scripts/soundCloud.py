import soundcloud
from tqdm import tqdm

class SC_CLI():
    def __init__(self):
        self.CLIENT_ID = "b9f9babc7bbe35f9b08f9efed8af6a25"
        self.CLIENT_SECRET = "5ae2ca5e51b3e066800d83e23e34f3ca"
        self.SC = soundcloud.Client(client_id=self.CLIENT_ID)
    
    def getArtist(self, ID):
        try: return self.SC.get(f'/users/{ID}')
        except: return "SCEXCEPTION"
    
    def getFollowing(self, ID):
        try: return self.SC.get(f'/users/{ID}/followings')
        except: return "SCEXCEPTION"
    
    def getFavoriteTrackArtists(self, ID):
        try: return [track.user for track in self.SC.get(f'/users/{ID}/favorites')]
        except: return []

    def getNumFollowers(self, ID):
        try: return int(self.SC.get(f'/users/{ID}').followers_count)
        except: return "SCEXCEPTION"
    
    def getSeedArtistsForScrape(self):
        try: return [artist for artist in (self.SC.get('/users', limit=10))]
        except: return "SCEXCEPTION"


if __name__ == "__main__":
    SC = SC_CLI()
