'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from tipfy.appengine.auth.model import User
from model.Event import Event

class InvitedUser(db.Model):
    firstname = db.StringProperty(required=False)
    lastname = db.StringProperty(required=False)
    email = db.EmailProperty()
    favorite_songs = db.ListProperty(db.Key)
    event = db.ReferenceProperty(Event, collection_name = 'event_user_invited')
    status = db.StringProperty(default='waiting')
    gender = db.StringProperty(required=False)
    
    def to_dict(self):
        
        result = {
                    
                    "name": self.name
                    
                    
                  }
        return result
    