'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from tipfy.appengine.auth.model import User


class Album(db.Model):
    name = db.StringProperty(required=True)
    
    
    def to_dict(self):
        
        result = {
                    
                    "name": self.name
                    
                    
                  }
        return result
    