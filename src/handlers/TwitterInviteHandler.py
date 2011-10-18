'''
Created on Sep 29, 2011

@author: Alexander
'''
from UserHandler import BaseHandler
from tipfy.auth.twitter import TwitterMixin


class TwitterInviteHandler(BaseHandler, TwitterMixin):
    
    
    def get(self):
        url = self.redirect_path()

        if self.auth.user:
            # User is already signed in, so redirect back.
            return self.redirect('/event/'+self.request.args.get('event'))

        self.session['_continue'] = url

        if self.request.args.get('oauth_token', None):
            return self.get_authenticated_user(self._on_auth)

        return self.authorize_redirect(callback_uri='/auth/invite/twitter/?event='+self.request.args.get('event'))

    def _on_auth(self, user):
        if not user:
            self.abort(403)

        auth_id = 'twitter|%s' % user.pop('username', '')
        self.auth.login_with_auth_id(auth_id, remember=True,
            access_token=user.get('access_token'))
        return self._on_auth_redirect_invite(self.request.args.get('event'))