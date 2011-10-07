# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy import Rule

rules = [
    Rule('/', endpoint='home', handler='handlers.UserHandler.RegisterHandler'),
    Rule('/auth/login', endpoint='auth/login', handler='handlers.UserHandler.LoginHandler'),
    Rule('/artist', endpoint='artist', handler='handlers.LastFmHandler.LastFmSearchHandler'),
    Rule('/dashboard', endpoint='dashboard', handler='handlers.DashboardHandler.DashboardHandler'),
    Rule('/create-event', endpoint='create-event', handler='handlers.EventHandler.CreateEventHandler'),
    Rule('/auth/logout', endpoint='auth/logout', handler='handlers.UserHandler.LogoutHandler'),
    Rule('/auth/signup', endpoint='auth/signup', handler='handlers.UserHandler.SignupHandler'),
    Rule('/event/file/<key>', endpoint='event-file', handler='handlers.EventHandler.EventFileHandler'),
    Rule('/auth/facebook/', endpoint='auth/facebook', handler='handlers.UserHandler.FacebookAuthHandler'),
    Rule('/auth/friendfeed/', endpoint='auth/friendfeed', handler='handlers.UserHandler.FriendFeedAuthHandler'),
    Rule('/auth/google/', endpoint='auth/google', handler='handlers.UserHandler.GoogleAuthHandler'),
    Rule('/auth/twitter/', endpoint='auth/twitter', handler='handlers.UserHandler.TwitterAuthHandler'),
    Rule('/auth/yahoo/', endpoint='auth/yahoo', handler='handlers.UserHandler.YahooAuthHandler'),

    Rule('/content', endpoint='content/index', handler='handlers.UserHandler.ContentHandler'),
]
