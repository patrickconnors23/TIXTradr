from abc import ABC, abstractmethod

class TICKET_CLI(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def getAPI(self, endpoint, obj, params):
        pass
    
    @abstractmethod
    def getEvent(self, ID):
        pass

    @abstractmethod
    def getEventsForPerformer(self, performerID):
        pass

    @abstractmethod
    def getPerformerLiteFromName(self, name):
        pass
