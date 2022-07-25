import time
from tkinter import *
from tkinter import filedialog
import pygame
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from lyricsgenius import Genius
from Models import *
from Repository import *
from View import *

class ControllerApp():
    def __init__(self, view):
        self.view = view
        self.list_of_songs=list()
        self.current_song_id=None
        self.list_of_playlists=list()
        self.current_playlist_id=None
        self.is_next=False



    def eject_playlist(self):
        if self.current_playlist_id!=None:
            if self.current_song_id!=None:
                self.stop()
            self.current_playlist_id=None
            self.list_of_songs =list()
            self.view.tab1_main.songlist_frame.song_list.delete(0,END)
            self.view.tab2_playlists.pl_songs_frame.list.delete(0,END)
            self.view.status_frame.status_bar_playlist.config(text="No Playlist currently loaded")
        else:
            self.view.popup("You must load a playlist!")




    def delete_playlist(self):
        if self.current_playlist_id!=None:
            name=self.list_of_playlists[self.current_playlist_id].name
            delete_playlist_from_db(name)
            self.view.tab2_playlists.playlist_frame.list.delete(self.current_playlist_id)
            #trqbva da go opr
            self.eject_playlist()
        else:
            self.view.popup("You must load a playlist!")
            

    def get_and_display_playlists(self):
        for playlist in get_all_playlists():
            self.list_of_playlists.append(Playlist(playlist[0]-1,playlist[1]))


        for playlist in self.list_of_playlists:
            for song in get_all_songs_for_playlist(playlist.name):
                playlist.list_of_songs.append(Song(song[0],song[1],song[2],song[3],song[4],song[5]))

            self.view.tab2_playlists.playlist_frame.list.insert(END,playlist.name)

    def display_songs_in_playlist(self,x):
        if len(self.view.tab2_playlists.playlist_frame.list.curselection())>0:
            playlist=self.list_of_playlists[int(self.view.tab2_playlists.playlist_frame.list.curselection()[0])]
            self.view.tab2_playlists.pl_songs_frame.list.delete(0,END)
            for song in playlist.list_of_songs:
                self.view.tab2_playlists.pl_songs_frame.list.insert(END,song.title)

    def load_playlist(self):
        if len(self.view.tab2_playlists.playlist_frame.list.curselection())>0:
            self.current_playlist_id=int(self.view.tab2_playlists.playlist_frame.list.curselection()[0])
            self.list_of_songs=self.list_of_playlists[self.current_playlist_id].list_of_songs

            self.view.tab1_main.songlist_frame.song_list.delete(0,END)
            for song in self.list_of_songs:
                self.view.tab1_main.songlist_frame.song_list.insert(END,song.title)
            self.view.tab2_playlists.pl_songs_frame.list.delete(0,END)
            self.view.status_frame.status_bar_playlist.config(text=f'Playlist Loaded: {self.list_of_playlists[self.current_playlist_id].name} ')


    def insert_playlist_in_db(self,name,window):
        if name!='' and name!=None:
            pl=Playlist(self.list_of_playlists.count,name)  
            pl.list_of_songs=self.list_of_songs[:]
            if create_new_playlist(pl)!=None:
                self.list_of_playlists.append(pl)
                self.view.tab2_playlists.playlist_frame.list.insert(END,name)
                window.destroy()
            else:
                self.view.popup("The name is already taken!")
        else:
            self.view.popup("You must enter name!")
        


    def edit_playlist(self):
        if self.current_playlist_id!=None:
            update_playlist_db(self.list_of_playlists[self.current_playlist_id])
            self.view.tab2_playlists.pl_songs_frame.list.delete(0,END)
            self.view.popup("OK")
        else:
            self.view.popup("You must load a playlist!")

    def get_song(self,song_path):
        try:
            id=int(self.view.tab1_main.songlist_frame.song_list.size())
        except:
            id=None
        try:
            title=EasyID3(song_path)["title"][0]
        except:
            title=None
        try:
            artist=EasyID3(song_path)["artist"][0]
        except:
            artist=None
        try:
            genre=EasyID3(song_path)["genre"][0]
        except:
            genre=None
        try:
            song_length=MP3(song_path).info.length
        except:
            song_length=0

        sg =Song(id,title,artist,genre,song_length,song_path)

        return sg

    def get_song_lyrics(self):
        if self.view.tab1_main.songlist_frame.song_list.size():
            self.view.tab1_main.lyrics_frame.song_lyrics['state']=NORMAL
            genius = Genius("yKvIvpLhWT30u1NJ1zDoLd67-1MTRy-aDrE28RNo7IjPZUXvBMfoAyqr4EtY-pps")
            song_lyr = genius.search_song(self.list_of_songs[self.current_song_id].title,self.list_of_songs[self.current_song_id].artist).lyrics[:-5]
            while song_lyr[-1].isdigit():
                song_lyr=song_lyr[:-1]

            if song_lyr!=None:
                self.view.tab1_main.lyrics_frame.song_lyrics.delete("1.0",END)
                self.view.tab1_main.lyrics_frame.song_lyrics.insert("1.0",song_lyr)
            self.view.tab1_main.lyrics_frame.song_lyrics['state']=DISABLED

    def add_song(self):
        song=filedialog.askopenfilename(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
        song_name = os.path.basename(song)
        song_name=song_name.replace(".mp3"," ")

        song=self.get_song(os.path.abspath(song))

        for song_saved in self.list_of_songs:
            if song.title==song_saved.title and song.artist==song_saved.artist:
                self.view.popup("Song Already In Playlist!")
                return
        self.list_of_songs.append(song)
        self.view.tab1_main.songlist_frame.song_list.insert(END,song_name)

    def add_songs(self):
        songs=filedialog.askopenfilenames(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
        list_of_added_songs=[self.get_song(os.path.abspath(song)) for song in songs]

        for added_song in list_of_added_songs:
            flag=True
            for song_in_playlist in self.list_of_songs:
                if added_song.title==song_in_playlist.title and added_song.artist==song_in_playlist.artist:
                    flag=False
                    break
            if flag:
                    self.list_of_songs.append(added_song)
                    song_name = os.path.basename(added_song.path)
                    song_name.replace(".mp3"," ")
                    self.view.tab1_main.songlist_frame.song_list.insert(END,song_name)



           

    def volume(self,slide_position):
        pygame.mixer.music.set_volume(self.view.tab1_main.volume_frame.volume_slider.get())

        current_volume=float(slide_position)*100
        if current_volume<1:
            self.view.tab1_main.volume_frame.volume_lbl.config(image=self.view.list_of_volume_pics[0])
        elif current_volume>=1 and current_volume<20:
            self.view.tab1_main.volume_frame.volume_lbl.config(image=self.view.list_of_volume_pics[1])
        elif current_volume>=20 and current_volume<40:
            self.view.tab1_main.volume_frame.volume_lbl.config(image=self.view.list_of_volume_pics[2])
        elif current_volume>=40 and current_volume<60:
            self.view.tab1_main.volume_frame.volume_lbl.config(image=self.view.list_of_volume_pics[3])
        elif current_volume>=60 and current_volume<80:
            self.view.tab1_main.volume_frame.volume_lbl.config(image=self.view.list_of_volume_pics[4])
        else:
            self.view.tab1_main.volume_frame.volume_lbl.config(image=self.view.list_of_volume_pics[5])

    def slide(self,slide_position):
        if self.current_song_id!=None:
            pygame.mixer.music.load(self.list_of_songs[self.current_song_id].path)
            pygame.mixer.music.play(loops=0,start=int(self.view.tab1_main.music_slider.get()))
        else:
            self.view.tab1_main.music_slider.config(value=0)  

    def play_time(self):
        if self.current_song_id!=None:
            if self.list_of_songs[self.current_song_id].is_paused==False:
                current_time=pygame.mixer.music.get_pos()/1000

                converted_time_elapsed=time.strftime("%M:%S",time.gmtime(current_time))

                song_length=self.list_of_songs[self.current_song_id].len
                converted_time_song=time.strftime("%M:%S",time.gmtime(song_length))

                current_time+=1
                if int(self.view.tab1_main.music_slider.get())==int(song_length):
                    self.next_song("next")
                    
                elif int(self.view.tab1_main.music_slider.get())==int(current_time):
                    self.view.tab1_main.music_slider.config(to=int(song_length),value=int(current_time))
                else:
                    self.view.tab1_main.music_slider.config(to=int(song_length),value=int(self.view.tab1_main.music_slider.get()))
                    converted_time_elapsed=time.strftime("%M:%S",time.gmtime(int(self.view.tab1_main.music_slider.get())))
                    self.view.status_frame.status_bar.config(text=f'{self.list_of_songs[self.current_song_id].title} - {self.list_of_songs[self.current_song_id].artist}/Time Elapsed: {converted_time_elapsed} of {converted_time_song} ')
                    next_time=int(self.view.tab1_main.music_slider.get())+1
                    self.view.tab1_main.music_slider.config(value=next_time)      
            if self.is_next==False:    
                self.view.status_frame.status_bar.after(1000,self.play_time)
        self.is_next=False


    def delete_song(self):
        if self.view.tab1_main.songlist_frame.song_list.size() and len(self.view.tab1_main.songlist_frame.song_list.curselection())>0:
            if self.current_playlist_id!=None:
                self.list_of_playlists[self.current_playlist_id].list_of_songs.pop(int(self.view.tab1_main.songlist_frame.song_list.curselection()[0]))
            else:
                self.list_of_songs.pop(int(self.view.tab1_main.songlist_frame.song_list.curselection()[0]))

            self.view.tab1_main.songlist_frame.song_list.delete(ANCHOR)

            if self.current_song_id!=None:
                self.stop()
        else:
            self.view.popup("You must select a song!")

    def delete_all_songs(self):
        if self.view.tab1_main.songlist_frame.song_list.size():
            if self.current_song_id!=None:
                self.stop()
            if self.current_playlist_id!=None:
                self.list_of_playlists[self.current_playlist_id].list_of_songs=list()
            self.view.tab1_main.songlist_frame.song_list.delete(0,END)
            self.list_of_songs=list()


    def play(self):
        if self.view.tab1_main.songlist_frame.song_list.size():
            self.view.tab1_main.buttons_frame.play_btn.configure(image=self.view.list_of_buttons[3])
            self.view.tab1_main.music_slider.config(state=NORMAL)
            
            if self.current_song_id!=None:
                pygame.mixer.music.unpause()
                self.list_of_songs[self.current_song_id].is_paused=False
            else:
                if len(self.view.tab1_main.songlist_frame.song_list.curselection())==0:
                    self.view.tab1_main.songlist_frame.song_list.activate(0)
                    self.view.tab1_main.songlist_frame.song_list.selection_set(0,last=None)
                self.current_song_id=int(self.view.tab1_main.songlist_frame.song_list.curselection()[0])
                pygame.mixer.music.load(self.list_of_songs[self.current_song_id].path)
                pygame.mixer.music.play(loops=0)
                self.list_of_songs[self.current_song_id].is_paused=False
                pygame.mixer.music.set_volume(self.view.tab1_main.volume_frame.volume_slider.get())
                self.play_time()
                self.get_song_lyrics()
                
    def stop(self):
        if self.view.tab1_main.songlist_frame.song_list.size():
            self.is_next=False
            pygame.mixer.music.stop()
            self.view.tab1_main.songlist_frame.song_list.select_clear(ACTIVE)
            self.view.tab1_main.songlist_frame.song_list.selection_clear(0, 'end')
            self.list_of_songs[self.current_song_id].is_paused=True
            self.view.tab1_main.buttons_frame.play_btn.configure(image=self.view.list_of_buttons[2])
            self.view.status_frame.status_bar.config(text="No Song Currently Playing ")
            self.view.tab1_main.music_slider.config(value=0)
            self.current_song_id=None
            self.view.tab1_main.music_slider.config(state=DISABLED)

            self.view.tab1_main.lyrics_frame.song_lyrics.config(state=NORMAL)
            self.view.tab1_main.lyrics_frame.song_lyrics.delete("1.0",END)
            self.view.tab1_main.lyrics_frame.song_lyrics.insert("1.0","No lyrics currently found!")
            self.view.tab1_main.lyrics_frame.song_lyrics.config(state=DISABLED)

    def pause(self):
        if self.view.tab1_main.songlist_frame.song_list.size():
            self.view.tab1_main.music_slider.config(state=DISABLED)
            pygame.mixer.music.pause()
            self.view.tab1_main.buttons_frame.play_btn.configure(image=self.view.list_of_buttons[2])
            self.list_of_songs[self.current_song_id].is_paused=True


    def next_song(self,where_to_go):
        if self.view.tab1_main.songlist_frame.song_list.size():
            if self.current_song_id!=None:
                 self.is_next=True
            self.view.tab1_main.music_slider.config(state=NORMAL)
            self.view.tab1_main.buttons_frame.play_btn.configure(image=self.view.list_of_buttons[3])
            
            if where_to_go=="next":
                self.current_song_id=0
                if len(self.view.tab1_main.songlist_frame.song_list.curselection())>0 and self.view.tab1_main.songlist_frame.song_list.curselection()[0]<self.view.tab1_main.songlist_frame.song_list.size()-1:
                    self.current_song_id=self.view.tab1_main.songlist_frame.song_list.curselection()[0]+1
            else:
                self.current_song_id=self.view.tab1_main.songlist_frame.song_list.size()-1
                if len(self.view.tab1_main.songlist_frame.song_list.curselection())>0 and self.view.tab1_main.songlist_frame.song_list.curselection()[0]>0:
                    self.current_song_id=self.view.tab1_main.songlist_frame.song_list.curselection()[0]-1
            
            self.list_of_songs[self.current_song_id].is_paused=False
            pygame.mixer.music.load(self.list_of_songs[self.current_song_id].path)
            pygame.mixer.music.play(loops=0)
            self.view.tab1_main.music_slider.config(value=0) 
            self.view.tab1_main.songlist_frame.song_list.select_clear(0,END)
            self.view.tab1_main.songlist_frame.song_list.activate(self.current_song_id)
            self.view.tab1_main.songlist_frame.song_list.selection_set(self.current_song_id,last=None)
            
            self.play_time()
            self.get_song_lyrics()
    
'''
def next_song(self,where_to_go):
        if self.view.tab1_main.songlist_frame.song_list.size():
            if self.current_song_id!=None:
                 self.is_next=True
            self.view.tab1_main.music_slider.config(state=NORMAL)
            self.view.tab1_main.buttons_frame.play_btn.configure(image=self.view.list_of_buttons[3])
            
            if self.current_song_id==None:
                self.current_song_id=0
            if where_to_go=="next":
                self.current_song_id+=1                            
                if self.current_song_id>len(self.list_of_songs)-1 and self.current_song_id!=0:
                    self.current_song_id=0
            else:
                self.current_song_id=len(self.list_of_songs)-1
                if  self.current_song_id>0:
                    self.current_song_id=self.current_song_id-1
                    
            
            self.list_of_songs[self.current_song_id].is_paused=False
            pygame.mixer.music.load(self.list_of_songs[self.current_song_id].path)
            pygame.mixer.music.play(loops=0)
            self.view.tab1_main.music_slider.config(value=0) 
            self.view.tab1_main.songlist_frame.song_list.select_clear(0,END)
            self.view.tab1_main.songlist_frame.song_list.activate(self.current_song_id)
            self.view.tab1_main.songlist_frame.song_list.selection_set(self.current_song_id,last=None)
            
            self.play_time()
            self.get_song_lyrics()

'''