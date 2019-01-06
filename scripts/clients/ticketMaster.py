import requests, sys, os, datetime
from pprint import pprint as pp

sys.path.append(os.path.join(os.path.dirname(__file__)))

from config import TM_API_KEY
from ticketClient import TICKET_CLI

class TICKETMASTER_CLI(TICKET_CLI):
    def __init__(self):
        self.CLIENT_ID = TM_API_KEY
        self.baseURL = "https://app.ticketmaster.com"
        self.pricesEndpoint = "/commerce/v2/events" # /{eventID}/offers
        self.eventsEndpoint = "/discovery/v2/events" # /{eventID}/offers
        self.performersEndpoint = "/discovery/v2/attractions"


    def getAPI(self, endpoint, obj="", params={}):
        # Set header
        p = {"apikey": self.CLIENT_ID}
        # Add query params
        for key, val in params.items(): p[key] = val
        # Send initial response
        return requests.get(self.baseURL + endpoint + "/" + obj, params=p).json()
    
    def getEvent(self, ID):
        pass
    
    def getEventPrice(self, ID):
        try:
            data = self.getAPI(endpoint=self.pricesEndpoint, obj=f"/{ID}/offers")
            return list(map(lambda x: x["attributes"], data["prices"]["data"]))
        except:
            print(f"Couldn't get prices for artist with ID: {ID}")
            return []

    def extractPrice(self, price):
        if price:
            price = price[0]
            minP, maxP, currency = price.get("min"), price.get("max"), price.get("currency")
        else:
            minP, maxP, currency = None, None, None
        return {"minPrice": minP, "maxPrice": maxP, "currency": currency}
        
    def getDateStr(self):
        now = datetime.datetime.now()
        return f"{now.year}-{now.month}-{now.day}"

    def extractEventData(self, event, performerID):
        artistify = lambda att: [x["name"] for x in att][:4] if len(att) > 0 else att
        return {
            "id": f"TM:{event['id']}",
            "date": event["dates"]["start"]["localDate"],
            "price": self.extractPrice(event.get("priceRanges")),
            "venueName": event["_embedded"]["venues"][0]["name"],
            "city": event["_embedded"]["venues"][0]["city"]["name"],
            "title": event["name"],
            "artistID": performerID,
            "artists": artistify(event["_embedded"]["attractions"]),
            "dateAccessed": self.getDateStr(),
            "platform":"TM"
        }

    def getEventsForPerformer(self, performerID):
        """
        id -> {id, date, price, venue}
        """
        try:
            if type(performerID) == str:
                q = {"attractionId": performerID, "source": "ticketmaster"}
                data = self.getAPI(endpoint=self.eventsEndpoint, params=q)
                events = data["_embedded"]["events"]
                return  [self.extractEventData(event, performerID) for event in events]
            else:
                return []
        except:
            return []

    def getPerformerLiteFromName(self, name):
        """
        name -> {id, name, numEvents}
        """
        try:
            data = self.getAPI(endpoint=self.performersEndpoint, params={"keyword": name})
            artists = data["_embedded"]["attractions"]
            stripArtist = lambda x: {"id": x["id"], "name": x["name"], "numEvents": len(x["upcomingEvents"])}
            return [stripArtist(artist) for artist in artists]
        except:
            # print(f"Couldn't find artist with name: {name}")
            return []

if __name__ == "__main__":
    TMC = TICKETMASTER_CLI()
    skril = TMC.getPerformerLiteFromName("Diplo")[0]
    print(skril)
    events = TMC.getEventsForPerformer(skril["id"])
    pp(events)
