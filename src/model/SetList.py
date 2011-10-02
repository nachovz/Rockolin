'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from lib.tipfy.appengine.auth.model import User
from Song import Song

class SetList(db.Model):
    songs = db.ListProperty(db.Key)
    
    
    def to_dict(self):
        
        result = {
                    
                    "name": self.name
                    
                    
                  }
        return result
    