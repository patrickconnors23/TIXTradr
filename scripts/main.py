from scrapeSC import ScrapeSCData

class PredictPrice():
    def __init__(self):
        self.SC_data = ScrapeSCData()

if __name__ == "__main__":
    pp = PredictPrice()
    pp.SC_data.getCurrentArtistFollows()