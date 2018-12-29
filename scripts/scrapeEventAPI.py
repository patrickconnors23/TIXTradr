from clients.seatGeek import SEAT_GEEK_CLI
from clients.ticketMaster import TICKETMASTER_CLI
from scrapeSC import SCData

class ScrapeTicketData():
    def __init__(self, client="SG", path="x.pkl"):
        self.SG = SEAT_GEEK_CLI()
        self.TM = TICKETMASTER_CLI()
        self.path = path
        self.artistDF = SCData().artistDF
        self.setClient(client)
    
    def setClient(self, client):
        if client == "SG":
            self.client = self.SG
        elif client == "TM":
            self.client = self.TM
    
    def findArtistPlatformID(self):
        pass
    

if __name__ == "__main__":
    x = ScrapeTicketData(client="SG")
    print(x.artistDF.iloc[:20])