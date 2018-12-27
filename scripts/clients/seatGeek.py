import requests
from pprint import pprint as pp

from ticketClient import TICKET_CLI

class SEAT_GEEK_CLI(TICKET_CLI):
    def __init__(self):
        self.CLIENT_ID = "MTQ1ODk2Mzl8MTU0NTc3MTgzMC43"
        self.baseURL = "https://api.seatgeek.com/2"
        self.eventsEndpoint = "/events"
        self.performersEndpoint = "/performers"
        self.CLIENT_SECRET = ""
    
    def getAPI(self, endpoint="/events", obj="", params={}):
        # Set header
        p = {"client_id": self.CLIENT_ID,
            "per_page":"50"}
        # Add query params
        for key, val in params.items(): p[key] = val
        # Send initial response
        response = requests.get(self.baseURL + endpoint + "/" + obj, params=p)
        return response.json()
    
    def getEvent(self, ID):
        return self.getAPI(self.eventsEndopint, str(ID))
    
    def extractEventData(self, event):
        return {
            "date": event["datetime_utc"],
            "lowest_price": event["stats"]["lowest_price"],
            "median_price": event["stats"]["median_price"],
            "highest_price": event["stats"]["highest_price"],
            "numListings": event["stats"]["listing_count"],
            "venue": event["venue"],
        }

    def getEventsForPerformer(self, performerID):
        data = self.getAPI(endpoint=self.eventsEndpoint, params={"performers.id": performerID})
        events = [self.extractEventData(event) for event in data["events"]]
        return events

    def getPerformerLiteFromName(self, name):
        data = self.getAPI(endpoint=self.performersEndpoint, params={"q": name})
        performers = data["performers"]
        stripInfo = lambda x: {"id": x["id"], "name": x["name"], "numEvents": x["num_upcoming_events"]} 
        return [stripInfo(p) for p in performers][0]

if __name__ == "__main__":
    client = SEAT_GEEK_CLI()
    artist = client.getPerformerLiteFromName("Skrillex")
    events = client.getEventsForPerformer(artist["id"])
    print(events)

