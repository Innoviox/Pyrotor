#Import necessary functions
from tkinter import Frame
from tkinter import Label
from tkinter import Button
from tkinter import Tk
from tkinter import Toplevel
from tkinter import StringVar
from tkinter import Entry
from tkinter import SUNKEN
from tkinter import RAISED
from tkinter import X
from tkinter import W
from tkinter import LEFT
from random import randint
from random import choice
from random import shuffle
from random import uniform
from string import ascii_uppercase
from time import sleep
from time import time
from sys import exit as end
from itertools import permutations

#import games
#Initialize the root

root = Tk() 
root.resizable(0,0)
root.title("Scrabble")
root.geometry("%dx%d%+d%+d" % (300, 300, 0, 0))
#Define useful functions: popup, destroyPopup, and generateRandomColor.
def popup(root, header, text, windowHeight, windowWidth, closable = True, closeTime = 2, winx=0, winy=0):
    """Makes a new window pop up with a text. Very helpful. Note: closable=False does not work."""
    global popupClosed, window
    popupClosed = 0
    window = Toplevel(root, height=windowHeight, width=windowWidth)
    window.wm_title(header)

    label = Label(window, text=text, relief = SUNKEN)
    #label.place(x=(windowWidth//2)-250+winx, y=(windowHeight//2)-25+winy, \
    #            height = 500, width = 500)
    label.place(x=winx, y=winy, height = 500, width = 500)
    if closable:
        button = Button(window, text="Close", command=destroyPopup)
        button.place(x=300, y=300)
    else:
        sleep(closeTime)
        destroyPopup()
        
def destroyPopup():
    """Seems obvious what this does"""
    #window.quit()
    window.destroy()
    popupClosed = 1

def generateRandomColor():
    """Generates a random color, HTML style."""
    randHex = lambda: randint(0, 255)
    return "#%02X%02X%02X" % (randHex(), randHex(), randHex())



distribution = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r", "r", "r","s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", "v", "v", "w", "w", "x", "y", "y", "z"]
