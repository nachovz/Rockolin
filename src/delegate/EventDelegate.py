from BaseDelegate import BaseDelegate
from google.appengine.ext import db
from google.appengine.api import mail
from model.Event import Event
from model.InvitedUser import InvitedUser
from google.appengine.api.taskqueue.taskqueue import Task
from google.appengine.api.taskqueue import Queue

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
        list = params["people_invited"]
        for l in list:
            iu = InvitedUser(
                             email = l,
                             event = event
                             )
            queue = Queue('mail-queue')
            subject =  "You have been invited to the event " + event.name + " in Rockolin'"
            body = " Hi!, You have been invited to the event " + event.name + """
                    This event would be on: """ + event.start_date + """ 
                    If you want to decide the music justo go to the following 
                    link: http://rockolinapp.appspot.com/event/"""+str(event.key())+"""
            
            queue.add(Task(url='/task/mail', params = { 'to' : l, 'subject' : subject, 'body' : body }))        
            iu.put()
        queue.purge()
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