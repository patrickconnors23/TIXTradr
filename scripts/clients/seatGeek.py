import requests, sys, os
from pprint import pprint as pp

sys.path.append(os.path.join(os.path.dirname(__file__)))

from config import SG_CLIENT_ID
from ticketClient import TICKET_CLI

class SEAT_GEEK_CLI(TICKET_CLI):
    def __init__(self):
        self.CLIENT_ID = SG_CLIENT_ID
        self.baseURL = "https://api.seatgeek.com/2"
        self.eventsEndpoint = "/events"
        self.performersEndpoint = "/performers"
        self.CLIENT_SECRET = ""
    
    def getAPI(self, endpoint="/events", obj="", params={}):
        # Set header
        p = {"client_id": self.CLIENT_ID, "per_page":"50"}
        # Add query params
        for key, val in params.items(): p[key] = val
        # Send initial response
        return requests.get(self.baseURL + endpoint + "/" + obj, params=p).json()
    
    def getEvent(self, ID):
        return self.getAPI(self.eventsEndopint, str(ID))
    
    def extractEventData(self, event):
        venuify = lambda x: {"city": x["city"], "name": x["name"]}
        parseDate = lambda x: x.split("T")[0]
        return {
            "id": f"SG:{event['id']}",
            "date": parseDate(event["datetime_local"]),
            "median_price": event["stats"]["median_price"],
            "numListings": event["stats"]["listing_count"],
            "price": {
                "minPrice": event["stats"]["lowest_price"],
                "maxPrice": event["stats"]["highest_price"],
                "currency": "USD",
            },
            "venue": venuify(event["venue"]),
        }

    def getEventsForPerformer(self, performerID):
        """
        id -> {date, price, venue}
        """
        data = self.getAPI(endpoint=self.eventsEndpoint, params={"performers.id": performerID})
        events = [self.extractEventData(event) for event in data["events"]]
        return events

    def getPerformerLiteFromName(self, name):
        """
        name -> {id, name, numEvents}
        """
        data = self.getAPI(endpoint=self.performersEndpoint, params={"q": name})
        performers = data["performers"]
        stripInfo = lambda x: {"id": x["id"], "name": x["name"], "numEvents": x["num_upcoming_events"]} 
        return [stripInfo(p) for p in performers]

if __name__ == "__main__":
    client = SEAT_GEEK_CLI()
    artist = client.getPerformerLiteFromName("Diplo")[0]
    events = client.getEventsForPerformer(artist["id"])
    pp(events)

