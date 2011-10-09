# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy import Rule

rules = [
    Rule('/', endpoint='home', handler='handlers.UserHandler.RegisterHandler'),
    Rule('/auth/login', endpoint='auth/login', handler='handlers.UserHandler.LoginHandler'),
    Rule('/artist', endpoint='artist', handler='handlers.LastFmHandler.LastFmSearchHandler'),
    Rule('/artist-json', endpoint='artist-json', handler='handlers.LastFmHandler.GetArtistHandler'),
    Rule('/dashboard', endpoint='dashboard', handler='handlers.DashboardHandler.DashboardHandler'),
    Rule('/create-event', endpoint='create-event', handler='handlers.EventHandler.CreateEventHandler'),
    Rule('/task/mail', endpoint='/task/mail', handler='handlers.MailHandler.MailSender'),
    Rule('/event/invitation/<key>', endpoint='event-validate', handler='handlers.EventHandler.EventValidateUserHandler'),
    Rule('/setlist/update', endpoint='event', handler='handlers.SetListHandler.SetListHandler'),
    Rule('/event/<key>', endpoint='event', handler='handlers.EventHandler.EventHandler'),
    Rule('/upload-song', endpoint='upload-song', handler='handlers.SongHandler.CreateSongHandler'),
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
