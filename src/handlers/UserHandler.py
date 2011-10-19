from werkzeug.utils import cached_property

from tipfy import RequestHandler
from tipfy.auth import (login_required, user_required,
    UserRequiredIfAuthenticatedMiddleware)
from tipfy.auth.facebook import FacebookMixin
from tipfy.auth.friendfeed import FriendFeedMixin
from tipfy.auth.google import GoogleMixin
from tipfy.auth.twitter import TwitterMixin
from tipfy.sessions import SessionMiddleware
from tipfy.utils import json_encode
from exception import RequestException
from tipfyext.jinja2 import Jinja2Mixin
from tipfyext.wtforms import Form, fields, validators
from google.appengine.ext import db
import datetime
# ----- Forms -----

REQUIRED = validators.required()
email_global = None
class LoginForm(Form):
    username_login = fields.TextField('')
    password_login = fields.PasswordField('')
    remember = fields.BooleanField('')


class SignupForm(Form):
    nickname = fields.TextField('Nickname', validators=[REQUIRED])


class RegistrationForm(Form):
    username = fields.TextField('Username', validators=[REQUIRED])
    email = fields.TextField('Email', validators=[REQUIRED])
    password = fields.PasswordField('Password', validators=[REQUIRED])
    password_confirm = fields.PasswordField('Confirm the password', validators=[REQUIRED])
    username_login = fields.TextField('')
    password_login = fields.PasswordField('')

# ----- Handlers -----

class BaseHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware(), UserRequiredIfAuthenticatedMiddleware()]

    def getVar(self, name, type='string'):
        
        if(type=='listProperty'):
            return self.request.args.getlist("name")
            
        value = self.request.args.get(name)
        if(value != None and value != ''):
            return self.cast(value,type);
        else:
            exception = RequestException.InvalidArgumentException
            exception.message = "Invalid Argument "+name
            #exception.setCode(401)
            raise exception
    
    def getOptionalVar(self, name, type='string'):
        
        value = self.request.args.get(name)
        if(value != None and value != ''):
            return self.cast(value,type);
        else:
            return None
    def cast(self,value,type):
        
        newvalue = None
        try:
            if(type=='long'):
                newvalue = long(value)
            elif(type=='string'):
                try:
                    newvalue = str(value)
                except:
                    newvalue = value
            elif(type=='float'):
                newvalue = float(value)
            elif(type=='int'):
                newvalue = int(value)
            elif(type=='bool'):
                newvalue = (value=='true' or value=='True' or value=='TRUE')
            elif(type=='email'):
                    newvalue = value
            elif(type=='date'):
                
                if(value[11:13]): hora = int(value[11:13])
                else: hora = 0
                if(value[14:16]): minuto = int(value[14:16])
                else: minuto = 0
                
                newvalue = datetime.datetime(
                                            int(value[6:10]),
                                            int(value[3:5]), 
                                            int(value[:2]),
                                            hora,
                                            minuto
                                            )
            elif(type=='reference'):
                newvalue = db.get(value)
            elif(type=='file'):
                    newvalue = value
            else:
                exception = RequestException.InvalidArgumentException
                exception.message = "Cast error "+value
                #exception.setCode(401)
                raise exception
    
            return newvalue
        except Exception,e:
            exception = RequestException.InvalidArgumentException
            exception.message = "Cast Error "+value+": "+e.message
            #exception.setCode(401)
            raise exception
        
        newvalue = None
        
    def wrapResult(self,data):
        result = {
                    'code' : '200',
                    'message' : 'ok',
                    'data' : data
                  }
        return result
    
    def wrapFault(self,message, code=500):
        result = {
                    'code' : str(code),
                    'message' : message
                  }
        return result
    
    @cached_property
    def messages(self):
        """A list of status messages to be displayed to the user."""
        return self.session.get_flashes(key='_messages')

    def render_response(self, filename, **kwargs):
        auth_session = None
        if self.auth.session:
            auth_session = self.auth.session

        kwargs.update({
            'auth_session': auth_session,
            'current_user': self.auth.user,
            'login_url':    self.auth.login_url(),
            'logout_url':   self.auth.logout_url(),
            'current_url':  self.request.url,
        })
        if self.messages:
            kwargs['messages'] = json_encode([dict(body=body, level=level)
                for body, level in self.messages])

        return super(BaseHandler, self).render_response(filename, **kwargs)

    def redirect_path(self, default='/'):
        if '_continue' in self.session:
            url = self.session.pop('_continue')
        else:
            url = self.request.args.get('continue', '/')

        if not url.startswith('/'):
            url = default

        return url

    def _on_auth_redirect(self):
        """Redirects after successful authentication using third party
        services.
        """
        if '_continue' in self.session:
            url = self.session.pop('_continue')
        else:
            url = '/'

        if not self.auth.user:
            url = self.auth.signup_url()
            

        return self.redirect(url)
    
    def _on_auth_redirect_invite(self,key):
        """Redirects after successful authentication using third party
        services.
        """
        if '_continue' in self.session:
            url = self.session.pop('_continue')
        else:
            url = '/auth/guest?event='+str(key)

        if not self.auth.user:
            url = '/auth/guest?event='+str(key)
            

        return self.redirect(url)


class HomeHandler(BaseHandler):
    def get(self, **kwargs):
        
       
        
        return self.render_response('home.html', form = self.form,section='home')
    
    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth.user:
            # User is already registered, so don't process the signup form.
            return self.redirect(redirect_url)

        if self.form.validate():
            username = self.form.username.data
            email = self.form.email.data
            password = self.form.password.data
            password_confirm = self.form.password_confirm.data

            if password != password_confirm:
                self.messages.append(("Password confirmation didn't match.",
                    'error'))
                return self.get(**kwargs)

            auth_id = 'own|%s' % username
            user = self.auth.create_user(username, auth_id, email = email, password=password)
            if user:
                self.auth.login_with_auth_id(user.auth_id, True)
                self.session.add_flash('You are now registered. Welcome!',
                    'success', '_messages')
                return self.redirect(redirect_url)
            else:
                self.messages.append(('This nickname is already registered.',
                    'error'))
                return self.get(**kwargs)

        self.messages.append(('A problem occurred. Please correct the '
            'errors listed in the form.', 'error'))
        return self.get(**kwargs)
    
    @cached_property
    def form(self):
        return RegistrationForm(self.request)


class ContentHandler(BaseHandler):
    @user_required
    def get(self, **kwargs):
        return self.render_response('content.html', section='content')


class LoginHandler(BaseHandler):
    def get(self, **kwargs):

        if self.auth.user:
            # User is already registered, so don't display the signup form.
            return self.redirect('/dashboard')

        opts = {'continue': self.redirect_path()}
        context = {
            'form':                 self.form,
            'facebook_login_url':   self.url_for('auth/facebook', **opts),
            'friendfeed_login_url': self.url_for('auth/friendfeed', **opts),
            'google_login_url':     self.url_for('auth/google', **opts),
            'twitter_login_url':    self.url_for('auth/twitter', **opts),
            'yahoo_login_url':      self.url_for('auth/yahoo', **opts),
        }
        return self.render_response('login.html',section='login', **context)

    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth.user:
            # User is already registered, so don't display the signup form.
            return self.redirect(redirect_url)

        if self.form.validate():
            username = self.form.username_login.data
            password = self.form.password_login.data
            remember = self.form.remember.data

            res = self.auth.login_with_form(username, password, remember)
            if res:
                self.session.add_flash('Welcome back!', 'success', '_messages')
                return self.redirect(redirect_url)

        self.messages.append(('Authentication failed. Please try again.',
            'error'))
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return LoginForm(self.request)


class LogoutHandler(BaseHandler):
    def get(self, **kwargs):
        self.auth.logout()
        return self.redirect(self.redirect_path())

class GuestHandler(BaseHandler):
    
    @login_required
    def get(self,**kwargs):
        if self.auth.user:
            # User is already registered, so don't display the signup form.
            return self.redirect(self.redirect_path())
        event = self.request.args.get('event')
        auth_id = self.auth.session.get('id')
        user = self.auth.create_user(auth_id.split('|')[1], auth_id,email=email_global,type='guest')
        if user:
            self.auth.login_with_auth_id(user.auth_id, True)
            self.session.add_flash('You are now registered. Welcome!',
                'success', '_messages')
            if self.auth.user:
                return self.redirect('/event/'+str(event))
            else:
                return self.redirect('/event/invitation/'+str(event))
        else:
            self.messages.append(('This nickname is already registered.',
                'error'))
            return self.get(**kwargs)

        self.messages.append(('A problem occurred. Please correct the '
            'errors listed in the form.', 'error'))
        return self.get(**kwargs)
    
class SignupHandler(BaseHandler):
    
    @login_required
    def get(self, **kwargs):
        if self.auth.user:
            # User is already registered, so don't display the signup form.
            return self.redirect(self.redirect_path())
        auth_id = self.auth.session.get('id')
        user = self.auth.create_user(auth_id.split('|')[1], auth_id,email=email_global)
        if user:
            self.auth.login_with_auth_id(user.auth_id, True)
            self.session.add_flash('You are now registered. Welcome!',
                'success', '_messages')
            if self.auth.user:
                return self.redirect('/dashboard')
            else:
                return self.redirect('/auth/login')
        else:
            self.messages.append(('This nickname is already registered.',
                'error'))
            return self.get(**kwargs)

        self.messages.append(('A problem occurred. Please correct the '
            'errors listed in the form.', 'error'))
        return self.get(**kwargs)

    @login_required
    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth.user:
            # User is already registered, so don't process the signup form.
            return self.redirect('/dashboard')

        if self.form.validate():
            auth_id = self.auth.session.get('id')
            user = self.auth.create_user(auth_id.split('|')[0], auth_id,email=email_global)
            if user:
                self.auth.login_with_auth_id(user.auth_id, True)
                self.session.add_flash('You are now registered. Welcome!',
                    'success', '_messages')
                return self.redirect('/dashboard')
            else:
                self.messages.append(('This nickname is already registered.',
                    'error'))
                return self.get(**kwargs)

        self.messages.append(('A problem occurred. Please correct the '
            'errors listed in the form.', 'error'))
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return SignupForm(self.request)


class RegisterHandler(BaseHandler):
    def get(self, **kwargs):
        
        if self.auth.user:
            # User is already registered, so don't display the registration form.
            return self.redirect('/dashboard')
        opts = {'continue': self.redirect_path()}
        context = {
            
            'facebook_login_url':   self.url_for('auth/facebook', **opts),
            'friendfeed_login_url': self.url_for('auth/friendfeed', **opts),
            'google_login_url':     self.url_for('auth/google', **opts),
            'twitter_login_url':    self.url_for('auth/twitter', **opts),
            'yahoo_login_url':      self.url_for('auth/yahoo', **opts),
        }
        return self.render_response('register.html',section='register', form=self.form, **context)

    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth.user:
            # User is already registered, so don't process the signup form.
            return self.redirect('/dashboard')

        if self.form.validate():
            username = self.form.username.data
            email = self.form.email.data
            password = self.form.password.data
            password_confirm = self.form.password_confirm.data

            if password != password_confirm:
                self.messages.append(("Password confirmation didn't match.",
                    'error'))
                return self.get(**kwargs)

            auth_id = 'own|%s' % username
            user = self.auth.create_user(username, auth_id, email = email, password=password)
            if user:
                self.auth.login_with_auth_id(user.auth_id, True)
                self.session.add_flash('You are now registered. Welcome!',
                    'success', '_messages')
                return self.redirect(redirect_url)
            else:
                self.messages.append(('This nickname is already registered.',
                    'error'))
                return self.get(**kwargs)

        self.messages.append(('A problem occurred. Please correct the '
            'errors listed in the form.', 'error'))
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return RegistrationForm(self.request)


class FacebookAuthHandler(BaseHandler, FacebookMixin):
    def head(self, **kwargs):
        """Facebook will make a HEAD request before returning a callback."""
        return self.app.response_class('')

    def get(self):
        url = self.redirect_path()

        if self.auth.session:
            # User is already signed in, so redirect back.
            return self.redirect('/dashboard')

        self.session['_continue'] = url

        if self.request.args.get('session', None):
            return self.get_authenticated_user(self._on_auth)

        return self.authenticate_redirect()

    def _on_auth(self, user):
        """
        """
        if not user:
            self.abort(403)

        # try user name, fallback to uid.
        username = user.pop('username', None)
        if not username:
            username = user.pop('uid', '')
        email_global = user.pop('email', None)
        auth_id = 'facebook|%s' % username
        self.auth.login_with_auth_id(auth_id, remember=True,
            session_key=user.get('session_key'))
        return self._on_auth_redirect()


class FriendFeedAuthHandler(BaseHandler, FriendFeedMixin):
    """
    """
    def get(self):
        url = self.redirect_path()

        if self.auth.session:
            # User is already signed in, so redirect back.
            return self.redirect(url)

        self.session['_continue'] = url

        if self.request.args.get('oauth_token', None):
            return self.get_authenticated_user(self._on_auth)

        return self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            self.abort(403)

        auth_id = 'friendfeed|%s' % user.pop('username', '')
        self.auth.login_with_auth_id(auth_id, remember=True,
            access_token=user.get('access_token'))
        return self._on_auth_redirect()


class TwitterAuthHandler(BaseHandler, TwitterMixin):
    def get(self):
        url = self.redirect_path()

        if self.auth.user:
            # User is already signed in, so redirect back.
            return self.redirect(url)

        self.session['_continue'] = url

        if self.request.args.get('oauth_token', None):
            return self.get_authenticated_user(self._on_auth)

        return self.authorize_redirect(callback_uri='/auth/twitter/')

    def _on_auth(self, user):
        if not user:
            self.abort(403)

        auth_id = 'twitter|%s' % user.pop('username', '')
        self.auth.login_with_auth_id(auth_id, remember=True,
            access_token=user.get('access_token'))
        return self._on_auth_redirect()


class GoogleAuthHandler(BaseHandler, GoogleMixin):
    def get(self):
        url = self.redirect_path()

        if self.auth.session:
            # User is already signed in, so redirect back.
            return self.redirect(url)

        self.session['_continue'] = url

        if self.request.args.get('openid.mode', None):
            return self.get_authenticated_user(self._on_auth)

        return self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            self.abort(403)

        auth_id = 'google|%s' % user.pop('email', '')
        self.auth.login_with_auth_id(auth_id, remember=True)
        return self._on_auth_redirect()
