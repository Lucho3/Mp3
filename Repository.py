import sqlite3
from sqlite3 import Error
from Models import *


def create_new_empty_playlist(playlist_name):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO playlists(name) VALUES(?)",(playlist_name,))
    except:
        return None
    conn.commit()
    return cur.lastrowid

def get_all_playlists():
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    
    cur = conn.cursor()
    try:
        return cur.execute("SELECT * FROM playlists").fetchall()
    except:
        return None

def get_all_songs_for_playlist(playlist_name):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        query=str.format('SELECT * FROM songs where id IN (SELECT song_id FROM song_playlist WHERE playlist_id=(SELECT id FROM playlists WHERE name="{}"))',playlist_name)
        return cur.execute(query).fetchall()
    except:
        return None

def insert_song(sg):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO songs (title,artist,genre,len,path) VALUES(?,?,?,?,?)",(sg.title,sg.artist,sg.genre,sg.len,sg.path,))
    except:
        return None
    conn.commit()
    return cur.lastrowid

def insert_song_into_playlist(song_id,playlist_id):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO song_playlist (song_id,playlist_id) VALUES(?,?)",(song_id,playlist_id,))
    except:
        return None
    conn.commit()

def get_id_of_song(title):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        return cur.execute('SELECT id FROM songs where title=?',(title,)).fetchone()[0]
    except:
        return None

def create_new_playlist(playlist):
    playlist_id=create_new_empty_playlist(playlist.name)
    if playlist_id==None:
        return

    for song in playlist.list_of_songs:
        song_id=insert_song(song)
        if song_id==None:
            song_id=get_id_of_song(song.title)
        insert_song_into_playlist(song_id,playlist_id)
    

    
    

