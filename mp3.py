from tkinter import *
from tkinter import filedialog
import pygame
from tkinter import ttk
import os

#functions

global paused
paused=True

global is_song_played
is_song_played=False

def add_song():
    song=filedialog.askopenfilename(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    song_name = os.path.basename(song)
    song_list.insert(END,song_name)

def add_songs():
    songs=filedialog.askopenfilenames(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    for song in songs:
        song_name = os.path.basename(song)
        song_list.insert(END,song_name)
    

def play():
    global is_song_played
    global paused
    play_btn.configure(image=pause_btn_img)
    if is_song_played:
        pygame.mixer.music.unpause()
        paused=False
    else:
        song=song_list.get(ACTIVE)
        song=f"Songs/{song}"
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        paused=False
        is_song_played=True


def stop():
    pygame.mixer.music.stop()
    song_list.select_clear(ACTIVE)
    global is_song_played
    global paused
    paused=True
    is_song_played=False
    play_btn.configure(image=play_btn_img)

def pause(is_paused):
    global paused
    paused=is_paused
    pygame.mixer.music.pause()
    play_btn.configure(image=play_btn_img)
    paused=True


#view
root=Tk()
root.title("Mp3 player")
root.geometry("600x400")

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

back_btn=Button(buttons_frame,image=back_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
back_btn.grid(row=0,column=0,padx=10)
forward_btn=Button(buttons_frame,image=forward_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
forward_btn.grid(row=0,column=1,padx=10)
play_btn=Button(buttons_frame,command=lambda: play() if paused else pause(paused),image=play_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
play_btn.grid(row=0,column=2,padx=10)
#pause_btn=Button(buttons_frame,command=lambda: pause(paused),image=pause_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
#pause_btn.grid(row=0,column=3,padx=10)
stop_btn=Button(buttons_frame,command=stop,image=stop_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
stop_btn.grid(row=0,column=4,padx=10)




menu_songs=Menu(root,background='grey', foreground='black', activebackground='white', activeforeground='black',borderwidth=0,relief=FLAT,activeborderwidth=0)
root.config(menu=menu_songs)
root.option_add('*tearOff',FALSE)

add_songs_menu=Menu(menu_songs,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)

menu_songs.add_cascade(label="Add Songs",menu=add_songs_menu)
add_songs_menu.add_command(label="Add One Song To The Playlist",command=add_song)
add_songs_menu.add_command(label="Add Many Songs To The Playlist",command=add_songs)
tabsystem.pack(expand=1, fill=BOTH)
root.mainloop()