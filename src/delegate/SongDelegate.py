from BaseDelegate import BaseDelegate
from google.appengine.ext import db
from google.appengine.api import mail
from model.Song import Song
from model.Artist import Artist
class SongDelegate(BaseDelegate):
    
    def listSongs(self,user):
        songs = Song.all().filter('creator =', user )
        return songs
    
    def add(self, params):
        artist = Artist.all().filter('artist =', params["artist"]).get()
        artist = None
        if artist:
            a = artist
        else:
            a = Artist(
                       name = params["name"]
                       )
            a.put()
        song = Song(
            name = params["name"],
            artist = a,
            url = params["url"]
        )
        song.put()
        
        return song
    
    def update(self, params):
        
        song = params["song"]
        song.response_note = params["reply"]
        song.status = "accepted"
        song.put()
         

        
        song.put()
        return song

    def getFile(self, key):
    
        song = Song.get(key)
        result = {
                "file": song.file,
                "name": str(song.key())+"."+song.filetype
        
                }
        
        return result