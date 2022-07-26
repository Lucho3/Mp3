#Model for songs
class Song:
    def __init__(self,id,title,artist,genre,len,path):
        self.id=id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.len = len
        self.path = path
        self.is_paused=True

#Model for playlists
class Playlist:
    def __init__(self,id,name):
        self.id=id
        self.name = name
        self.list_of_songs=list()