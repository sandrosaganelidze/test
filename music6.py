import os
import pygame
from tkinter import *
from tkinter.filedialog import askdirectory
from mutagen.id3 import ID3
import random

root = Tk()
root.minsize(300, 300)

root.configure(bg='#3f403f')

listofsongs = []
realnames = []

v = StringVar()
songlabel = Label(root, textvariable=v, width=35)

index = 0


listbox_songs = Listbox(root)
listbox_songs.pack(pady=4)

def directorychooser():
    global listofsongs, realnames

    listofsongs = []
    realnames = []

    directory = askdirectory()

    if not directory:
        return

    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)

            if 'TIT2' in audio:
                realnames.append(audio['TIT2'].text[0])
            else:
                realnames.append(files)

            listofsongs.append(files)

    if listofsongs:
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(directory, listofsongs[0]))
        pygame.mixer.music.play()

        listbox_songs.delete(0, 'end')
        for song in realnames:
            listbox_songs.insert('end', song)
    else:
        print("No MP3 files found in the selected folder.")

def updatelabel():
    global index
    global songname
    v.set(realnames[index])


def nextsong(event):
    global index
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


def prevsong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


def unpausesong(event):
    pygame.mixer.music.unpause()
    v.set("Song unpasued")


def pausesong(event):
    pygame.mixer.music.pause()
    v.set("Song Paused")

def shuffle(event):
    global index
    if pygame.mixer.music.get_busy():
        index = random.randint(0, len(listofsongs) - 1)
        pygame.mixer.music.queue(listofsongs[index])
    else:
        index = random.randint(0, len(listofsongs) - 1)
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
    updatelabel()

def repeat(event):
    global index
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.queue(listofsongs[index])
    else:
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
    updatelabel()

button_frame = Frame(root, bg='#3f403f')
button_frame.pack(side='top', padx=10, pady=10)

previous_icon = PhotoImage(file="C:/Users/x/Desktop/previous.png")
previousbutton = Button(button_frame, image=previous_icon, bg="white")
previousbutton.pack(side='left', padx=2)

pause_icon = PhotoImage(file="C:/Users/x/Desktop/pause.png")
pausebutton = Button(button_frame, image=pause_icon, bg="white")
pausebutton.pack(side='left', padx=2)

unpause_icon = PhotoImage(file="C:/Users/x/Desktop/play-button-arrowhead.png")
unpausebutton = Button(button_frame, image=unpause_icon, bg="white")
unpausebutton.pack(side='left', padx=2)

next_icon = PhotoImage(file="C:/Users/x/Desktop/next.png")
nextbutton = Button(button_frame, image=next_icon, bg="white")
nextbutton.pack(side='left', padx=2)

button_frame_2 = Frame(root, bg='#3f403f')
button_frame_2.pack(side="top", padx=10, pady=10)

shuffle_icon = PhotoImage(file="C:/Users/x/Desktop/shuffle.png")
shufflebutton = Button(button_frame_2, image=shuffle_icon, bg="white")
shufflebutton.pack(side='left', padx=2)

repeat_icon = PhotoImage(file="C:/Users/x/Desktop/repeat.png")
repeatbutton = Button(button_frame_2, image=repeat_icon, bg="white")
repeatbutton.pack(side='left', padx=2)

change_file_button = Button(root, text='Choose Folder', command=directorychooser, bg="white", fg="black", width=15)
change_file_button.pack()

songlabel.configure(bg="#3f403f", fg="white")

nextbutton.bind("<Button-1>", nextsong)
previousbutton.bind("<Button-1>", prevsong)
pausebutton.bind("<Button-1>", pausesong)
unpausebutton.bind("<Button-1>", unpausesong)
shufflebutton.bind("<Button-1>", shuffle)
repeatbutton.bind("<Button-1>", repeat)
songlabel.pack()
root.mainloop()
