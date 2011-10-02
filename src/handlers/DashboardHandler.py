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

class DashboardHandler(BaseHandler, Jinja2Mixin):
    
        def get(self, **kwargs):
            
            return self.render_response('dashboard.html')
        