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
        return get_id_of_song(sg.title,sg.artist)
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

def get_id_of_song(title,artist):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        return cur.execute('SELECT id FROM songs where title=? and artist=?',(title,artist,)).fetchone()[0]
    except:
        return None

def create_new_playlist(playlist):
    playlist_id=create_new_empty_playlist(playlist.name)
    if playlist_id==None:
        return None

    if len(playlist.list_of_songs)>0:
        for song in playlist.list_of_songs:
            song_id=insert_song(song)
            insert_song_into_playlist(song_id,playlist_id)
            
    return playlist_id
    
def remove_song_from_playlist(song_id,playlist_id):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM song_playlist WHERE id =(SELECT MIN(id) FROM song_playlist WHERE song_id=? AND playlist_id=?);',(song_id,playlist_id,))
    except:
        return None
    conn.commit()

def get_playlist_id(playlist_name):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        return cur.execute('SELECT id FROM playlists where name=?',(playlist_name,)).fetchone()[0]
    except:
        return None

def update_playlist_db(playlist):
    all_songs=get_all_songs_for_playlist(playlist.name)
    playlist_id=get_playlist_id(playlist.name)
    all_songs_id=list()
    for el in all_songs:
        all_songs_id.append(el[0])
    
    view_songs_id=list()
    for song in playlist.list_of_songs:
        view_songs_id.append(insert_song(song))

    for song_id in all_songs_id:
        if song_id not in view_songs_id:
            remove_song_from_playlist(song_id,playlist_id)

    for song_id in view_songs_id:
        if song_id not in all_songs_id:
            insert_song_into_playlist(song_id,playlist_id)

def delete_playlist_from_db(playlist_name):
    conn = None
    try:
        conn = sqlite3.connect("playlistsDB.sqlite")
    except Error as e:
        print(e)

    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM playlists WHERE name=?;',(playlist_name,))
    except:
        return None
    conn.commit()
