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
from tipfyext.jinja2 import Jinja2Mixin
from tipfyext.wtforms import Form, fields, validators


REQUIRED = validators.required()

class SearchForm(Form):
    name = fields.TextField('Name', validators=[REQUIRED])
    description = fields.TextField('Description', validators=[REQUIRED])
    
class EventHandler(BaseHandler):
    
        def get(self, **kwargs):
            
            manager = EventDelegate('Event')
            events = manager.listEvents(self.auth.user)
            
            return self.render_response('create_event.html',events=events)
        
        
class CreateEventHandler(BaseHandler):
    
        def get(self, **kwargs):
            
            return self.render_response('create_event.html',form=self.form)
        
        def post(self, **kwargs):
            params = {
                        "image": db.Blob(self.request.files.get('image_upload').filename),
                        "name" : self.request.form.get('name'),
#                        "start_date" : self.cast(self.request.form.get('start_date'),'date'),
#                        "end_date" : self.cast(self.request.form.get('end_date'),'date'),
                        "description" : self.request.form.get('description'),
                        "creator" : self.auth.user,
#                        "people_invited" : self.request.form.getlist('people_invited'),
#                        "type" : self.request.form.get('type'),
#                        "setlist" : self.request.form.getlist('setlist')
                    
                  }
            manager = EventDelegate('Event')
            value = manager.add(params)
            return self.render_response('create_event.html',form=self.form)
        
        @cached_property
        def form(self):
            return SearchForm(self.request)   

class EventListHandler(BaseHandler):
    
        def get(self, **kwargs):
            
            manager = EventDelegate('Event')
            events = manager.listEvents(self.auth.user)
            
            return self.render_response('create_event.html',events=events)
        