# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy import Rule

rules = [
    Rule('/', endpoint='home', handler='handlers.UserHandler.HomeHandler'),
    Rule('/auth/login', endpoint='auth/login', handler='handlers.UserHandler.LoginHandler'),
    Rule('/auth/logout', endpoint='auth/logout', handler='handlers.UserHandler.LogoutHandler'),
    Rule('/auth/signup', endpoint='auth/signup', handler='handlers.UserHandler.SignupHandler'),
    Rule('/auth/register', endpoint='auth/register', handler='handlers.UserHandler.RegisterHandler'),

    Rule('/auth/facebook/', endpoint='auth/facebook', handler='handlers.UserHandler.FacebookAuthHandler'),
    Rule('/auth/friendfeed/', endpoint='auth/friendfeed', handler='handlers.UserHandler.FriendFeedAuthHandler'),
    Rule('/auth/google/', endpoint='auth/google', handler='handlers.UserHandler.GoogleAuthHandler'),
    Rule('/auth/twitter/', endpoint='auth/twitter', handler='handlers.UserHandler.TwitterAuthHandler'),
    Rule('/auth/yahoo/', endpoint='auth/yahoo', handler='handlers.UserHandler.YahooAuthHandler'),

    Rule('/content', endpoint='content/index', handler='handlers.UserHandler.ContentHandler'),
]
