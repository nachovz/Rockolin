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
API_KEY = "eebbb799fdfee7ae2636c0f488d0fe52" # this is a sample key
API_SECRET = "53bd026aa030663464571c255dd93d6c"
REQUIRED = validators.required()

class SearchForm(Form):
    artist = fields.TextField('Artist', validators=[REQUIRED])
    track = fields.TextField('Track', validators=[REQUIRED])
class LastFmSearchHandler(BaseHandler, Jinja2Mixin):
    
        def get(self, **kwargs):
            
            return self.render_response('artist.html',form=self.form,artista=None )
        
        def post(self):
               
            a = self.form.artist.data
            t = self.form.track.data
            network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
#            artista = network.search_for_artist(a).get_next_page()
            track = network.get_track(a, t)
            return self.render_response('artist.html',form=self.form,artista=track )
            
        @cached_property
        def form(self):
            return SearchForm(self.request)       