import time
from tkinter import *
from tkinter import filedialog
import pygame
from tkinter import ttk
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from tkinter import scrolledtext
from lyricsgenius import Genius
from Models import *
from Repository import *

#functions

global list_of_songs
list_of_songs =list()

global current_song_id
current_song_id=None

global list_of_playlists
list_of_playlists =list()

global current_playlist_id
current_playlist_id=None

def eject_playlist():
    global current_playlist_id
    if current_playlist_id!=None:
        global current_song_id
        global list_of_songs
        if current_song_id!=None:
            stop()
        current_playlist_id=None
        list_of_songs =list()
        song_list.delete(0,END)
        songs_playlist_list.delete(0,END)
        status_bar_playlist.config(text="No Playlist currently loaded")
    else:
        popup("You must load a playlist!")

def popup(text):
    pop=Tk()
    pop.title("Error")
    pop.configure(background='white')
    e = Label(pop,text=text,background='white')
    e.grid(row=0,column=0,padx=10,pady=10)
    close_btn=ttk.Button(pop,text="Close",command=pop.destroy)
    close_btn.grid(row=1,column=0,padx=10,pady=10)

    pop.mainloop()


def delete_playlist():
    global current_playlist_id
    global list_of_playlists
    if current_playlist_id!=None:
        delete_playlist_from_db(list_of_playlists[current_playlist_id].id+1)
        eject_playlist()
    else:
        popup("You must load a playlist!")
        

def get_and_display_playlists():
    global list_of_playlists
    for playlist in get_all_playlists():
        list_of_playlists.append(Playlist(playlist[0]-1,playlist[1]))


    for playlist in list_of_playlists:
        for song in get_all_songs_for_playlist(playlist.name):
            playlist.list_of_songs.append(Song(song[0],song[1],song[2],song[3],song[4],song[5]))

        playlist_list.insert(END,playlist.name)

def display_songs_in_playlist(x):
    if len(playlist_list.curselection())>0:
        global list_of_playlists
        playlist=list_of_playlists[int(playlist_list.curselection()[0])]
        songs_playlist_list.delete(0,END)
        for song in playlist.list_of_songs:
            songs_playlist_list.insert(END,song.title)

def load_playlist():
    if len(playlist_list.curselection())>0:
        global current_playlist_id
        current_playlist_id=int(playlist_list.curselection()[0])
        global list_of_playlists
        global list_of_songs
        list_of_songs=list_of_playlists[current_playlist_id].list_of_songs

        song_list.delete(0,END)
        for song in list_of_songs:
            song_list.insert(END,song.title)
        songs_playlist_list.delete(0,END)
        status_bar_playlist.config(text=f'Playlist Loaded: {list_of_playlists[current_playlist_id].name} ')


def insert_playlist_in_db(name,window):
    if name!='' and name!=None:
        global list_of_songs
        global list_of_playlists

        pl=Playlist(list_of_playlists.count,name)  
        pl.list_of_songs=list_of_songs[:]
        if create_new_playlist(pl)!=None:
            list_of_playlists.append(pl)
            playlist_list.insert(END,name)
            window.destroy()
        else:
            popup("The name is already taken!")
    else:
        popup("You must enter name!")
    

def create_playlist():
    pop=Tk()
    pop.title("Enter playlist name:")
    pop.configure(background='white')
    e = ttk.Entry(pop)
    e.grid(row=0,column=0,columnspan=2,padx=10,pady=10)
     #da kazva che e v bazata veche
    save_btn=ttk.Button(pop,text="Save",command=lambda: insert_playlist_in_db(e.get(),pop))
    save_btn.grid(row=1,column=0,padx=10,pady=10)
    close_btn=ttk.Button(pop,text="Close",command=pop.destroy)
    close_btn.grid(row=1,column=1,padx=10,pady=10)

    pop.mainloop()

def edit_playlist():
    global current_playlist_id
    if current_playlist_id!=None:
        global list_of_playlists
        update_playlist_db(list_of_playlists[current_playlist_id])
        songs_playlist_list.delete(0,END)
        popup("OK")
    else:
        popup("You must load a playlist!")

def get_song(song_path):
    try:
        id=int(song_list.size())
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

#opraveno
def get_song_lyrics():
    if song_list.size():
        song_lyrics['state']=NORMAL
        genius = Genius("yKvIvpLhWT30u1NJ1zDoLd67-1MTRy-aDrE28RNo7IjPZUXvBMfoAyqr4EtY-pps")
        song_lyr = genius.search_song(list_of_songs[current_song_id].title,list_of_songs[current_song_id].artist).lyrics[:-5]
        while song_lyr[-1].isdigit():
            song_lyr=song_lyr[:-1]

        if song_lyr!=None:
            song_lyrics.delete("1.0",END)
            song_lyrics.insert("1.0",song_lyr)
        song_lyrics['state']=DISABLED

#opraveno
def add_song():
    song=filedialog.askopenfilename(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    song_name = os.path.basename(song)
    song_name=song_name.replace(".mp3"," ")
    global list_of_songs
    list_of_songs.append(get_song(os.path.abspath(song)))
    song_list.insert(END,song_name)

#opraveno
def add_songs():
    songs=filedialog.askopenfilenames(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    global list_of_songs
    for song in songs:
        list_of_songs.append(get_song(os.path.abspath(song)))
        song_name = os.path.basename(song)
        song_name.replace(".mp3"," ")
        song_list.insert(END,song_name)

#opraveno
def volume(slide_position):
    pygame.mixer.music.set_volume(volume_slider.get())

    current_volume=float(slide_position)*100
    if current_volume<1:
        volume_lbl.config(image=v0)
    elif current_volume>=1 and current_volume<20:
        volume_lbl.config(image=v1)
    elif current_volume>=20 and current_volume<40:
        volume_lbl.config(image=v2)
    elif current_volume>=40 and current_volume<60:
        volume_lbl.config(image=v3)
    elif current_volume>=60 and current_volume<80:
        volume_lbl.config(image=v4)
    else:
        volume_lbl.config(image=v5)

#opraveno
def slide(slide_position):
    global current_song_id
    global list_of_songs
    if current_song_id!=None:
        pygame.mixer.music.load(list_of_songs[current_song_id].path)
        pygame.mixer.music.play(loops=0,start=int(music_slider.get()))
    else:
        music_slider.config(value=0)  

#opraveno
def play_time():
    global current_song_id
    if current_song_id!=None:
        if list_of_songs[current_song_id].is_paused==False:
            current_time=pygame.mixer.music.get_pos()/1000

            converted_time_elapsed=time.strftime("%M:%S",time.gmtime(current_time))

            song_length=list_of_songs[current_song_id].len
            converted_time_song=time.strftime("%M:%S",time.gmtime(song_length))

            current_time+=1
            if int(music_slider.get())==int(song_length):
                next_song("next")
                return
            elif int(music_slider.get())==int(current_time):
                music_slider.config(to=int(song_length),value=int(current_time))
            else:
                music_slider.config(to=int(song_length),value=int(music_slider.get()))
                converted_time_elapsed=time.strftime("%M:%S",time.gmtime(int(music_slider.get())))
                status_bar.config(text=f'{list_of_songs[current_song_id].title} - {list_of_songs[current_song_id].artist}/Time Elapsed: {converted_time_elapsed} of {converted_time_song} ')
                next_time=int(music_slider.get())+1
                music_slider.config(value=next_time)      
            
        status_bar.after(1000,play_time)


#trqbva da maha lista
def delete_song():
    if song_list.size() and len(song_list.curselection())>0:
        global list_of_songs
        list_of_songs.pop(int(song_list.curselection()[0]))
        song_list.delete(ANCHOR)
        global current_song_id
        if current_song_id!=None:
            stop()

#opraveno
def delete_all_songs():
    if song_list.size():
        global list_of_songs
        global current_song_id
        if current_song_id!=None:
            stop()
        song_list.delete(0,END)
        list_of_songs=list()


#opravena sprqmo refaktor
def play():
    if song_list.size():
        global list_of_songs
        global current_song_id

        play_btn.configure(image=pause_btn_img)
        music_slider.config(state=NORMAL)
        
        if current_song_id!=None:
            pygame.mixer.music.unpause()
            list_of_songs[current_song_id].is_paused=False
        else:
            if len(song_list.curselection())==0:
                song_list.activate(0)
                song_list.selection_set(0,last=None)
            current_song_id=int(song_list.curselection()[0])
            pygame.mixer.music.load(list_of_songs[current_song_id].path)
            pygame.mixer.music.play(loops=0)
            list_of_songs[current_song_id].is_paused=False
            pygame.mixer.music.set_volume(volume_slider.get())
            play_time()
            get_song_lyrics()
            

#opraveno
def stop():
    if song_list.size():
        pygame.mixer.music.stop()
        song_list.select_clear(ACTIVE)
        song_list.selection_clear(0, 'end')
        global current_song_id
        global list_of_songs
        list_of_songs[current_song_id].is_paused=True
        play_btn.configure(image=play_btn_img)
        status_bar.config(text="No Song Currently Playing ")
        music_slider.config(value=0)
        current_song_id=None
        music_slider.config(state=DISABLED)

        song_lyrics.config(state=NORMAL)
        song_lyrics.delete("1.0",END)
        song_lyrics.insert("1.0","No lyrics currently found!")
        song_lyrics.config(state=DISABLED)

#opraveno
def pause():
    if song_list.size():
        global current_song_id
        global list_of_songs
        music_slider.config(state=DISABLED)
        pygame.mixer.music.pause()
        play_btn.configure(image=play_btn_img)
        list_of_songs[current_song_id].is_paused=True


def next_song(where_to_go):
    if song_list.size():
        global current_song_id
        music_slider.config(state=NORMAL)
        global list_of_songs
        play_btn.configure(image=pause_btn_img)
        
        #trqbva da se opravq
        if where_to_go=="next":
            current_song_id=0
            if len(song_list.curselection())>0 and song_list.curselection()[0]<song_list.size()-1:
                current_song_id=song_list.curselection()[0]+1
        else:
            current_song_id=song_list.size()-1
            if len(song_list.curselection())>0 and song_list.curselection()[0]>0:
                current_song_id=song_list.curselection()[0]-1
        
        list_of_songs[current_song_id].is_paused=False
        pygame.mixer.music.load(list_of_songs[current_song_id].path)
        pygame.mixer.music.play(loops=0)
        music_slider.config(value=0) 
        song_list.select_clear(0,END)
        song_list.activate(current_song_id)
        song_list.selection_set(current_song_id,last=None)

        play_time()
        get_song_lyrics()


#view
root=Tk()
root.title("Mp3 player")
root.geometry("700x750")
root. resizable(width=False, height=False)

tabsystem = ttk.Notebook(root)

style = ttk.Style()
 
style.theme_create('mainTheme', settings={
    ".": {
        "configure": {
            "background": 'white', # All except tabs
            "font": 'black'
        }
    },
    "TNotebook": {
        "configure": {
            "background":'grey', # Your margin color    
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": '#0076b3', # tab color when not selected
            "padding": [10, 2] # [space between text and horizontal tab-button border, space between text and vertical tab_button border]
        },
        "map": {
            "background": [("selected", 'white')], # Tab color when selected
            "expand": [("selected", [1, 1, 1, 0])] # text margins
        }
    }
})

style.theme_use("mainTheme")

tab1_main=ttk.Frame(tabsystem)
tab1_main.pack(fill=BOTH)

player_frame=ttk.Frame(tab1_main)
player_frame.pack(padx=10)

tab2_playlists=ttk.Frame(tabsystem)
tab2_playlists.pack(fill=BOTH)
tabsystem.add(tab1_main, text='Main')
tabsystem.add(tab2_playlists, text='Playlists')

pygame.mixer.init()

songlist_frame=Frame(player_frame, highlightbackground="#0076b3", highlightthickness=5,highlightcolor="#0076b3")
song_list=Listbox(songlist_frame,bg="#1e1e1e",fg="blue",width=60,borderwidth=1,selectbackground="white",selectforeground="black",highlightcolor="black")
song_list.pack(side=LEFT,fill = BOTH )

scrollbar_song_list = Scrollbar(songlist_frame,bg="White",activebackground="#c6c9cf",bd=1,elementborderwidth=0)
scrollbar_song_list.pack(side=RIGHT,fill=Y)

song_list.config(yscrollcommand = scrollbar_song_list.set)
scrollbar_song_list.config(command = song_list.yview)

songlist_frame.grid(row=0,column=0,pady=20)

back_btn_img=PhotoImage(file="buttons/prevb.png")
forward_btn_img=PhotoImage(file="buttons/nextb.png")
play_btn_img=PhotoImage(file="buttons/stb.png")
pause_btn_img=PhotoImage(file="buttons/pb.png")
stop_btn_img=PhotoImage(file="buttons/sb.png")

v0=PhotoImage(file="buttons/vlo/v0.png")
v1=PhotoImage(file="buttons/vlo/v1.png")
v2=PhotoImage(file="buttons/vlo/v2.png")
v3=PhotoImage(file="buttons/vlo/v3.png")
v4=PhotoImage(file="buttons/vlo/v4.png")
v5=PhotoImage(file="buttons/vlo/v5.png")

volume_lbl=ttk.Label(player_frame,image=v5)
volume_lbl.grid(row=1,column=1,pady=10)

buttons_frame=ttk.Frame(player_frame)
buttons_frame.grid(row=1,column=0,pady=10)

back_btn=Button(buttons_frame,command=lambda: next_song("prev"),image=back_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
back_btn.grid(row=0,column=0,padx=10)
forward_btn=Button(buttons_frame,command=lambda: next_song("next"), image=forward_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
forward_btn.grid(row=0,column=1,padx=10)
play_btn=Button(buttons_frame,command=lambda: play() if (current_song_id==None or list_of_songs[current_song_id].is_paused) else pause(),image=play_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
play_btn.grid(row=0,column=2,padx=10)
stop_btn=Button(buttons_frame,command=stop,image=stop_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
stop_btn.grid(row=0,column=4,padx=10)


menu_songs=Menu(root,background='grey', foreground='black', activebackground='white', activeforeground='black',borderwidth=0,relief=FLAT,activeborderwidth=0)
root.config(menu=menu_songs)
root.option_add('*tearOff',FALSE)

add_songs_menu=Menu(menu_songs,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)
delete_song_menu=Menu(menu_songs,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)
playlist_menu=Menu(menu_songs,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)

menu_songs.add_cascade(label="Add Songs",menu=add_songs_menu)
menu_songs.add_cascade(label="Remove Songs",menu=delete_song_menu)
menu_songs.add_cascade(label="Playlists",menu=playlist_menu)

add_songs_menu.add_command(label="Add One Song To The Playlist",command=add_song)
add_songs_menu.add_command(label="Add Many Songs To The Playlist",command=add_songs)

delete_song_menu.add_command(label="Remove One Song From The Playlist",command=delete_song)
delete_song_menu.add_command(label="Remove All Songs From The Playlist",command=delete_all_songs)

playlist_menu.add_command(label="Save New Playlist",command=create_playlist)
playlist_menu.add_command(label="Update Playlist",command=edit_playlist)
playlist_menu.add_command(label="Delete Playlist",command=delete_playlist)

music_slider=ttk.Scale(player_frame,from_=0,to=100,orien=HORIZONTAL,value=0,command=slide,length=500)
music_slider.grid(row=2,column=0,pady=20)

volume_frame=LabelFrame(player_frame,text="Volume",bg="White")
volume_frame.grid(row=0,column=1,padx=55)
volume_slider=ttk.Scale(volume_frame,from_=1,to=0,orien=VERTICAL,value=1,command=volume,length=150)
volume_slider.pack(pady=20,padx=10)

song_lyrics_frame=LabelFrame(tab1_main,text="Song lyrics powerd by Genius.com",background="white")
song_lyrics_frame.pack()

song_lyrics=scrolledtext.ScrolledText(song_lyrics_frame,height=10,background="white")
song_lyrics.insert("1.0","No lyrics currently found!")
song_lyrics['state']=DISABLED
song_lyrics.grid(row=0,column=0,padx=10,pady=10)


statbar_frame=ttk.Frame(root)
statbar_frame.pack(fill=X,side=BOTTOM)
status_bar=Label(statbar_frame,text="No Song Currently Playing ",borderwidth=1,bg='grey',fg='black',relief=GROOVE,anchor=E)
status_bar.pack(side=RIGHT,expand=True,fill=X)
status_bar_playlist=Label(statbar_frame,text="No Playlist currently loaded",borderwidth=1,bg='grey',fg='black',relief=GROOVE,anchor=E)
status_bar_playlist.pack(side=LEFT,expand=True,fill=X)


playlists_frame=LabelFrame(tab2_playlists,text="Playlists",background="white",bd=0)
playlists_frame.pack(side=LEFT,padx=60)

inner_frame_playlist=Frame(playlists_frame,background="white")
inner_frame_playlist.pack()

playlist_list=Listbox(inner_frame_playlist,height=20,width=25,borderwidth=1,background="white",selectbackground='#c6c9cf')
playlist_list.pack(side=LEFT,fill = BOTH)
playlist_list.bind('<Double-Button>',display_songs_in_playlist)


scrollbar_playlist_list = Scrollbar(inner_frame_playlist,bg="White",activebackground="#c6c9cf",bd=1,elementborderwidth=0)
scrollbar_playlist_list.pack(side=RIGHT,fill=Y)

playlist_list.config(yscrollcommand = scrollbar_playlist_list.set)
scrollbar_playlist_list.config(command = playlist_list.yview)

load_btn=Button(playlists_frame,text="Load Playlist",borderwidth=1,bg='white', activebackground='#c6c9cf',highlightthickness=1,command=load_playlist)
load_btn.pack(padx=10,pady=10)



songs_playlist_frame=LabelFrame(tab2_playlists,text="Songs In Playlist",background="white",bd=0)
songs_playlist_frame.pack(side=RIGHT,padx=60)

inner_frame_songs=Frame(songs_playlist_frame,background="white")
inner_frame_songs.pack()

songs_playlist_list=Listbox(inner_frame_songs,height=20,width=25,borderwidth=1,background="white", selectbackground='#c6c9cf')
songs_playlist_list.pack(side=LEFT,fill = BOTH)

scrollbar_songs_playlist_list = Scrollbar(inner_frame_songs,bg="White",activebackground="#c6c9cf",bd=1,elementborderwidth=0)
scrollbar_songs_playlist_list.pack(side=RIGHT,fill=Y)

songs_playlist_list.config(yscrollcommand = scrollbar_songs_playlist_list.set)
scrollbar_songs_playlist_list.config(command = songs_playlist_list.yview)

eject_btn=Button(songs_playlist_frame,text="Eject Playlist",borderwidth=1,bg='white', activebackground='#c6c9cf',highlightthickness=1,command=eject_playlist)
eject_btn.pack(padx=10,pady=10)

get_and_display_playlists()
tabsystem.pack(expand=1, fill=BOTH)
root.mainloop()