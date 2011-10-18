'''
Created on Sep 29, 2011

@author: Alexander
'''
from UserHandler import BaseHandler
from tipfy.auth.facebook import FacebookMixin


class FacebookInviteHandler(BaseHandler, FacebookMixin):
    def head(self, **kwargs):
        """Facebook will make a HEAD request before returning a callback."""
        return self.app.response_class('')

    def get(self):
        url = self.redirect_path()

        if self.auth.session:
            # User is already signed in, so redirect back.
            return self.redirect('/event/'+self.request.args.get('event'))

        self.session['_continue'] = url

        if self.request.args.get('session', None):
            return self.get_authenticated_user(self._on_auth)

        return self.authenticate_redirect(callback_uri='/auth/invite/facebook/?event='+self.request.args.get('event'))

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
        return self._on_auth_redirect_invite(self.request.args.get('event'))