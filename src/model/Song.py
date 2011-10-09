'''
Created on Aug 9, 2011

@author: Alexander
'''

from google.appengine.ext import db
from tipfy.appengine.auth.model import User
from Album import Album
from Artist import Artist

class Song(db.Model):
    name = db.StringProperty(required=True)
    artist = db.ReferenceProperty(Artist, collection_name = 'artist_songs')
    album = db.ReferenceProperty(Album, collection_name = 'album_songs')
    likes = db.ListProperty(db.Key)
    file = db.BlobProperty(required=False)  
    filetype = db.StringProperty(required=False)
    url = db.StringProperty(required = False)
    
    def to_dict(self):
        
        result = {
                    
                    "name": self.name
                    
                    
                  }
        return result
    