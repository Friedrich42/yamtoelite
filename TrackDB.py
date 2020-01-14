import sqlite3

from functions import *


class Track:
    def __init__(self, id_of_song, song_name, artists, album_id, local_path):
        self.id_of_song = id_of_song
        self.song_name = song_name.replace("/", " ")
        self.artists = artists.replace("/", " ")
        self.album_id = album_id
        self.local_path = local_path


class TrackDB:
    def __init__(self, db_name=f'songs.db', db_name_prefix="", table_name='songs'):
        """ initializing db. requires no parameters.
            the first optional parameter is db_name.
            the second optional parameter is db_name_prefix. "" by default
            the third optional parameter is table_name. 'all_users' by default
        """
        self.connection = None
        self.db_name = db_name if db_name_prefix == "" else db_name_prefix + "-" + db_name
        self.table_name = table_name

        self.connect()  # connects to db
        # self.connection.row_factory = sqlite3.Row
        self.create_table()  # creates new table

    def connect(self):
        """ connects to database by name given on initialization """
        try:
            if not os.path.exists('db'):
                os.makedirs('db')  # if path not exists, creates the folder
            os.chdir('db')  # cd to db folder
            connection = sqlite3.connect(self.db_name, check_same_thread=False)  # makes a connection to db
            self.connection = connection  # saves connection as class variable
            os.chdir('..')  # cd ..
            if connection is None:
                raise Exception("Connection to db failed")  # if not connected, raise an error
        except Exception as e:
            return log_error(e)  # log and exit if error is present

    def disconnect(self):
        """ closes connection """
        self.connection.close()  # close the connection

    def create_table(self):
        """ if table doesn't exist creates new table with the name, represented by class variable 'table_name' """
        try:
            cursor = self.connection.cursor()  # creates a new cursor
            cursor.execute(""" CREATE TABLE IF NOT EXISTS {} (
                                pk INTEGER PRIMARY KEY,
                                id_of_song INTEGER NOT NULL,
                                song_name TEXT NOT NULL,
                                artists TEXT NOT NULL,
                                album_id INTEGER,
                                local_path TEXT
                            );""".format(self.table_name))  # creates a table
        except Exception as e:
            return log_error(e)  # log and exit if error is present

    def add_song(self, song: Track):
        try:
            song = (int(song.id_of_song), song.song_name, song.artists, int(song.album_id), song.local_path)

            query = """ INSERT INTO {}
                            (id_of_song, song_name, artists, album_id, local_path)
                            VALUES (?,?,?,?,?) """.format(self.table_name)  # sets a query

            cursor = self.connection.cursor()  # creates a new cursor
            cursor.execute(query, song)  # executes sql
            self.connection.commit()  # commit
            return "ok"
        except Exception as e:
            return log_error(e)  # log and exit if error is present

    def get_song(self, id_of_song):
        try:
            cursor = self.connection.cursor()  # creates a new cursor
            cursor.execute(""" SELECT * FROM {} WHERE id_of_song=(?); """.format(self.table_name), (id_of_song,))
            song = cursor.fetchone()  # fetch it
            if song:
                return Track(*song[1:])
            else:
                return None
        except Exception as e:
            return log_error(e)  # log and exit if error is present

    def get_songs(self, limit=None):
        try:
            limit = "" if not limit else f"LIMIT {int(limit)}"
            cursor = self.connection.cursor()
            cursor.execute(""" SELECT * FROM {} {} ORDER BY pk; """.format(self.table_name, limit))
            return [Track(*song_tup[1:]) for song_tup in cursor.fetchall()]
        except Exception as e:
            return log_error(e)
