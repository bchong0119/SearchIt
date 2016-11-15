''' searchit.web - Web Application '''

from searchit.database import Database

import logging
import socket
import sys

import tornado.ioloop
import tornado.web

# Application

class Application(tornado.web.Application):
    DEFAULT_PORT  = 9876
    TEMPLATE_PATH = 'assets/html'

    def __init__(self, port=DEFAULT_PORT):
	tornado.web.Application.__init__(self, debug=True, template_path=Application.TEMPLATE_PATH)
        # TODO: Initialize database and port
        self.logger   = logging.getLogger()
        self.ioloop   = tornado.ioloop.IOLoop.instance()
        self.database = Database()
        self.port     = port

        # TODO: Add Index, Album, Artist, and Track Handlers
        self.add_handlers('', [
            (r'/'          , IndexHandler),
            (r'/artist/(.*)', ArtistHandler),
            (r'/album/(.*)' , AlbumHandler),
            (r'/track/(.*)' , TrackHandler),
        ])        

    def run(self):
        try:
            self.listen(self.port)
        except socket.error as e:
            self.logger.fatal('Unable to listen on {} = {}'.format(self.port, e))
            sys.exit(1)

        self.ioloop.start()

# Handlers

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        table  = self.get_argument('table', '')
        query  = self.get_argument('query', '')

        if table == 'Artists':
            groups= self.application.database.artists('%{}%' .format(query))
            self.render('gallery.html',groups=groups,prefix='artist')
        elif table == 'Albums':
            groups= self.application.database.albums('%{}%' .format(query))
            self.render('gallery.html',groups=groups,prefix='album')
        elif table == 'Tracks':
            groups= self.application.database.tracks('%{}%' .format(query))
            self.render('gallery.html',groups=groups,prefix='track')
        else:
            self.render('index.html')


class ArtistHandler(tornado.web.RequestHandler):
    def get(self, artist_id=None):
        # TODO: Implement Artist Handler
	if artist_id:
	    artist=self.application.database.artist(artist_id)
	    self.render('gallery.html',groups=artist, prefix='album')
	else:
	    artist=self.application.database.artists('')
	    self.render('gallery.html', groups=artist, prefix='artist')

class AlbumHandler(tornado.web.RequestHandler):
    def get(self, album_id=None):
        # TODO: Implement Album Handler
	if album_id:
	    album=self.application.database.album(album_id)
	    self.render('album.html', album=album, prefix='track')
        else:
	    album=self.application.database.albums('')
	    self.render('gallery.html', groups=album, prefix='album')

class TrackHandler(tornado.web.RequestHandler):
    def get(self, track_id=None):
        # TODO: Implement Album Handler
	if track_id:
	    track=self.application.database.track(track_id)
	    self.render('track.html', track=track, prefix='track')
	else:
	    track=self.application.database.tracks('')
	    self.render('gallery.html', groups=track, prefix='track')

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
