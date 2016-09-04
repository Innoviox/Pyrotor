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
from random import randint
from random import choice
from random import shuffle
from random import uniform
from string import ascii_uppercase
from time import sleep
from time import time
from sys import exit as end
from itertools import permutations

#from games import *

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

def playSavedGame(file="savedGame.txt"):
    if len(open(file).read()) > 0:
        playing = 1
        global scrabble
        scrabble = SavedGame(root)
        playing = 0
    else:
        popup(root, "No saved games", "No saved games\n\n\n", root.winfo_screenheight(), root.winfo_screenwidth())
        
def writeVars(game, file):
    file.write("New Game\n")
    
    file.write("%s %d\n" % (game.player1.name, game.player1.score))
    #file.write("%s %d\n" % (game.player2.name, game.player2.score))
    file.write("%s %d\n" % (game.player2.name, game.player2.score))
    for letter in distribution:
        file.write(letter)
        file.write(",")
    file.write("\n")
    file.write("%s %s %d\n" % (game.mode1, game.mode2, game.playerGoing))
    #print(len(distribution))
    game.player1.drawTiles()
    game.player2.drawTiles()
    #print(len(distribution))
    for letter in game.player1.rack:
        file.write(letter)
    file.write("\n")
    for letter in game.player2.rack:
        file.write(letter)
    file.write("\n")
    for row in [game.player1.board, game.player2.board][game.playerGoing-1]:
            for column in row:
                    file.write(column + "|")
            file.write("\n")
            
def setFileTextToList(newTextList, file="savedGame.txt"):
    with open(file, "w"):
        pass
    file = open(file, "w")
    for text in newTextList:
        file.write(text)
        file.write("\n")
        
def writeAllGames(games, file="savedGame.txt"):
    for game in games:
        writeGameToFile(game, gameNum = game.gameNum, gameAlreadyInFile = game.gameAlreadyInFile, file = file)
        
def writeGameToFile(game, gameNum = -1, gameAlreadyInFile = False, file="savedGame.txt"):
    if not gameAlreadyInFile:
        file = open(file, "w")
        writeVars(game, file)
    else:
        file = open(file, "r+")
        fileText = file.read().split("New Game\n")
        #print(fileText)
        text = "New Game\n"
        text += "%s %d\n%s %d\n" % (game.player1.name, game.player1.score, game.player2.name, game.player2.score)
        #print(len(distribution))
        for letter in distribution:
            text += letter
            text += ","
        #print(len(distribution))
        text += "\n"
        text += "%s %s %d\n" % (game.mode1, game.mode2, game.playerGoing)
        game.player1.drawTiles()
        game.player2.drawTiles()
        for letter in game.player1.rack:
            text += letter
        text += "\n"
        for letter in game.player2.rack:
            text += letter
        text += "\n"
        for row in [game.player1.board, game.player2.board][game.playerGoing-1]:
            for column in row:
                text += column
                text += "|"
            text += "\n"
        #print(fileText, gameNum)
        fileText[gameNum] = text
        setFileTextToList(fileText)

distribution = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r", "r", "r","s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", "v", "v", "w", "w", "x", "y", "y", "z"]
