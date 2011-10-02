'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from lib.tipfy.appengine.auth.model import User


class InvitedUser(db.Model):
    firstname = db.StringProperty(required=True)
    lastname = db.StringProperty(required=True)
    email = db.EmailProperty()
    favorite_songs = db.ListProperty(db.Key)
    
    
    def to_dict(self):
        
        result = {
                    
                    "name": self.name
                    
                    
                  }
        return result
    