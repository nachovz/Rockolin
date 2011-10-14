'''
Created on Sep 29, 2011

@author: Alexander
'''
from google.appengine.ext import db
from werkzeug import cached_property
from tipfy import RequestHandler
from google.appengine.api import mail
from utils import pylast
from UserHandler import BaseHandler
from django.utils import simplejson as json
from delegate.EventDelegate import EventDelegate
from model.Event import Event
from google.appengine.api import images
from xmlrpclib import datetime
from model.Song import Song
from model.SetListVotes import SetListVotes
from delegate.SetListDelegate import SetListVotesDelegate

class SetListHandler(BaseHandler):
    
        def get(self, **kwargs):
            
            songs = Song.all()
            return self.render_response('event.html',section='event',songs=songs)
        

        def post(self, **kwargs):
            song = Song.get(self.request.form.get('idsong'))
            event = Event.get(self.request.form.get('idevent'))
            sum =  int(self.request.form.get('sum'))
            params = {
                        "event": event,
                        "song": song,
                        "sum": sum
                    
                  }
            manager = SetListVotesDelegate('SetListVotes')
            manager.update(params)
            slv = event.event_setlist.order('-votes')
            i = 0
            for s in slv:
                if s.song.key() == song.key():
                    break
                i=i+1
            list = {'position' : i}
            return json.dumps(list)