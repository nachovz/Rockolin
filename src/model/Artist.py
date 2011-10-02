'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from lib.tipfy.appengine.auth.model import User


class Artist(db.Model):
    name = db.StringProperty(required=False)
    
    
    def to_dict(self):
        
        result = {
                    
                    "name": self.name
                    
                    
                  }
        return result
    