'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from tipfy.appengine.auth.model import User

class Event(db.Model):
    
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    start_date = db.DateTimeProperty(required=False)
    end_date = db.DateTimeProperty (required = False)
    description = db.StringProperty(required=False)
    creator = db.ReferenceProperty(User, collection_name = 'user_events')
    people_invited = db.ListProperty(db.Key)
    type = db.StringProperty(required=False)
    file = db.BlobProperty(required=False)  
    file150 = db.BlobProperty(required=False) 
    filetype = db.StringProperty(required=False)
    
    def to_dict(self):
        
        result = {
                    
                    "name": self.name
                    
                    
                  }
        return result
    