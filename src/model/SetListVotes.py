'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from tipfy.appengine.auth.model import User
from Song import Song
from SetList import SetList
from Event import Event

class SetListVotes(db.Model):
    event = db.ReferenceProperty(Event,collection_name = "event_setlist")
    song = db.ReferenceProperty(Song, collection_name = "song_votes")
    votes = db.IntegerProperty(required = False)
    
    def to_dict(self):
        
        result = {
                    
                    "votes": self.votes
                    
                    
                  }
        return result
    