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
from delegate.SongDelegate import SongDelegate
from model.Song import Song
from tipfyext.jinja2 import Jinja2Mixin
from tipfyext.wtforms import Form, fields, validators
from tipfy import Response
from google.appengine.api import images
from xmlrpclib import datetime

REQUIRED = validators.required()

class SongForm(Form):
    name = fields.TextField('Name', validators=[REQUIRED])
    artist = fields.TextField('Artist', validators=[REQUIRED])
    url = fields.TextField('URL', validators=[REQUIRED])

class CreateSongHandler(BaseHandler):
    
        def get(self, **kwargs):
            songs = Song.all()
            return self.render_response('upload_song.html',form=self.form,songs=songs)

        
        def post(self, **kwargs):
            
            
            params = {
                        "url": self.request.form.get('url'), 
                        "name" : self.request.form.get('name'), 
                        "artist" : self.request.form.get('artist')                   
                  }
            manager = SongDelegate('Song')
            manager.add(params)
            
            return self.get(**kwargs)
        
        @cached_property
        def form(self):
            return SongForm(self.request)   

class SongListHandler(BaseHandler):
    
        def get(self, **kwargs):
        
            songs = Song.all()
            return self.render_response('create_song.html',songs=songs)

class SongFileHandler(BaseHandler):

    def get(self,key):
        response = Response()
        response.headers['Content-Type'] = "audio"
        response.headers['Content-Disposition'] = "attachment"
        try:
            manager = SongDelegate('Song')
            result = manager.getFile(key.split('.')[0])
        except Exception,e:
            result = self.wrapFault(e.message)
        response.headers['filename'] = result["name"]
        response.data = result["file"]
        return response