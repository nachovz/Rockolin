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
from tipfy import Response
from google.appengine.api import images
from xmlrpclib import datetime

REQUIRED = validators.required()

class SearchForm(Form):
    name = fields.TextField('Name', validators=[REQUIRED])
    description = fields.TextField('Description', validators=[REQUIRED])
    
class EventHandler(BaseHandler):
    
        def get(self, **kwargs):
            
            manager = EventDelegate('Event')
            events = manager.listEvents(self.auth.user)
            
            return self.render_response('event.html',events=events)
        
        
class CreateEventHandler(BaseHandler):
    
        def get(self, **kwargs):
            
            return self.render_response('create_event.html',form=self.form)
        def castTime(self,datestring,timestring):
            year = int(datestring[:4])
            month = int(datestring[5:7])
            day = int(datestring[8:10])
            hour = int(timestring[:2])
            minutes = int(timestring[3:5])
            newvalue = datetime.datetime(
                                            year,
                                            month, 
                                            day,
                                            hour,
                                            minutes
                                            )
            return newvalue
        
        def post(self, **kwargs):
            image = self.request.files.get('image_upload').read()
            datestring = self.request.form.get('start-date')
            timestring = self.request.form.get('start-time')
            start_date = self.castTime(datestring, timestring)
            end_date = self.castTime(self.request.form.get('finish-date'), self.request.form.get('finish-time'))
            #start_date = datetime.datetime(self.request.form.get('start_time'))
            
            params = {
                        "file": images.resize(image, 90, 90),
                        "filetype": self.request.files.get('image_upload').filename,
                        "name" : self.request.form.get('name'),
                        "start_date" : start_date,
                        "end_date" : end_date,
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

class EventFileHandler(BaseHandler):

    def get(self,key):
        response = Response()
        response.headers['Content-Type'] = "image"
        response.headers['Content-Disposition'] = "attachment"
        try:
            manager = EventDelegate('Event')
            result = manager.getFile(key.split('.')[0])
        except Exception,e:
            result = self.wrapFault(e.message)
        response.headers['filename'] = result["name"]
        response.data = result["file"]
        return response