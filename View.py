from tkinter import *
import pygame
from tkinter import ttk
from tkinter import scrolledtext
from Models import *
from Repository import *
from Controllers import *

class PlaylistFrame(LabelFrame):
     def __init__(self, parent,button_command,btn_text,text_info):
        super().__init__(parent,text=text_info,background="white",bd=0)

        self.inner_frame=Frame(self,background="white")
        self.inner_frame.pack()

        self.list=Listbox(self.inner_frame,height=20,width=25,borderwidth=1,background="white", selectbackground='#c6c9cf')
        self.list.pack(side=LEFT,fill = BOTH)

        self.scrollbar_list = Scrollbar(self.inner_frame,bg="White",activebackground="#c6c9cf",bd=1,elementborderwidth=0)
        self.scrollbar_list.pack(side=RIGHT,fill=Y)

        self.list.config(yscrollcommand = self.scrollbar_list.set)
        self.scrollbar_list.config(command = self.list.yview)

        self.btn=Button(self,text=btn_text,borderwidth=1,bg='white', activebackground='#c6c9cf',highlightthickness=1,command=button_command)
        self.btn.pack(padx=10,pady=10)

class StatusFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.status_bar=Label(self,text="No Song Currently Playing ",borderwidth=1,bg='grey',fg='black',relief=GROOVE,anchor=E)
        self.status_bar.pack(side=RIGHT,expand=True,fill=X)

        self.status_bar_playlist=Label(self,text="No Playlist currently loaded",borderwidth=1,bg='grey',fg='black',relief=GROOVE,anchor=E)
        self.status_bar_playlist.pack(side=LEFT,expand=True,fill=X)

class MenuBar(Menu):
    def __init__(self, parent,controller):
        super().__init__(parent,background='grey', foreground='black', activebackground='white', activeforeground='black',borderwidth=0,relief=FLAT,activeborderwidth=0)
        parent.option_add('*tearOff',FALSE)
        self.controller=controller

        self.add_songs_menu=Menu(self,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)
        self.delete_song_menu=Menu(self,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)
        self.playlist_menu=Menu(self,background='grey',foreground='black', activebackground='white',activeborderwidth=0, activeforeground='black',relief=RAISED)

        self.add_cascade(label="Add Songs",menu=self.add_songs_menu)
        self.add_cascade(label="Remove Songs",menu=self.delete_song_menu)
        self.add_cascade(label="Playlists",menu=self.playlist_menu)

        #komandite trqbva da idvat ot kontrolera
        self.add_songs_menu.add_command(label="Add One Song To The Playlist",command=controller.add_song)
        self.add_songs_menu.add_command(label="Add Many Songs To The Playlist",command=controller.add_songs)

        self.delete_song_menu.add_command(label="Remove One Song From The Playlist",command=controller.delete_song)
        self.delete_song_menu.add_command(label="Remove All Songs From The Playlist",command=controller.delete_all_songs)

        self.playlist_menu.add_command(label="Save New Playlist",command=self.create_playlist)
        self.playlist_menu.add_command(label="Update Playlist",command=controller.edit_playlist)
        self.playlist_menu.add_command(label="Delete Playlist",command=controller.delete_playlist)

    
    def create_playlist(self):
        pop=Tk()
        pop.title("Enter playlist name:")
        pop.configure(background='white')
        e = ttk.Entry(pop)
        e.grid(row=0,column=0,columnspan=2,padx=10,pady=10)
        #da kazva che e v bazata veche
        save_btn=ttk.Button(pop,text="Save",command=lambda: self.controller.insert_playlist_in_db(e.get(),pop))
        save_btn.grid(row=1,column=0,padx=10,pady=10)
        close_btn=ttk.Button(pop,text="Close",command=pop.destroy)
        close_btn.grid(row=1,column=1,padx=10,pady=10)

        pop.mainloop()

class LyricsFrame(LabelFrame):
    def __init__(self, parent):
        super().__init__(parent,text="Song lyrics powerd by Genius.com",background="white")
        self.song_lyrics=scrolledtext.ScrolledText(self,height=10,background="white")
        self.song_lyrics.insert("1.0","No lyrics currently found!")
        self.song_lyrics['state']=DISABLED
        self.song_lyrics.grid(row=0,column=0,padx=10,pady=10)

class VolumeControlFrame(LabelFrame):
    def __init__(self, parent,controller,pictures):
        super().__init__(parent,text="Volume",bg="White")

        self.volume_slider=ttk.Scale(self,from_=1,to=0,orien=VERTICAL,value=1,command=controller.volume,length=150)
        self.volume_slider.pack(pady=20,padx=10)
        self.volume_lbl=ttk.Label(parent,image=pictures[5])
        self.volume_lbl.grid(row=1,column=1,pady=10)

class ButtonsFrame(ttk.Frame):
    def __init__(self, parent,controller,buttons):
        super().__init__(parent)
        
        self.back_btn=Button(self,command=lambda: controller.next_song("prev"),image=buttons[0],borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
        self.back_btn.grid(row=0,column=0,padx=10)
        self.forward_btn=Button(self,command=lambda: controller.next_song("next"), image=buttons[1],borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
        self.forward_btn.grid(row=0,column=1,padx=10)
        self.play_btn=Button(self,command=lambda: controller.play() if (controller.current_song_id==None or controller.list_of_songs[controller.current_song_id].is_paused) else controller.pause(),image=buttons[2],borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
        self.play_btn.grid(row=0,column=2,padx=10)
        self.stop_btn=Button(self,command=controller.stop,image=buttons[4],borderwidth=0,bg='white', activebackground='white',highlightthickness=0)
        self.stop_btn.grid(row=0,column=4,padx=10)

class SongListFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent,highlightbackground="#0076b3", highlightthickness=5,highlightcolor="#0076b3")

        self.song_list=Listbox(self,bg="#1e1e1e",fg="blue",width=60,borderwidth=1,selectbackground="white",selectforeground="black",highlightcolor="black")
        self.song_list.pack(side=LEFT,fill = BOTH )

        self.scrollbar_song_list = Scrollbar(self,bg="White",activebackground="#c6c9cf",bd=1,elementborderwidth=0)
        self.scrollbar_song_list.pack(side=RIGHT,fill=Y)

        self.song_list.config(yscrollcommand = self.scrollbar_song_list.set)
        self.scrollbar_song_list.config(command = self.song_list.yview)

class Tab1Frame(ttk.Frame):
    def __init__(self, parent,controller,buttons,volume):
        super().__init__(parent)
        self.player_frame=ttk.Frame(self)
        self.player_frame.pack(padx=10)

        self.songlist_frame=SongListFrame(self.player_frame)
        self.songlist_frame.grid(row=0,column=0,pady=20)

        self.buttons_frame=ButtonsFrame(self.player_frame,controller,buttons)
        self.buttons_frame.grid(row=1,column=0,pady=10)

        self.music_slider=ttk.Scale(self.player_frame,from_=0,to=100,orien=HORIZONTAL,value=0,command=controller.slide,length=500)
        self.music_slider.grid(row=2,column=0,pady=20)

        self.volume_frame=VolumeControlFrame(self.player_frame,controller,volume)
        self.volume_frame.grid(row=0,column=1,padx=55)

        self.lyrics_frame=LyricsFrame(self)
        self.lyrics_frame.pack()

class Tab2Frame(ttk.Frame):
    def __init__(self, parent,controller):
        super().__init__(parent)
        self.playlist_frame=PlaylistFrame(self,controller.load_playlist,"Load Playlist","Playlists")
        self.playlist_frame.pack(side=LEFT,padx=60)
        self.playlist_frame.list.bind('<Double-Button>',controller.display_songs_in_playlist)

        self.pl_songs_frame=PlaylistFrame(self,controller.eject_playlist,"Eject playlists","Songs In Playlist")
        self.pl_songs_frame.pack(side=RIGHT,padx=60)

class App(Tk):
    def __init__(self,):
        super().__init__()

        self.list_of_buttons=[PhotoImage(file="buttons/prevb.png"),PhotoImage(file="buttons/nextb.png"),PhotoImage(file="buttons/stb.png"),PhotoImage(file="buttons/pb.png"),PhotoImage(file="buttons/sb.png")]

        self.list_of_volume_pics=[PhotoImage(file="buttons/vlo/v0.png"),PhotoImage(file="buttons/vlo/v1.png"),PhotoImage(file="buttons/vlo/v2.png"),PhotoImage(file="buttons/vlo/v3.png"),PhotoImage(file="buttons/vlo/v4.png"),PhotoImage(file="buttons/vlo/v5.png")]

        self.controller=ControllerApp(self)
        self.title("Mp3 player")
        self.geometry("700x750")
        self.resizable(width=False, height=False)

        self.tabsystem = ttk.Notebook(self)

        self.tab1_main=Tab1Frame(self.tabsystem,self.controller,self.list_of_buttons,self.list_of_volume_pics)
        self.tab1_main.pack(fill=BOTH)

        self.tab2_playlists=Tab2Frame(self.tabsystem,self.controller)
        self.tab2_playlists.pack(fill=BOTH)

        self.tabsystem.add(self.tab1_main, text='Main')
        self.tabsystem.add(self.tab2_playlists, text='Playlists')

        menu_songs=MenuBar(self,self.controller)
        self.config(menu=menu_songs)

        self.status_frame=StatusFrame(self)
        self.status_frame.pack(fill=X,side=BOTTOM)
        self.tabsystem.pack(expand=1, fill=BOTH)

        self.style = ttk.Style()
 
        self.style.theme_create('mainTheme', settings={
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

        self.style.theme_use("mainTheme")

    def popup(self,text):
        pop=Tk()
        pop.title("Info")
        pop.configure(background='white')
        e = Label(pop,text=text,background='white')
        e.grid(row=0,column=0,padx=10,pady=10)
        close_btn=ttk.Button(pop,text="Close",command=pop.destroy)
        close_btn.grid(row=1,column=0,padx=10,pady=10)

        pop.mainloop()


pygame.mixer.init()


if __name__ == '__main__':
    app = App()
    app.controller.get_and_display_playlists()
    
    app.mainloop()  
