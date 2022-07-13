import time
from tkinter import *
from tkinter import filedialog
import pygame
from tkinter import ttk
import os
from mutagen.mp3 import MP3

#functions

global paused
paused=True

global is_song_played
is_song_played=False

def add_song():
    song=filedialog.askopenfilename(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    song_name = os.path.basename(song)
    song_list.insert(END,song_name)

def play_time():
    if is_song_played:
        current_time=pygame.mixer.music.get_pos()/1000
        converted_time_elapsed=time.strftime("%M:%S",time.gmtime(current_time))

        song=song_list.get(ACTIVE)
        song=f"Songs/{song}"

        song_length=MP3(song).info.length
        converted_time_song=time.strftime("%M:%S",time.gmtime(song_length))


        status_bar.config(text=f'Time Elapsed: {converted_time_elapsed} of {converted_time_song} ')
        status_bar.after(1000,play_time)

def add_songs():
    songs=filedialog.askopenfilenames(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    for song in songs:
        song_name = os.path.basename(song)
        song_list.insert(END,song_name)
    
def delete_song():
    if song_list.size() and len(song_list.curselection())>0:
        song_list.delete(ANCHOR)
        global is_song_played
        if is_song_played:
            stop()

def delete_all_songs():
    if song_list.size():
        global is_song_played
        if is_song_played:
            stop()
        song_list.delete(0,END)


def play():
    if song_list.size():
        global is_song_played
        global paused
        play_btn.configure(image=pause_btn_img)
        if is_song_played:
            pygame.mixer.music.unpause()
            paused=False
        else:
            if len(song_list.curselection())==0:
                song_list.activate(0)
                song_list.selection_set(0,last=None)
            song=song_list.get(ACTIVE)
            song=f"Songs/{song}"
            pygame.mixer.music.load(song)
            pygame.mixer.music.play(loops=0)
            paused=False
            is_song_played=True
            play_time()


def stop():
    if song_list.size():
        pygame.mixer.music.stop()
        song_list.select_clear(ACTIVE)
        song_list.selection_clear(0, 'end')
        global is_song_played
        global paused
        paused=True
        is_song_played=False
        play_btn.configure(image=play_btn_img)
        status_bar.config(text="No Song Currently Playing ")

def pause(is_paused):
    if song_list.size() and len(song_list.curselection())>0:
        global paused
        paused=is_paused
        pygame.mixer.music.pause()
        play_btn.configure(image=play_btn_img)
        paused=True

def next_song():
    if song_list.size():
        global is_song_played
        is_song_played=True
        global paused
        paused=False
        play_btn.configure(image=pause_btn_img)
        next=0
        if len(song_list.curselection())>0 and song_list.curselection()[0]<song_list.size()-1:
            next=song_list.curselection()
            next=next[0]+1
        song=song_list.get(next)
        song=f"Songs/{song}"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        song_list.select_clear(0,END)
        song_list.activate(next)
        song_list.selection_set(next,last=None)

        play_time()


def prev_song():
    if song_list.size():
        global is_song_played
        is_song_played=True
        global paused
        paused=False
        play_btn.configure(image=pause_btn_img)
        next=song_list.size()-1
        if len(song_list.curselection())>0 and song_list.curselection()[0]>0:
            next=song_list.curselection()
            next=next[0]-1
        song=song_list.get(next)
        song=f"Songs/{song}"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        song_list.select_clear(0,END)
        song_list.activate(next)
        song_list.selection_set(next,last=None)

        play_time()

#view
root=Tk()
root.title("Mp3 player")
root.geometry("700x400")

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
tab1_main.pack()

tab2_playlists=ttk.Frame(tabsystem)
tab2_playlists.place(width=600, height=400)
tabsystem.add(tab1_main, text='Main')
tabsystem.add(tab2_playlists, text='Playlists')

pygame.mixer.init()

songlist_frame=Frame(tab1_main, highlightbackground="#0076b3", highlightthickness=5,highlightcolor="#0076b3")
song_list=Listbox(songlist_frame,bg="#1e1e1e",fg="blue",width=60,borderwidth=1,selectbackground="white",selectforeground="black",highlightcolor="black")
song_list.pack(side=LEFT,fill = BOTH )

scrollbar_song_list = Scrollbar(songlist_frame,bg="White",activebackground="#c6c9cf",bd=1,elementborderwidth=0)
scrollbar_song_list.pack(side=RIGHT,fill=Y)

song_list.config(yscrollcommand = scrollbar_song_list.set)
scrollbar_song_list.config(command = song_list.yview)

songlist_frame.pack(pady=20)

back_btn_img=PhotoImage(file="buttons/prevb.png")
forward_btn_img=PhotoImage(file="buttons/nextb.png")
play_btn_img=PhotoImage(file="buttons/stb.png")
pause_btn_img=PhotoImage(file="buttons/pb.png")
stop_btn_img=PhotoImage(file="buttons/sb.png")

buttons_frame=ttk.Frame(tab1_main,)
buttons_frame.pack()

back_btn=Button(buttons_frame,command=prev_song,image=back_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
back_btn.grid(row=0,column=0,padx=10)
forward_btn=Button(buttons_frame,command=next_song, image=forward_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
forward_btn.grid(row=0,column=1,padx=10)
play_btn=Button(buttons_frame,command=lambda: play() if paused else pause(paused),image=play_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
play_btn.grid(row=0,column=2,padx=10)
stop_btn=Button(buttons_frame,command=stop,image=stop_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
stop_btn.grid(row=0,column=4,padx=10)




menu_songs=Menu(root,background='grey', foreground='black', activebackground='white', activeforeground='black',borderwidth=0,relief=FLAT,activeborderwidth=0)
root.config(menu=menu_songs)
root.option_add('*tearOff',FALSE)

add_songs_menu=Menu(menu_songs,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)
delete_song_menu=Menu(menu_songs,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)

menu_songs.add_cascade(label="Add Songs",menu=add_songs_menu)
menu_songs.add_cascade(label="Remove Songs",menu=delete_song_menu)

add_songs_menu.add_command(label="Add One Song To The Playlist",command=add_song)
add_songs_menu.add_command(label="Add Many Songs To The Playlist",command=add_songs)

delete_song_menu.add_command(label="Remove One Song From The Playlist",command=delete_song)
delete_song_menu.add_command(label="Remove All Songs From The Playlist",command=delete_all_songs)

status_bar=Label(tab1_main,text="No Song Currently Playing ",borderwidth=1,bg='grey',fg='black',relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

tabsystem.pack(expand=1, fill=BOTH)
root.mainloop()