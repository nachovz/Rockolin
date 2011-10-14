'''
Created on Sep 29, 2011

@author: Alexander
'''
from werkzeug import cached_property
from tipfy import RequestHandler
from google.appengine.api import mail
from utils import pylast
from UserHandler import BaseHandler
from django.utils import simplejson as json

from tipfyext.jinja2 import Jinja2Mixin
from tipfyext.wtforms import Form, fields, validators
from delegate.EventDelegate import EventDelegate
API_KEY = "eebbb799fdfee7ae2636c0f488d0fe52" # this is a sample key
API_SECRET = "53bd026aa030663464571c255dd93d6c"

class DashboardHandler(BaseHandler):
    
        def get(self, **kwargs):
            network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
            
            manager = EventDelegate('Event')
            events = manager.listEvents(self.auth.user)
            popular_songs = []
            
            for e in events:
                for s in e.event_setlist:
                    aux = True
                    if len(popular_songs) > 0 :
                        for p in popular_songs:
                            if p[0] == s.song.name:
                                p[1] = int(p[1])+int(s.votes)
                                aux = False
                        if aux:
                            popular_songs.append([s.song.name,s.votes,network.get_artist(s.song.artist.name)])
                    else:
                        popular_songs.append([s.song.name,s.votes,network.get_artist(s.song.artist.name)])
                        
            ps = sorted(popular_songs, key=lambda song: song[1], reverse=True)[:5]
            
                
            return self.render_response('dashboard.html',section='dashboard', events=events,popular_songs=ps)
        