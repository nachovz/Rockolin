from BaseDelegate import BaseDelegate
from google.appengine.ext import db
from google.appengine.api import mail
from model.Event import Event

class EventDelegate(BaseDelegate):
    
    def listEvents(self,user):
        events = Event.all().filter('creator =', user )
        return events
    
    def add(self, params):
        
        event = Event(
            name = params["name"],
            file = params["file"],
            filetype = params["filetype"].split('.')[1],
            start_date = params["start_date"],
            end_date = params["end_date"],
            description = params["description"],
            creator = params["creator"],
#            people_invited = params["people_invited"],
#            type = params["type"],
            #setlist = params["setlist"],
            
        )
        event.put()
        
        return event
    
    def update(self, params):
        
        event = params["event"]
        event.response_note = params["reply"]
        event.status = "accepted"
        event.put()
         

        
        event.put()
        return event

    def getFile(self, key):
    
        event = Event.get(key)
        result = {
                "file": event.file,
                "name": str(event.key())+"."+event.filetype
        
                }
        
        return result