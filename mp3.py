from glob import glob
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

global song_length
song_length=0

global current_song
current_song=None

def add_song():
    song=filedialog.askopenfilename(initialdir='Songs/',title="Choose A Song",filetypes=(("mp3 Files","*.mp3"),))
    song_name = os.path.basename(song)
    song_list.insert(END,song_name)


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
                stop()
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
            play_time()
            


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

def pause():
    if song_list.size() and len(song_list.curselection())>0:
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

#view
root=Tk()
root.title("Mp3 player")
root.geometry("700x500")

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

tab2_playlists=ttk.Frame(tabsystem)
tab2_playlists.pack(fill=BOTH)
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
play_btn=Button(buttons_frame,command=lambda: play() if paused else pause(),image=play_btn_img,borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
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

music_slider=ttk.Scale(tab1_main,from_=0,to=100,orien=HORIZONTAL,value=0,command=slide,length=500)
music_slider.pack(pady=40)

tabsystem.pack(expand=1, fill=BOTH)
root.mainloop()