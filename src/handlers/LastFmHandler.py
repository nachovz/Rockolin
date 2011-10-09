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
import yql
API_KEY = "eebbb799fdfee7ae2636c0f488d0fe52" # this is a sample key
API_SECRET = "53bd026aa030663464571c255dd93d6c"
REQUIRED = validators.required()


class SearchForm(Form):
    artist = fields.TextField('Artist', validators=[REQUIRED])
    track = fields.TextField('Track')
class GetArtistHandler(BaseHandler, Jinja2Mixin):
    def post(self):
               
            a = self.form.artist.data
            t = self.form.track.data
            
            y = yql.Public()
            query = 'select name from music.artist.search where keyword=@text limit 8';
            result = y.execute(query, {"text": a})
            artista = json.dumps(json.loads(result)['query']['results']['Artist'])
    #            network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
    ##            artista = network.search_for_artist(a).get_next_page()
    #            track = network.get_track(a, t)
            return artista
    
    def get(self):
               
        
            y = yql.Public()
            query = 'select name from music.artist.search where keyword=@text limit 5';
            result = y.execute(query, {"text": self.request.args.get('q')})
            artista = json.dumps(json.loads(result)['query']['results']['Artist'])
    #            network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
    ##            artista = network.search_for_artist(a).get_next_page()
    #            track = network.get_track(a, t)
            return artista
            
class LastFmSearchHandler(BaseHandler, Jinja2Mixin):
    
        def get(self, **kwargs):
            
            
            return self.render_response('artist.html',form=self.form,artista= None)
        
        def post(self):
               
            a = self.form.artist.data
            t = self.form.track.data
            
            
            network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
            artista = network.get_artist(a)
            track = network.get_track(a).get_next_page()
            return self.render_response('artist.html',form=self.form,artista=artista )
            
        @cached_property
        def form(self):
            return SearchForm(self.request)       