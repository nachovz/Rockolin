from BaseDelegate import BaseDelegate
from google.appengine.ext import db
from google.appengine.api import mail
from model.Song import Song
from model.SetListVotes import SetListVotes
class SetListVotesDelegate(BaseDelegate):
    
   
    def update(self, params):
        
        setlist = params["event"].event_setlist.filter('song =',params["song"]).get()
        c = setlist.votes + params["sum"]
        setlist.votes = c
        setlist.put()
        
        setlist.put()
         
        return setlist
