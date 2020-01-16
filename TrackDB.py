import sqlite3

from functions import *

DB_DIR = "db"


class Track:
    def __init__(self, id_of_song, song_name, artists, album_id, local_path):
        self.id_of_song = id_of_song
        self.song_name = song_name.replace("/", " ")
        self.artists = artists.replace("/", " ")
        self.album_id = album_id
        self.local_path = local_path


class TrackDB:
    def __init__(self, db_name=f'songs.db', db_name_prefix="", table_name='songs'):
        """
        initializing db. requires no parameters.

        @param db_name: 'songs.db' by default
        @param db_name_prefix: prefix before db_name. '' by default
        @param table_name: table name is 'songs' by default
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
            with in_dir(DB_DIR):
                connection = sqlite3.connect(self.db_name, check_same_thread=False)  # makes a connection to db
                self.connection = connection  # saves connection as class variable
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

    def add_song(self, song: Track, table_name=None):
        """
        @param song: Track object should be given as parameter
        @param table_name: by default using self.table_name
        @return: 'ok' if all is ok, error otherwise
        adds one record to current database. requires Track object as parameter
        the first parameter is song: Track
        the second parameter is table_name. By default it equals to self.table_name
        """

        table_name = self.table_name if not table_name else table_name

        try:
            song = (int(song.id_of_song), song.song_name, song.artists, int(song.album_id), song.local_path)

            query = """ INSERT INTO {}
                            (id_of_song, song_name, artists, album_id, local_path)
                            VALUES (?,?,?,?,?) """.format(table_name)  # sets a query

            cursor = self.connection.cursor()  # creates a new cursor
            cursor.execute(query, song)  # executes sql
            self.connection.commit()  # commit
            return "ok"
        except Exception as e:
            return log_error(e)  # log and exit if error is present

    def get_song(self, id_of_song, table_name=None):
        """
        @param id_of_song: id of song that you want to get from database
        @param table_name: by default using self.table_name
        @return: Track object is returned if song is present, None otherwise
        """

        table_name = self.table_name if not table_name else table_name

        try:
            cursor = self.connection.cursor()  # creates a new cursor
            cursor.execute(""" SELECT * FROM {} WHERE id_of_song=(?); """.format(table_name), (id_of_song,))
            song = cursor.fetchone()  # fetch it
            if song:
                return Track(*song[1:])
            else:
                return None
        except Exception as e:
            return log_error(e)  # log and exit if error is present

    def get_all_songs(self, limit=None, table_name=None):
        """
        @param limit: limit of returned values
        @param table_name: by default using self.table_name
        @return: returns list of Track objects
        """

        table_name = self.table_name if not table_name else table_name

        try:
            limit = "" if not limit else f"LIMIT {int(limit)}"
            cursor = self.connection.cursor()
            cursor.execute(""" SELECT * FROM {} {} ORDER BY pk; """.format(table_name, limit))
            return [Track(*song_tup[1:]) for song_tup in cursor.fetchall()]
        except Exception as e:
            return log_error(e)
