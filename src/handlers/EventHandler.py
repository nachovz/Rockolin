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
from model.Song import Song
from model.SetListVotes import SetListVotes
REQUIRED = validators.required()

class SearchForm(Form):
    name = fields.TextField('Name', validators=[REQUIRED])
    description = fields.TextField('Description', validators=[REQUIRED])

class ValidateUserForm(Form):
    email = fields.TextField('Email', validators=[REQUIRED])
    
class EventValidateUserHandler(BaseHandler):
    def get(self,key, **kwargs):
            event = Event.get(key)
            return self.render_response('validate_user.html',section='validate_user',form = self.form,event=event)
    
    def post(self, key, **kwargs):
        event = Event.get(key)
        email = self.form.email.data
        invited_users = event.event_user_invited
        for iu in invited_users:
            if email == iu.email:
                return self.redirect('/event/'+str(event.key()))
            else: 
                self.messages.append(('This email was not invited to this event',
                            'error'))
                return self.get(key,**kwargs)
            
    @cached_property
    def form(self):
        return ValidateUserForm(self.request)   
        
class EventHandler(BaseHandler):
    
        def get(self,key, **kwargs):
            
            slv = Event.get(key).event_setlist.order('-votes')
            return self.render_response('event.html',section='event',setlist = slv,event=Event.get(key))
        

        
class CreateEventHandler(BaseHandler):
    
        def get(self, **kwargs):
            songs = Song.all()
            return self.render_response('create_event.html',section='create-event',form=self.form,songs=songs)
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
                        "file150": images.resize(image, 150, 150),
                        "filetype": self.request.files.get('image_upload').filename,
                        "name" : self.request.form.get('name'),
                        "start_date" : start_date,
                        "end_date" : end_date,
                        "description" : self.request.form.get('description'),
                        "creator" : self.auth.user,
                        "people_invited" : self.request.form.getlist('contacts[]'),
#                        "type" : self.request.form.get('type'),
                        "setlist" : self.request.form.getlist('songs[]')
                    
                  }
            manager = EventDelegate('Event')
            value = manager.add(params)
            songs = Song.all()
            
            return self.redirect('/dashboard')
        
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
            result = manager.getFile(key.split('.')[0],90)
        except Exception,e:
            result = self.wrapFault(e.message)
        response.headers['filename'] = result["name"]
        response.data = result["file"]
        return response
    
class EventFile150Handler(BaseHandler):

    def get(self,key):
        response = Response()
        response.headers['Content-Type'] = "image"
        response.headers['Content-Disposition'] = "attachment"
        try:
            manager = EventDelegate('Event')
            result = manager.getFile(key.split('.')[0],150)
        except Exception,e:
            result = self.wrapFault(e.message)
        response.headers['filename'] = result["name"]
        response.data = result["file"]
        return response