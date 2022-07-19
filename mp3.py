import time
from tkinter import *
from tkinter import filedialog
import pygame
from tkinter import ttk
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from tkinter import scrolledtext
from lyricsgenius import Genius

#functions

global paused
paused=True

global song_length
song_length=0

global current_song
current_song=None

def get_song_lyrics():
    if song_list.size():
        song_lyrics['state']=NORMAL
        genius = Genius("yKvIvpLhWT30u1NJ1zDoLd67-1MTRy-aDrE28RNo7IjPZUXvBMfoAyqr4EtY-pps")
        song_lyr = genius.search_song(ID3(current_song)["TIT2"].text[0],ID3(current_song)["TPE1"].text[0]).lyrics[:-5]
        while song_lyr[-1].isdigit():
            song_lyr=song_lyr[:-1]

        if song_lyr!=None:
            song_lyrics.delete("1.0",END)
            song_lyrics.insert("1.0",song_lyr)
        song_lyrics['state']=DISABLED

def add_song():
    song=filedialog.askopenfilename(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    song_name = os.path.basename(song)
    song_list.insert(END,song_name)

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

def slide(slide_position):
    global current_song
    global paused
    if current_song!=None:
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play(loops=0,start=int(music_slider.get()))
    else:
        music_slider.config(value=0)  


def play_time():
    global current_song
    if current_song!=None:
        if paused==False:
            current_time=pygame.mixer.music.get_pos()/1000

            converted_time_elapsed=time.strftime("%M:%S",time.gmtime(current_time))

            global song_length
            song_length=MP3(current_song).info.length
            converted_time_song=time.strftime("%M:%S",time.gmtime(song_length))

            current_time+=1
            if int(music_slider.get())==int(song_length):
                next_song()
                return
            elif int(music_slider.get())==int(current_time):
                music_slider.config(to=int(song_length),value=int(current_time))
            else:
                music_slider.config(to=int(song_length),value=int(music_slider.get()))
                converted_time_elapsed=time.strftime("%M:%S",time.gmtime(int(music_slider.get())))
                status_bar.config(text=f'Time Elapsed: {converted_time_elapsed} of {converted_time_song} ')
                next_time=int(music_slider.get())+1
                music_slider.config(value=next_time)      
            
        status_bar.after(1000,play_time)

def add_songs():
    songs=filedialog.askopenfilenames(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    for song in songs:
        song_name = os.path.basename(song)
        song_list.insert(END,song_name)
    
def delete_song():
    if song_list.size() and len(song_list.curselection())>0:
        song_list.delete(ANCHOR)
        global current_song
        if current_song!=None:
            stop()

def delete_all_songs():
    if song_list.size():
        global current_song
        if current_song!=None:
            stop()
        song_list.delete(0,END)


def play():
    if song_list.size():
        global current_song
        global paused
        play_btn.configure(image=pause_btn_img)
        music_slider.config(state=NORMAL)
        if current_song!=None:
            pygame.mixer.music.unpause()
            paused=False
        else:
            if len(song_list.curselection())==0:
                song_list.activate(0)
                song_list.selection_set(0,last=None)
            current_song=f"Songs/{song_list.get(ACTIVE)}"
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play(loops=0)
            paused=False
            pygame.mixer.music.set_volume(volume_slider.get())
            play_time()
            get_song_lyrics()
            


def stop():
    if song_list.size():
        pygame.mixer.music.stop()
        song_list.select_clear(ACTIVE)
        song_list.selection_clear(0, 'end')
        global paused
        global current_song
        paused=True
        play_btn.configure(image=play_btn_img)
        status_bar.config(text="No Song Currently Playing ")
        music_slider.config(value=0)
        current_song=None
        music_slider.config(state=DISABLED)
        song_lyrics.delete("1.0",END)
        song_lyrics.insert("1.0","No lyrics currently found!")

def pause():
    if song_list.size():
        global paused
        music_slider.config(state=DISABLED)
        pygame.mixer.music.pause()
        play_btn.configure(image=play_btn_img)
        paused=True

def next_song():
    if song_list.size():
        global current_song
        music_slider.config(state=NORMAL)
        global paused
        paused=False
        play_btn.configure(image=pause_btn_img)
        next=0
        if len(song_list.curselection())>0 and song_list.curselection()[0]<song_list.size()-1:
            next=song_list.curselection()
            next=next[0]+1
        current_song=f"Songs/{song_list.get(next)}"
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play(loops=0)
        music_slider.config(value=0) 
        song_list.select_clear(0,END)
        song_list.activate(next)
        song_list.selection_set(next,last=None)

        play_time()
        get_song_lyrics()


def prev_song():
    if song_list.size():
        global current_song
        music_slider.config(state=NORMAL)
        global paused
        paused=False
        play_btn.configure(image=pause_btn_img)
        next=song_list.size()-1
        if len(song_list.curselection())>0 and song_list.curselection()[0]>0:
            next=song_list.curselection()
            next=next[0]-1
        current_song=f"Songs/{song_list.get(next)}"
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play(loops=0)
        music_slider.config(value=0) 
        song_list.select_clear(0,END)
        song_list.activate(next)
        song_list.selection_set(next,last=None)

        play_time()
        get_song_lyrics()

#view
root=Tk()
root.title("Mp3 player")
root.geometry("700x750")

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

back_btn=Button(buttons_frame,command=prev_song,image=back_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
back_btn.grid(row=0,column=0,padx=10)
forward_btn=Button(buttons_frame,command=next_song, image=forward_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
forward_btn.grid(row=0,column=1,padx=10)
play_btn=Button(buttons_frame,command=lambda: play() if paused else pause(),image=play_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
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

playlist_menu.add_command(label="Save playlist",command=delete_song)

music_slider=ttk.Scale(player_frame,from_=0,to=100,orien=HORIZONTAL,value=0,command=slide,length=500)
music_slider.grid(row=2,column=0,pady=20)

volume_frame=LabelFrame(player_frame,text="Volume",bg="White")
volume_frame.grid(row=0,column=1,padx=55)
volume_slider=ttk.Scale(volume_frame,from_=0,to=1,orien=VERTICAL,value=1,command=volume,length=150)
volume_slider.pack(pady=20,padx=10)

song_lyrics_frame=LabelFrame(tab1_main,text="Song lyrics powerd by Genius.com",background="white")
song_lyrics_frame.pack()

song_lyrics=scrolledtext.ScrolledText(song_lyrics_frame,height=10,background="white")
song_lyrics.insert("1.0","No lyrics currently found!")
song_lyrics['state']=DISABLED
song_lyrics.grid(row=0,column=0,padx=10,pady=10)

status_bar=Label(root,text="No Song Currently Playing ",borderwidth=1,bg='grey',fg='black',relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)






playlists_frame=LabelFrame(tab2_playlists,text="Playlists",background="white",bd=0)
playlists_frame.pack(side=LEFT,padx=60)

inner_frame_playlist=Frame(playlists_frame,background="white")
inner_frame_playlist.pack()

playlist_list=Listbox(inner_frame_playlist,height=20,width=25,borderwidth=1,background="white")
playlist_list.pack(side=LEFT,fill = BOTH)

scrollbar_playlist_list = Scrollbar(inner_frame_playlist,bg="White",activebackground="#c6c9cf",bd=1,elementborderwidth=0)
scrollbar_playlist_list.pack(side=RIGHT,fill=Y)

playlist_list.config(yscrollcommand = scrollbar_playlist_list.set)
scrollbar_playlist_list.config(command = playlist_list.yview)

back_btn=Button(playlists_frame,text="Load Playlist",borderwidth=1,bg='white', activebackground='#c6c9cf',highlightthickness=1)
back_btn.pack(padx=10,pady=10)



songs_playlist_frame=LabelFrame(tab2_playlists,text="Songs In Playlist",background="white",bd=0)
songs_playlist_frame.pack(side=RIGHT,padx=60)

songs_playlist_list=Listbox(songs_playlist_frame,height=20,width=25,borderwidth=1,background="white")
songs_playlist_list.pack(side=LEFT,fill = BOTH)

scrollbar_songs_playlist_list = Scrollbar(songs_playlist_frame,bg="White",activebackground="#c6c9cf",bd=1,elementborderwidth=0)
scrollbar_songs_playlist_list.pack(side=RIGHT,fill=Y)

songs_playlist_list.config(yscrollcommand = scrollbar_songs_playlist_list.set)
scrollbar_songs_playlist_list.config(command = songs_playlist_list.yview)



tabsystem.pack(expand=1, fill=BOTH)
root.mainloop()