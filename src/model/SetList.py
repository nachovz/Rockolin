'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from tipfy.appengine.auth.model import User
from Song import Song
from Event import Event

class SetList(db.Model):
    songs = db.ListProperty(db.Key)
    
    def to_dict(self):
        
        result = {
                    
                    "name": self.name
                    
                    
                  }
        return result
    