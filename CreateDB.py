import sqlite3
from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('playlistsDB.sqlite')

        return con

    except Error:

        print(Error)


def sql_tables(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT,artist text, genre,len REAL ,path TEXT UNIQUE, UNIQUE(title, artist));")
    cursorObj.execute("CREATE TABLE IF NOT EXISTS playlists(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE);")

    cursorObj.execute("CREATE TABLE IF NOT EXISTS song_playlist(id INTEGER PRIMARY KEY AUTOINCREMENT, song_id INTEGER,playlist_id INTEGER, FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY (playlist_id) REFERENCES playlists (id) ON DELETE CASCADE ON UPDATE CASCADE)")

    con.commit()
    con.close()

sql_tables(sql_connection())
