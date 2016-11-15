''' searchit.database - SQLite Database '''

import logging
import sqlite3
import yaml

# Database

class Database(object):
    PORT=8888
    SQLITE_PATH = 'searchit.db'
    YAML_PATH   = 'assets/yaml/data.yaml'

    def __init__(self, data=YAML_PATH, path=SQLITE_PATH):
        # TODO: Set instance variables and call _create_tables and _load_tables
       self.logger = logging.getLogger()
       self.data   = data
       self.path   = path
       self.conn   = sqlite3.connect(self.path)
       self._create_tables()
       self._load_tables()
       
       
    def _create_tables(self):
        # TODO: Create Artist, Album, and Track tables
        with self.conn:
            cursor = self.conn.cursor()
            artists_sql = '''
            CREATE Table IF NOT EXISTS Artists(
                ArtistID	INTEGER	NOT NULL,
                Name		TEXT    NOT NULL,
                Image		TEXT    NOT NULL,
                PRIMARY KEY(ArtistID)
            )'''
            albums_sql = '''
            CREATE TABLE IF NOT EXISTS Albums(
                ArtistID	INTEGER	NOT NULL,
		AlbumID  	INTEGER NOT NULL,
                Name   		TEXT    NOT NULL,
                Image   	TEXT     NOT NULL,
                PRIMARY KEY(ArtistID, Name),
                FOREIGN KEY(ArtistID) References Artists(ArtistID)
            )'''
            tracks_sql = '''
            CREATE TABLE IF NOT EXISTS Tracks(
                AlbumID     INTEGER     NOT NULL,
                TrackID     INTEGER     NOT NULL,
                Number      INTEGER     NOT NULL,
                Name        TEXT        NOT NULL,   
                PRIMARY KEY(TRACKID),
                FOREIGN KEY(AlbumID) References Albums(AlbumID)
            )'''

            cursor.execute(artists_sql)
            self.logger.info('Created Artists Table')

            cursor.execute(albums_sql)
            self.logger.info('Created Albums Table')

            cursor.execute(tracks_sql)
            self.logger.info('Created Tracks Table')

    def _load_tables(self):
        # TODO: Insert Artist, Album, and Track tables from YAML

	with self.conn: 
	    cursor = self.conn.cursor()
	    artists_sql = 'INSERT OR REPLACE INTO Artists(ArtistID, Name, Image) VALUES (?, ?, ?)'
	    album_sql 	= 'INSERT OR REPLACE INTO Albums(ArtistID, AlbumID, Name, Image) VALUES (?, ?, ?, ?)'
	    track_sql 	= 'INSERT OR REPLACE INTO Tracks(AlbumID, TrackID, Number, Name) VALUES (?, ?, ?, ?)'
	    artist_id=0
	    album_id=0
	    track_id=0
	    for artist in yaml.load(open(self.data)):
		artist_id=artist_id+1
		cursor.execute(artists_sql, (artist_id, artist['name'], artist['image']))
		self.logger.debug('Added Artist: id={}, name={}'.format(artist_id, artist['name']))
		for album in artist['albums']:
		    album_id=album_id+1	
		    cursor.execute(album_sql, (artist_id, album_id, album['name'], album['image'])) 
		    number=0
		    for track in album['tracks']:
			track_id=track_id+1
			number=number+1
			cursor.execute(track_sql, (album_id, track_id, number, track))
			
    def artists(self, artist):
        # TODO: Select artists matching query
        with self.conn:
            cursor      = self.conn.cursor()
            artists_sql = '''
            SELECT Artists.ArtistID, Name, Image
            FROM Artists
            WHERE Name Like (?)
            '''
            return cursor.execute(artists_sql, ('%'+artist+'%',))

    def artist(self, artist_id=None):
        # TODO: Select artist albums
        with self.conn:
            cursor      = self.conn.cursor()
            artists_sql = '''
            SELECT Albums.AlbumID, Name, Image, GROUP_CONCAT(Albums.AlbumID) AS Albums
            FROM Albums
            WHERE ArtistID LIKE (?)
            '''
            return cursor.execute(artists_sql, (artist_id,))

    def albums(self, album):
        # TODO: Select albums matching query
        with self.conn:
            cursor      = self.conn.cursor()
            album_sql   = '''
            SELECT Albums.AlbumID, Name, Image
            FROM Albums
            WHERE Name Like (?)
            '''
            return cursor.execute(album_sql, ('%'+album+'%',))

    def album(self, album_id=None):
        # TODO: Select specific album
        with self.conn:
            cursor      = self.conn.cursor()
            album_sql = '''
            SELECT TrackID, Number, Name
	    FROM Tracks
            WHERE AlbumID LIKE (?)
            '''
            return cursor.execute(album_sql, (album_id,))

    def tracks(self, track):
        # TODO: Select tracks matching query
        with self.conn:
            cursor      = self.conn.cursor()
            track_sql   = '''
            SELECT TrackID, Tracks.Name, Albums.Image
            FROM Tracks
            JOIN Albums ON Albums.AlbumID=Tracks.AlbumID
            WHERE Tracks.Name LIKE (?)
            '''
            return cursor.execute(track_sql, ('%'+track+'%',))

    def track(self, track_id=None):
        # TODO: Select specific track
        with self.conn:
            cursor      = self.conn.cursor()
            track_sql   = '''
            SELECT TrackID, Artists.ArtistID, Artists.Name, Albums.AlbumID, Albums.Name, Number, Tracks.Name
            FROM Tracks
            JOIN Albums ON Tracks.AlbumID=Albums.AlbumID
            JOIN Artists ON Albums.ArtistID=Artists.ArtistID
            WHERE TrackID LIKE (?)
            '''
            return cursor.execute(track_sql, (track_id,))
# vim: set sts=4 sw=4 ts=8 expandtab ft=python:

