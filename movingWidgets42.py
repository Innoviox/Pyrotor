from tkinter import *
root = Tk()
root.resizable(0,0)
root.title("Scrabble")
root.geometry("%dx%d%+d%+d" % (300, 300, 0, 0))

global played
played = 0

import random #Choosing racks
import string #Checking if touching a letter
import time   #Score animation
import os     #File manipulation (unneccesary?)
import itertools #For the AI

def popup(root, header, text, windowHeight, windowWidth, closable = True):
    """Makes a new window pop up with a text. Very helpful."""
    global popupClosed, window
    popupClosed = 0
    window = Toplevel(root, height=windowHeight, width=windowWidth)
    window.wm_title(header)

    label = Label(window, text=text, relief = SUNKEN)
    label.place(x=(windowWidth//2)-250, y=(windowHeight//2)-250, \
                height = 500, width = 500)

    if closable:
        button = Button(window, text="Close", command=destroyPopup)
        button.place(x=0, y=0)
    else:
        time.sleep(2)
        destroyPopup()        
def destroyPopup():
    #window.quit()
    window.destroy()
    popupClosed = 1

class MovingLetter():
    def __init__(self, root, text, x, y, frame):
        self.board = [[" ", "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O "],
    ['01', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'TWS', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS'],
    ['02', ' ', 'DWS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'DWS', ' '],
    ['03', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' '],
    ['04', 'DLS', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' ', 'DLS'],
    ['05', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' '],
    ['06', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' '],
    ['07', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', ' '],
    ['08', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', '*', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS'],
    ['09', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', ' '],
    ['10', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' '],
    ['11', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' '],
    ['12', 'DLS', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' ', 'DLS'],
    ['13', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' '],
    ['14', ' ', 'DWS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'DWS', ' '],
    ['15', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'TWS', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS']]
        self.scoreList = ['TWS', 'DWS', 'TLS', 'DLS']
        self.root = root
        self.rackFrame = frame
        self.x = x
        self.y = y

        self.origX = x
        self.origY = y

        self.text = text
        self.origText = text
        if text == "?":
            self.blankChosen = 0
            self.blankWindow = Toplevel(self.root)
            self.blankWindow.geometry("%dx%d%+d%+d" % (self.root.winfo_screenwidth(), self.root.winfo_screenheight(), 0, 0))
            self.blankWindow.resizable(0, 0)
            self.blankWindow.withdraw()
            self.blankWindow.title("Choose Blank")
                      
        self.frame = Frame(self.rackFrame, bd=1, relief=SUNKEN)
        self.frame.place(x=self.x, y=self.y, width=25, height=25)

        self.label = Label(self.frame, bd=1, relief=RAISED, text=text, width=25, bg="yellow")
        self.label.pack(fill=X, padx=1, pady=1)

        self.label.bind('<ButtonPress-1>', self.startMoveWindow)
        self.label.bind('<B1-Motion>', self.MoveWindow)
        self.label.bind('<ButtonRelease-1>', self.checkForReturn)
        
        self.frame.bind('<ButtonPress-1>', self.startMoveWindow)
        self.frame.bind('<B1-Motion>', self.MoveWindow)
        self.label.bind('ButtonRelease-1>', self.checkForReturn)
        
        self.frame.lift()

        self.hoveringOver = "%s,%s" % ("NA", "NA")
        self.getPositions()
    def startMoveWindow(self, event):
        self.lastX = event.x_root
        self.lastY = event.y_root
    def MoveWindow(self, event):
        self.root.update_idletasks()
        self.x += event.x_root - self.lastX
        self.y += event.y_root - self.lastY
        if self.x > 650: self.x = 650
        if self.y > 675: self.y = 675
        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        
        self.lastX, self.lastY = event.x_root, event.y_root
        self.frame.place_configure(x=self.x, y=self.y)

        f1Position = (self.x, self.y)
        for labelPosition in self.labels_positionList.keys():
            if self.isTouching(f1Position, labelPosition,
                               self.frame.winfo_width(), self.frame.winfo_height(),
                               26, 26):
                self.frame.place_configure(x=labelPosition[0], y=labelPosition[1])
                self.hoveringOver = "%d,%d" % (self.labels_positionList[(labelPosition[0], labelPosition[1])][0],
                                               self.labels_positionList[(labelPosition[0], labelPosition[1])][1])
                if self.text == "?" and self.blankChosen != 1:
                    self.chooseBlank()

        if self.isTouching(f1Position, (100, 550),
                           self.frame.winfo_width(), self.frame.winfo_height(),
                           300, 50):
            self.senseMovables()
            
        self.frame.lift()       
    def isTouching(self, position1, position2, width1, height1, width2, height2):
        #((x1>x2)) or (x1>(x2+w1))) and ((y1>y2) or (y1>(y2+h1))) and ((x1<(x2+w2)) and (y1<(y2+h2)))
        if ((position1[0] > position2[0]) or (position1[0] > (position2[0] + width1))) and \
           ((position1[1] > position2[1]) or (position1[1] > (position2[1] + height1))) and \
           ((position1[0] < (position2[0] + width2)) and (position1[1] < (position2[1] + height2))):
            return True
        
        elif ((position2[0] > position1[0]) or (position2[0] > (position1[0] + width2))) and \
             ((position2[1] > position1[1]) or (position2[1] > (position1[1] + height2))) and \
             ((position2[0] < (position1[0] + width1)) and (position2[1] < (position1[1] + height1))):
            return True
        
        else:
            return False
    def checkForReturn(self, *event):
        f1Position = (self.x, self.y)
        #If not touching board: go back
        if not(self.isTouching(f1Position, (self.boardX, self.boardY),
                          self.frame.winfo_width(), self.frame.winfo_height(),
                          self.boardWidth, self.boardHeight)):
            self.returnToOrig()
    def getPositions(self):
        self.labels_positionList = {}
        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                if not(label[0] == "0" or label[0] == "1" or label[0].isalpha()):
                    self.labels_positionList[((i*31)+3, (j*31)+3)] = (j, i)
                elif label in self.scoreList:
                    self.labels_positionList[((i*31)+3, (j*31)+3)] = (j, i)
        self.boardWidth, self.boardHeight = 497, 497
        self.boardX, self.boardY = 0, 0
    def getBoard(self):
        self.extraList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
                     "TWS", "DWS", "TLS", "DLS", \
                     "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ", \
                     "*", " "]
        colors = {"TWS":"red", "DWS":"pink", "TLS":"green", "DLS":"blue", "*":"pink"}
        self.boardFrame = Frame(self.root, bd=1, relief=SUNKEN)
        self.boardFrame.place(x=0, y=0, width=497, height = 497)
        labels = list()
        squares = list()

        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                if label in self.extraList:
                    entry = Frame(self.boardFrame, bd=1, relief=RAISED)
                    entry.place(x=(i*31), y=(j*31), width=31, height=31)
                    labels.append(Label(entry, text = label,
                                        height = 31, width = 31))
                    if label in colors.keys():
                        labels[-1].config(bg=colors[label])
                        
                    labels[-1].pack()
                else:
                    frame = Frame(self.boardFrame, bd=1, relief=RAISED)
                    frame.place(x=(i*31), y=(j*31), width=31, height=31)
                    entry = Frame(self.boardFrame, bd=1, relief=SUNKEN)
                    entry.place(x=(i*31) + 3, y=(j*31) + 3, width=25, height=25)
                    squares.append(Label(entry, bd = 1, text=label,
                                         height=25, width=25, relief=RAISED))
                    squares[-1].pack(fill=X, padx=1, pady=1)
                    entry.lift()                                               
    def returnToOrig(self):
        self.x = self.origX
        self.y = self.origY
        self.frame.place_configure(x=self.x, y=self.y)
        self.hoveringOver = "NA,NA"
        if self.origText == "?":
            self.blankChosen = 0
            self.setBlank("?")           
    def chooseBlank(self):
        self.blankWindow.deiconify()
        chooseLabel = Label(self.blankWindow, text = "Choose the tile you want your blank to be.")
        chooseLabel.place(x = 400, y = 200, width = 300, height = 100)
        self.choiceWindow = Frame(self.blankWindow)
        self.choiceWindow.place(x=400, y=400, width=500, height = 500)
        buttons = []
        row = 1
        column = 1
        for letter in string.ascii_uppercase:
            button = Button(self.choiceWindow, text = letter,
                            command = lambda letter=letter: self.setBlank(letter), \
                            height = 1, width = 1)
            buttons.append(button)
            buttons[-1].place(x = row * 30, y = column * 30)
            column += 1
            if column % 6 == 0:
                column = 1
                row += 1                
    def setBlank(self, letter):
        if letter != "?":
            self.blankChosen = 1
            self.blankWindow.withdraw()
            
        self.text = letter
        self.label.destroy()
        self.label = Label(self.frame, bd=1, relief=RAISED, text=self.text, width=25)
        self.label.pack(fill=X, padx=1, pady=1)

        self.label.bind('<ButtonPress-1>', self.startMoveWindow)
        self.label.bind('<B1-Motion>', self.MoveWindow)
    def senseMovables(self, *event):
        for movable in self.movables:
            if self.isTouching((self.x, self.y), (movable.x, movable.y), 
                               25, 25, 30, 30):
                self.switchOnRack(self, movable)
    def setPlace(self, x, y):
            self.frame.place_configure(x=x, y=y)
            self.x = x
            self.y = y

            self.frame.update()
            self.frame.lift()            
    def weedMovables(self):
        for movable in self.movables:
            if movable is self:
                self.movables.remove(movable)           
    def getRackPosition(self):
        for position in self.rackPositions:
            if self.isIn(self.x, self.y, position[0], position[1], 30, 30):
                self.rackPosition = self.rackPositions.index(position)
                self.origRackX, self.origRackY = position[0], position[1]                
    def isIn(self, x1, y1, x2, y2, height2, width2):
        if x1 >= x2 and x1 <= x2+width2 and y1 >= y2 and y1 <= y2+height2:
            return True
        return False        
    def switchOnRack(self, m1, m2):
        x1, y1 = m1.origRackX, m1.origRackY
        x2, y2 = m2.origRackX, m2.origRackY
        
        m1.origX, m1.origY = x2, y2
        m2.origX, m2.origY = x1, y1

        m1.origRackX, m1.origRackY = x2, y2
        m2.origRackX, m2.origRackY = x1, y1
        
        m2.setPlace(x1, y1)
        
        rackPos1, rackPos2 = m1.rackPosition, m2.rackPosition
        m1.rackPosition = rackPos2
        m2.rackPosition = rackPos1


class MovingExchangeLetter(MovingLetter):
    def __init__(self, root, text, x, y, frame):
        super(MovingExchangeLetter, self).__init__(root, text, x, y, frame)
        self.boundaryX, self.boundaryY = 550, 450
        self.onExchangeRack = False        
    def startMoveWindow(self, event):
        super(MovingExchangeLetter, self).startMoveWindow(event)
    def MoveWindow(self, event):
        self.root.update_idletasks()
        self.x += event.x_root - self.lastX
        self.y += event.y_root - self.lastY
        self.lastX, self.lastY = event.x_root, event.y_root
        self.frame.place_configure(x=self.x, y=self.y)

        f1Position = (self.x, self.y)
        for labelPosition in self.labels_positionList.values():
            if self.isTouching(f1Position, labelPosition,
                               self.frame.winfo_width(), self.frame.winfo_height(),
                               30, 30):
                self.frame.place_configure(x=labelPosition[0], y=labelPosition[1])
                self.onExchangeRack = True

        self.checkForReturn()
        self.frame.lift()
    def getPositions(self):
        self.exchangeRackWidth, self.exchangeRackHeight = 210, 40
        self.exchangeRackX, self.exchangeRackY = 300, 200
        self.labels_positionList = {}
        for column in range(7):
            self.labels_positionList[(self.exchangeRackX, column)] = ((column*30)+self.exchangeRackX, self.exchangeRackY+5)
    def getExchangeRack(self):
        self.exchangeRack = Frame(self.root, bd=1, relief=RAISED)
        self.exchangeRack.place(x=self.exchangeRackX, y=self.exchangeRackY, width=self.exchangeRackWidth, height = self.exchangeRackHeight)
        labels = []
        for i in range(7):
            labels.append(Label(self.exchangeRack, relief=SUNKEN))
            labels[-1].place(x=i*30+self.exchangeRackX, y=self.exchangeRackY, height=30, width=30)            
    def isTouching(self, position1, position2, width1, height1, width2, height2):
        #super(MovingExchangeLetter, self).isTouching(position1, position2, width1, height1, width2, height2)
        if ((position1[0] > position2[0]) or (position1[0] > (position2[0] + width1)))and \
           ((position1[1] > position2[1]) or (position1[1] > (position2[1] + height1))) and \
           ((position1[0] < (position2[0] + width2)) and (position1[1] < (position2[1] + height2))):
            return True
        
        elif ((position2[0] > position1[0]) or (position2[0] > (position1[0] + width2))) and \
             ((position2[1] > position1[1]) or (position2[1] > (position1[1] + height2))) and \
             ((position2[0] < (position1[0] + width1)) and (position2[1] < (position1[1] + height1))):
            return True
        
        else:
            return False
    def checkForReturn(self, *event):
        f1Position = (self.x, self.y)
        if not(self.isTouching(f1Position, (200,130),
                          self.frame.winfo_width(), self.frame.winfo_height(),
                          300, 275)):
            self.frame.place_configure(x=self.origX, y=self.origY)
            #self.x = self.origX
            #self.y = self.origY
            self.onExchangeRack = False

        
class Player():
    def __init__(self, root, playerNum, name, x, y, mode1, mode2):
        self.board = [[" ", "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O "],
            ['01', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'TWS', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS'],
            ['02', ' ', 'DWS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'DWS', ' '],
            ['03', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' '],
            ['04', 'DLS', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' ', 'DLS'],
            ['05', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' '],
            ['06', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' '],
            ['07', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', ' '],
            ['08', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', '*', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS'],
            ['09', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DLS', ' ', ' '],
            ['10', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' '],
            ['11', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' ', ' ', 'DWS', ' ', ' ', ' ', ' '],
            ['12', 'DLS', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' ', 'DLS'],
            ['13', ' ', ' ', 'DWS', ' ', ' ', ' ', 'DLS', ' ', 'DLS', ' ', ' ', ' ', 'DWS', ' ', ' '],
            ['14', ' ', 'DWS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'TLS', ' ', ' ', ' ', 'DWS', ' '],
            ['15', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'TWS', ' ', ' ', ' ', 'DLS', ' ', ' ', 'TWS']]

        
        self.ospd = open("dict.txt").read().split() #taken from http://www.puzzlers.org/pub/wordlists/ospd.txt #/Volumes/PYTHONDISK/
        #self.ospd = open("newDict.txt").read().split("\n") #taken from https://raw.githubusercontent.com/xjtian/PyScrabble/master/wordlists/OSPD4_stripped.txt

        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10, "?" : 0}
        
        self.scoreList = ['TWS', 'DWS', 'TLS', 'DLS']
        self.score = 0
        self.playerNum = playerNum
        self.name = name
        
        self.rack = []
        self.drawTiles()
        
        self.x = x
        self.y = y

        self.mode1 = mode1
        self.mode2 = mode2
        
        self.overRoot = root
        
        self.root = root        
    def reRoot(self, root):
        self.root.deiconify()
        self.overRoot.deiconify()
    def startTurn(self, otherName, otherScore):
        self.switchTurn = 0
        
        self.root.title("%s's Turn" % self.name)
        self.root.resizable(0,0)
        self.root.geometry("%dx%d%+d%+d"%(675, 700, 0, 0))


        self.rackFrame = Frame(self.root, bd=1, relief=RAISED)
        self.rackFrame.place(x=self.x-50, y=self.y, width=300, height=50)

        self.getMovables(self.x, self.y)
        for movable in self.movables:
            movable.board = self.board
            
        self.rackFrame.lower()
        self.movables[-1].getBoard()

        self.shuffleButton = Button(self.root, text = "Shuffle", command = self.shuffleRack)
        self.shuffleButton.place(x=self.x-150, y=self.y+100)
        
        self.enterButton = Button(self.root, text = "Enter Word", command = self.getNewWord)
        self.enterButton.place(x=self.x+50, y=self.y+100)
        
        self.returnButton = Button(self.root, text = "Return", command = self.returnMovables)
        self.returnButton.place(x=self.x+150, y=self.y+100)

        self.exchangeButton = Button(self.root, text = "Exchange", command= self.exchange)
        self.exchangeButton.place(x = self.x-50, y=self.y+100)

        self.screenHeight = self.root.winfo_screenheight()
        self.screenWidth = self.root.winfo_screenwidth()

        self.getScoreBoard(otherName, otherScore)


        
        self.root.mainloop()
    def getScoreBoard(self, otherName, otherScore):
        self.player1ScoreLabel = Label(self.root, text="%s's Score: %d" % (self.name, self.score), height=1, width=20, relief=SUNKEN)
        self.player2ScoreLabel = Label(self.root, text="%s's Score: %d" % (otherName, otherScore), height=1, width=20, relief=SUNKEN)
        self.tilesLabel = Label(self.root, text = "%d tiles left" % len(distribution), height = 1, width = 20)
        if self.playerNum == 1:
            self.player1ScoreLabel.place(x=500, y=0)
            self.player2ScoreLabel.place(x=500, y=20)
            self.scoreX, self.scoreY = 500, 0
        else:
            self.player1ScoreLabel.place(x=500, y=20)
            self.player2ScoreLabel.place(x=500, y=0)
            self.scoreX, self.scoreY = 500, 20
        self.tilesLabel.place(x=500, y=40)      
    def updateSelfScore(self):
        self.player1ScoreLabel.config(text = "%s's Score: %d" % (self.name, self.score))        
    def scoreAnimation(self, scoreLabel, startX, startY, endX, endY, endWidth, endHeight, travelTime = .1, changesPerSecond = 2500, schoolComputerChangesPerSecond = 2500):
        frame = Frame(self.root, relief=RAISED)
        frame.place(x=startX, y=startY, height = 25, width = 25)
        label = Label(frame, text = "+" + str(scoreLabel), bd=1, relief=RAISED, height = 25, width = 25)
        label.pack()

        frame.lift()

        newX = startX
        newY = startY

        changeNum = travelTime * changesPerSecond
        changeSpeed = travelTime / changesPerSecond
        if startX > endX:
            xChange = round((startX - endX) / changeNum)
        else:
            xChange = round((endX - startX) / changeNum)

        if startY > endY:
            yChange = round((startY - endY) / changeNum)
        else:
            yChange = round((endY - startY) / changeNum)
            
        while not self.isTouchingScoreboard(newX, newY):
            if newX < endX:
                newX += xChange
            if newY < endY:
                newY += yChange
            if newX > endX:
                newX -= xChange
            if newY > endY:
                newY -= yChange
            frame.place_configure(x=newX, y=newY)
  
            frame.lift()
            frame.update()

        for scoreChange in range(scoreLabel):
            self.player1ScoreLabel.config(text = "%s's Score: %d" % (self.name, self.score + scoreChange + 1))
            self.player1ScoreLabel.update()
            time.sleep(0.05)
        frame.destroy()
        label.destroy()
    def isTouchingScoreboard(self, x, y):
        if x > self.scoreX - 25 and y < self.scoreY + 25:
            return True
        else:
            return False
    def getMovables(self, x, y):
        row = 0
        self.movables = []
        for letter in self.rack:
            self.movables.append(MovingLetter(self.root, letter, row*30+x, y+12.5, self.root))
            row += 1

        for movable in self.movables:
            movable.movables = []
            for movable2 in self.movables:
                movable.movables.append(movable2)

            movable.weedMovables()

        rackPositions = []
        for movable in self.movables:
            rackPositions.append((movable.x, movable.y))

        for movable in self.movables:
            movable.rackPositions = rackPositions

        for movable in self.movables:
            movable.getRackPosition()            
    def exchange(self):
        self.root.update_idletasks()
        
        self.exchangeWindow = Toplevel(self.root, height=self.screenHeight, \
                                  width = self.screenWidth)
        self.exchangeWindow.wm_title("Exchange")

        label = Label(self.exchangeWindow, text="Drag the letters you wish to exchange to the rack.", relief=RAISED)
        label.place(x=390, y=130, height=50, width=310)

        self.exchangeLetters = []
        for letterCount in range(len(self.rack)):
            self.exchangeLetters.append(MovingExchangeLetter(self.exchangeWindow, self.rack[letterCount], letterCount*30+250, 400, self.exchangeWindow))
        self.exchangeLetters[-1].getExchangeRack()
            
        button = Button(self.exchangeWindow, text="Back", command=self.exchangeWindow.destroy)
        button.place(x=500, y=360)

        exchangeButton = Button(self.exchangeWindow, text="Enter", command=self.getNewTiles)
        exchangeButton.place(x=550, y=230)        
    def getNewTiles(self, *event):
        toBeExchanged = []
        for exchangeLetter in self.exchangeLetters:
            if exchangeLetter.onExchangeRack:
                toBeExchanged.append(exchangeLetter.text)
        if toBeExchanged:
            for letter in toBeExchanged:
                self.rack.remove(letter)
            for movable in self.movables:
                movable.frame.place_forget()
            self.drawTiles()
            self.getMovables(self.x, self.y)
            for movable in self.movables:
                movable.board = self.board
                movable.getPositions()
                movable.returnToOrig()
            self.movables[-1].getBoard()
            self.exchangeWindow.destroy()
            self.endTurn()
        else:
            return False
    def setBoard(self):
        word = ""
        specialScores = {}
        for movable in self.movables:
            if not(movable.row == "NA"):
                word += movable.origText
                movable.row = int(movable.row)
                movable.column = int(movable.column)
                if self.board[movable.row][movable.column][0] != " " and \
                    self.board[movable.row][movable.column] != "*": #If it was ontop of a letter

                    #The extra scores
                    if self.board[movable.row][movable.column] in self.scoreList:

                        #Check for each of the types
                        if self.board[movable.row][movable.column] == "DLS":
                            self.addKey(specialScores, "DLS", movable.text)
                                
                        elif self.board[movable.row][movable.column] == "TLS":
                            self.addKey(specialScores, "TLS", movable.text)
                            
                        elif self.board[movable.row][movable.column] == "DWS":
                            self.addKey(specialScores, "DWS", "") #Don't need to show a letter because it just doubles the score
                                
                        else:
                            self.addKey(specialScores, "TWS", "")
                                
                        self.board[movable.row][movable.column] = movable.text
                        
                    else:
                        popup(self.root, "Letters Cannot Overlap", "Letters Cannot Overlap\n\n\n", \
                              self.screenHeight, self.screenWidth)
                        self.resetBoard()
                        self.enterButton.place(x=self.x+50, y=self.y+100)
                        return False
                else:
                    if self.board[movable.row][movable.column][0] == "*":
                        self.addKey(specialScores, "DWS", "")
                    self.board[movable.row][movable.column] = movable.text #Place the letter
                    
        return word, specialScores
    def getNewWord(self):
        self.enterButton.place_forget()
        #self.scoreAnimation(50, 245, 245, 500, 0, 50, 100) #Testing
        if self.board[8][8] == "*":
            isFirstTurn = True
        else:
            isFirstTurn = False
        places = []
        self.rows = []
        self.columns = []
        specialScores = {}
        for movable in self.movables:
            movable.row = movable.hoveringOver.split(",")[0]
            movable.column = movable.hoveringOver.split(",")[1]
            if movable.row != "NA":
                self.rows.append(movable.row)
                self.columns.append(movable.column)

        if self.rows:           
            wordAndScores = self.setBoard()
            if wordAndScores is False:
                self.resetBoard()
                self.enterButton.place(x=self.x+50, y=self.y+100)
                return False
            else:
                word = wordAndScores[0]
                specialScores = wordAndScores[1]
                if self.movableCheck(self.board):
                    boardCheck = self.checkWholeBoard(self.board, isFirstTurn)
                    if boardCheck[0]:
                        for scoreType in specialScores.keys():
                            if scoreType == "DWS" or scoreType == "TWS":
                                specialScores[scoreType] = self.movables[-1].sharedWord
                        self.newGetScore(specialScores)
                        if len(word) == 7:
                            popup(self.root, "Bingo!!!", "Bingo!!!\n\n\nYou used all your tiles!\n\n\n+50 points!", \
                                  self.screenHeight, self.screenWidth, closable = False)
                            self.score += 50
                            self.scoreAnimation(50, 245, 245, 500, 0, 50, 100)
                    
                        for movable in self.movables:
                            movable.frame.place_forget()
                        for letter in word:
                            self.rack.remove(letter)
                        self.drawTiles()
                        #self.movables[-1].boardFrame.destroy()
                        self.endTurn()
                    else:
                        if boardCheck[1] == "Invalid Word":
                            text = "Invalid Words: \n\n"
                            for invalidWord in boardCheck[2]:
                                text += invalidWord
                                text += "\n"
                            popup(self.root, "Invalid Word", text, self.screenHeight, self.screenWidth)
                            self.resetBoard()
                            if self.mode1 == "h" or self.mode1 == "H":
                                self.endTurn()
                        else:
                            popup(self.root, boardCheck[1], boardCheck[1], self.screenHeight, self.screenWidth)
                        self.enterButton.place(x=self.x+50, y=self.y+100)
                        #self.resetBoard()
                        return False
                else:
                    self.resetBoard()
                    self.enterButton.place(x=self.x+50, y=self.y+100)
                    return False
        else:
            popup(self.root, "No tiles played", "No tiles played\n\n\n", self.screenHeight, self.screenWidth)
            self.enterButton.place(x=self.x+50, y=self.y+100)
    def movableCheck(self, boardToCheck):
        for movable in self.movables:
            movable.words = []
            movable.wordIndexes = {}
        words = self.getBoardWords(boardToCheck)
        if type(words) == type({}):
            for (word, attributes) in words.items():
                for attribute in attributes:
                    for movable in self.movables:
                        if movable.row != "NA":
                            movable.attributes = self.getAttributes("%s,%s" % (movable.column, movable.row), self.board)
                            if str(movable.attributes) == str(attribute):
                                movable.wordIndexes[word] = attributes.index(movable.attributes)
                                movable.words.append(word)
                                
            sharedWords = []
            for movable in self.movables:
                if movable.row != "NA":
                    notWord = 0
                    for word in movable.words:
                        sharedWords.append(word)
                    if notWord >= len(movable.words):
                        popup(self.root, 'a', 'a', 50, 50)

            sharedWord = self.getMode(sharedWords)
            movablesInWord = 0
            for movable in self.movables:
                if sharedWord[0] in movable.words:
                    movablesInWord += 1
            if movablesInWord < sharedWord[1][0]:
                return False
            
            for movable in self.movables:
                if movable.row != "NA":
                    if sharedWord[0] in movable.wordIndexes.keys():
                        movable.wordIndex = movable.wordIndexes[sharedWord[0]]
                    else:
                        return False
            usedWordIndexes = []
            for movable in self.movables:
                if movable.row != "NA":
                    if movable.wordIndex in usedWordIndexes:
                        return False

                    else:
                        usedWordIndexes.append(movable.wordIndex)
            self.movables[-1].sharedWord = sharedWord
            return True
        else:
            return False    
    def getMode(self, listToSearch):
        itemNums = {}
        for item in listToSearch:
            self.addKey(itemNums, item, listToSearch.count(item))

        highest = max(itemNums.values())
        return list(itemNums.keys())[list(itemNums.values()).index(highest)], highest
    def resetBoard(self):
        for movable in self.movables:
            if movable.row != "NA":
                if movable.hoveringOver == "8,8":
                    self.board[int(movable.row)][int(movable.column)] = "*"
                elif movable.hoveringOver == "1,1" or movable.hoveringOver == "1,8" or \
                     movable.hoveringOver == "1,15" or movable.hoveringOver == "8,1" or \
                     movable.hoveringOver == "8,15" or movable.hoveringOver == "15,1" or \
                     movable.hoveringOver == "15,8" or movable.hoveringOver == "15,15":
                    self.board[int(movable.row)][int(movable.column)] = "TWS"
                elif movable.hoveringOver == "2,2" or movable.hoveringOver == "2,14" or \
                     movable.hoveringOver == "3,3" or movable.hoveringOver == "3,12" or \
                     movable.hoveringOver == "4,4" or movable.hoveringOver == "4,11" or \
                     movable.hoveringOver == "5,5" or movable.hoveringOver == "5,10" or \
                     movable.hoveringOver == "11,5" or movable.hoveringOver == "11,11" or \
                     movable.hoveringOver == "12,4" or movable.hoveringOver == "12,12" or \
                     movable.hoveringOver == "13,3" or movable.hoveringOver == "13,13":
                    self.board[int(movable.row)][int(movable.column)] = "DWS"
                elif movable.hoveringOver == "2,6" or movable.hoveringOver == "2,11" or \
                     movable.hoveringOver == "7,2" or movable.hoveringOver == "7,6" or \
                     movable.hoveringOver == "7,10" or movable.hoveringOver == "7,14" or \
                     movable.hoveringOver == "10,2" or movable.hoveringOver == "10,7" or \
                     movable.hoveringOver == "10,11" or movable.hoveringOver == "10,14" or \
                     movable.hoveringOver == "14,6" or movable.hoveringOver == "14,11":
                    self.board[int(movable.row)][int(movable.column)] = "TLS"
                elif movable.hoveringOver == "1,4" or movable.hoveringOver == "1,12" or \
                     movable.hoveringOver == "3,7" or movable.hoveringOver == "3,9" or \
                     movable.hoveringOver == "4,1" or movable.hoveringOver == "4,8" or \
                     movable.hoveringOver == "4,15" or movable.hoveringOver == "7,3" or \
                     movable.hoveringOver == "7,7" or movable.hoveringOver == "7,9" or \
                     movable.hoveringOver == "7,13" or movable.hoveringOver == "8,4" or \
                     movable.hoveringOver == "8,12" or movable.hoveringOver == "9,3" or \
                     movable.hoveringOver == "9,7" or movable.hoveringOver == "9,9" or \
                     movable.hoveringOver == "9,13" or movable.hoveringOver == "12,1" or \
                     movable.hoveringOver == "12,8" or movable.hoveringOver == "12,15" or \
                     movable.hoveringOver == "13,7" or movable.hoveringOver == "13,9" or \
                     movable.hoveringOver == "15,4" or movable.hoveringOver == "15,12":
                    self.board[int(movable.row)][int(movable.column)] = "DLS"
                else:
                    self.board[int(movable.row)][int(movable.column)] = " "

                movable.returnToOrig()
    def addKey(self, dictToCheck, key, value):
        """Check if the key already exists. If it does, add the value, otherwise create one with the value.
           Note: this algorithm assumes all keys in the dictionary are lists."""
        if dictToCheck.get(key):
            dictToCheck[key].append(value)
        else:
            dictToCheck[key] = [value]
    def endTurn(self):
        """End the turn by quitting the root."""
        for movable in self.movables:
            movable.frame.destroy()
        self.root.quit()
        self.root.withdraw()
        self.overRoot.quit()
        self.overRoot.withdraw()
        self.switchTurn = 1
    def getScore(self, specialScores):
        """Getting a score. Works by going through all the movables and expanding until not touching any tiles.
           Then, delete all the duplicates and add the special scores."""
        lettersToScore = []
        wordScore = 0
        for movable in self.movables:
            if movable.row != "NA":
               lettersToScore.append((movable.row, movable.column))

        for movable in self.movables:
            if movable.row != "NA":
                row = int(movable.row)
                column = int(movable.column)
                
                rowAdd = 0
                rowSub = 0
                colAdd = 0
                colSub = 0

                while (row + rowAdd <= 15 and row - rowSub >= 1 and \
                      column + colAdd <= 15 and column - colSub >= 1) and \
                      (self.board[row][column + colAdd][0] != " " or \
                      self.board[row][column - colSub][0] != " " or \
                      self.board[row + rowAdd][column][0] != " " or \
                      self.board[row - rowSub][column][0] != " "):

                    lettersToScore.append((column + colAdd, row))
                    lettersToScore.append((column - colSub, row))
                    lettersToScore.append((column, row + rowAdd))
                    lettersToScore.append((column, row - rowSub))
                    
                    rowAdd += 1
                    rowSub += 1
                    colAdd += 1
                    colSub += 1
                    
        lettersToScore = self.removeDuplicates(lettersToScore)
        
        for position in lettersToScore:
            letter = self.getAttributes("%d,%d" % (position[0], position[1]), self.board)['text']
            if letter[0] != " " and letter != "NA":
                if letter not in self.scoreList:
                    wordScore += self.scores[letter.lower()]

        for item in specialScores.items():
            scoreType = item[0]
            scoreLetters = item[1]
            if scoreType == "DLS":
                for letter in scoreLetters:
                    wordScore += self.scores[letter.lower()]
            elif scoreType == "TLS":
                for count in range(2):
                    for letter in scoreLetters:
                        wordScore += self.scores[letter.lower()]
        for item in specialScores.items(): #Double and Triple Word have to be evaluated last
            scoreType = item[0]
            if scoreType == "DWS":
                wordScore *= 2
            elif scoreType == "TWS":
                wordScore *= 3
        if len(self.rack) == 0:
            wordScore += 50 #If they played all their tiles, +50 points.
        lastX = -1000
        lastY = -1000
        for movable in self.movables:
            if movable.row != "NA":
                if movable.row * 31 > lastX:
                    lastX = movable.row * 31
                if movable.column * 31 > lastY:
                    lastY = movable.column * 31
        self.scoreAnimation(wordScore, lastX, lastY, 500, 0, 500, 500)
        
        self.score += wordScore

        self.updateSelfScore()
    def newGetScore(self, specialScores):
        wordsToScore = []
        for movable in self.movables:
            wordsToScore.extend(movable.words)
        wordsToScore = self.removeDuplicates(wordsToScore)
        
        wordScore = 0
        for word in wordsToScore:
            for letter in word:
                wordScore += self.scores[letter.lower()]
        for item in specialScores.items():
            scoreType = item[0]
            scoreLetters = item[1]
            if scoreType == "DLS":
                for letter in scoreLetters:
                    wordScore += self.scores[letter.lower()]
            elif scoreType == "TLS":
                for count in range(2):
                    for letter in scoreLetters:
                        wordScore += self.scores[letter.lower()]
        for item in specialScores.items(): #Double and Triple Word have to be evaluated last
            scoreType = item[0]
            scoreLetters = item[1][0]
            if scoreType == "DWS":
                for letter in scoreLetters:
                    wordScore += self.scores[letter.lower()]
            elif scoreType == "TWS":
                for count in range(2):
                    for letter in scoreLetters:
                        wordScore += self.scores[letter.lower()]
        lastX = -1000
        lastY = -1000
        for movable in self.movables:
            if movable.row != "NA":
                if movable.row * 31 > lastY:
                    lastY = movable.row * 31
                if movable.column * 31 > lastX:
                    lastX = movable.column * 31

        self.scoreAnimation(wordScore, lastX, lastY, 500, 0, 500, 500)
        
        self.score += wordScore

        self.updateSelfScore()                    
    def drawTiles(self):
        while len(self.rack) < 7:
            letter = random.choice(distribution)
            distribution.remove(letter)
            self.rack.append(letter.upper())            
    def checkWord(self, word):
        print(word, word.upper(), word.lower())
        if word in self.ospd or word.upper() in self.ospd or word.lower() in self.ospd:
            return True
        else:
            return False
    def removeDuplicates(self, oldList):
          newList = []
          for item in oldList:
            if item not in newList:
              newList.append(item)
          oldList = newList
          return newList        
    def getBoardWords(self, boardToCheck):
        touchingList = []
        for row in range(1, 16):
            for column in range(1, 16):
                attributes = self.getAttributes("%d,%d" % (row, column), boardToCheck)
                if attributes['text'][0] != " " and attributes['text'] not in self.scoreList:
                    touchingList.append(attributes)
        touchingList = self.removeDuplicates(touchingList)
        for item in touchingList:
            if item['numTouchingLetters'] == 0:
                return False, "Must Be Connected"
        preservedList = []
        for item in touchingList:
            preservedList.append(item)
        words = {}
        touchingListAcross = []
        touchingListDown = []
        for item in touchingList:
            touchingListAcross.append(item)
            touchingListDown.append(item)
        usedLetters = []
        while touchingList:
            wordAcross = ""
            wordStart = touchingList[0]
            column = wordStart['column']
            row = wordStart['row']
            wordLettersAcross = [wordStart]
            wordAcross += wordStart['text'][0]
            while wordStart['right'][0] != " " and wordStart['right'] != "NA":
                right = wordStart['right']
                column += 1
                for item in touchingList:
                    if item['text'] == right and \
                       item['column'] == column and \
                       item['row'] == row and \
                       item in touchingListAcross:
                        touchingListAcross.remove(item)
                        wordStart = item
                        wordAcross += wordStart['text'][0]
                        wordLettersAcross.append(wordStart)
                if wordStart in usedLetters:
                    break
                else:
                    usedLetters.append(wordStart)
            usedLetters = []
            wordDown = ""
            wordStart = touchingList[0]
            column = wordStart['column']
            row = wordStart['row']
            wordLettersDown = [wordStart]
            wordDown += wordStart['text'][0]
            while wordStart['down'][0] != " " and wordStart['down'] != "NA":
                down = wordStart['down']
                row += 1
                for item in touchingList:
                    if item['text'] == down and \
                       item['column'] == column and \
                       item['row'] == row and \
                       item in touchingListDown:
                        touchingListDown.remove(item)
                        wordStart = item
                        wordDown += wordStart['text'][0]
                        wordLettersDown.append(wordStart)
                if wordStart in usedLetters:
                    break
                else:
                    usedLetters.append(wordStart)
            touchingList.remove(touchingList[0])
            if len(wordAcross) > 1:
                words[wordAcross] = wordLettersAcross
            if len(wordDown) > 1:
                words[wordDown] = wordLettersDown

        return words
    def checkWholeBoard(self, boardToCheck, isFirstTurn):
        touchingList = []
        for row in range(1, 16):
            for column in range(1, 16):
                attributes = self.getAttributes("%d,%d" % (row, column), boardToCheck)
                if attributes['text'][0] != " " and attributes['text'] not in self.scoreList:
                    touchingList.append(attributes)
        touchingList = self.removeDuplicates(touchingList)
        for item in touchingList:
            if item['numTouchingLetters'] == 0:
                return False, "Must Be Connected2"
        words = self.getBoardWords(boardToCheck)
        #Checking that words are contiguous algorithm is below.
        if isFirstTurn and boardToCheck[8][8][0] != "*":
            pass
        else:
            if isFirstTurn and boardToCheck[8][8][0] == "*":
                return False, "Must Touch Star"
            else:
                for word in words:
                    letters = words[word]
                    totalTouching = 0
                    for letter in letters:
                        totalTouching += letter['numTouchingLetters']

                    if isFirstTurn:
                        minimumTouching = (len(word) * 2) - 2
                    else:
                        minimumTouching = (len(word) * 2) - 1
                    if not(totalTouching >= minimumTouching):
                        return False, "Must Be Connected"
        
        incorrectWords = []
        if len(words) < 1:
            return False
        else:
            for word in words:
                if not(self.checkWord(word.lower())):
                    incorrectWords.append(word)
            
        if incorrectWords:
            return False, "Invalid Word", incorrectWords
        else:
            return True, words     
    def getAttributes(self, place, boardToCheck):
        touching = {}
        place = place.split(',')
        row = int(place[1])
        column = int(place[0])
        numTouching = 0
        if not row-1<1:
            up = boardToCheck[row-1][column]
            touching['up'] = up
            if up.upper() in string.ascii_uppercase:
                numTouching += 1

        else:
            touching['up'] = 'NA'
            
        if not row+1>15:
            down = boardToCheck[row+1][column]
            touching['down'] = down
            if down.upper() in string.ascii_uppercase:
                numTouching += 1

        else:
            touching['down'] = 'NA'

        if not column+1 > 15:
            right = boardToCheck[row][column+1]
            touching['right'] = right
            if right.upper() in string.ascii_uppercase:
                numTouching += 1
        else:
            touching['right'] = 'NA'

        if not column-1 < 1:
            left = boardToCheck[row][column-1]
            touching['left'] = left
            if left.upper() in string.ascii_uppercase:
                numTouching += 1
        else:
            touching['left'] = 'NA'
            

        touching['numTouchingLetters'] = numTouching
        touching['row'] = row
        touching['column'] = column
        touching['text'] = boardToCheck[row][column]
        return touching
    def checkWord(self, word):
        if word in self.ospd:
            return True
        else:
            return False
    def returnMovables(self):
        for movable in self.movables:
            movable.returnToOrig()
    def shuffleRack(self):
        random.shuffle(self.rack)
        for movable in self.movables:
            movable.frame.destroy()
        self.getMovables(self.x, self.y)

class AI(Player): #WIP. Just contemplating what would be good functions to use. not even starting. HUGE undertaking.
    def __init__(self):
        self.extraList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
             "TWS", "DWS", "TLS", "DLS", \
             "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ", \
             "*", " "]
        #Need (so far): board, score, rack
    def getAllWordsOnRack(self):
        self.getAllCorrectCombinations(self, self.rack, len(self.rack))
    def getAllCorrectCombinations(self, iterable, maxDepth):
        allWords = []
        for depth in range(0, maxDepth + 1):
            for word in itertools.permutations(iterable, depth):
                allWords.append(word)
        correctWords = []
        for word in allWords:
            if self.checkWord(word):
                correctWords.append(word)
        return correctWords
    def checkWord(self, word):
        super(AI, self).checkWord(word)
    def getAttributes(self, place, boardToCheck):
        super(AI, self).getAttributes(place, boardToCheck)
    def getAllOpenLetters(self):
        possibleList = []
        for row in range(len(self.board)):
            for column in range(len(row)):
                possibleList.append(self.getAttributes("%d,%d" % (column, row), self.board))
                
        tempList = []
        for i in possibleList: tempList.append(i) #So that when things are deleted from possibleList
                                                  #the size doesn't change and items are not skipped.
        for letter in tempList:
            if letter["text"] in self.extraList:
                possibleList.remove(letter)
                
        tempList = []
        for i in possibleList: tempList.append(i)
        for letter in tempList:
            if letter["numTouchingLetters"] > 2:
                possibleList.remove(letter)

        for letter in possibleList:
            letter["depth"] = self.getDepth(letter)
            
        tempList = []
        for i in possibleList: tempList.append(i)
        for letter in tempList:
            if letter["depth"] < 3: #Has to have at least 3 empty spots from it to be considered "open".
                possibleList.remove(letter)

        return possibleList
    def getDepth(self, attributes):
        upDepth = 0
        downDepth = 0
        leftDepth = 0
        rightDepth = 0
        if attributes["up"] == " ":
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column, row-1), self.board)
            while newLetter["up"] in self.extraList:
                upDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column, row-1), self.board)
        if attributes["down"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column, row+1), self.board)
            while newLetter["down"] in self.extraList:
                downDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column, row+1), self.board)
        if attributes["left"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column-1, row), self.board)
            while newLetter["left"] in self.extraList:
                leftDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column-1, row), self.board)
        if attributes["right"] == " ":
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column+1, row), self.board)
            while newLetter["right"] in self.extraList:
                rightDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column+1, row), self.board)
        if leftDepth == 0 or rightDepth == 0:
            return upDepth + downDepth
        elif upDepth == 0 or downDepth == 0:
            return leftDepth + rightDepth
    def getOpenWords(self):
        words = []
        for letter in self.getAllOpenLetters():
            words.extend(self.getAllCorrectCombinations(self.rack+letter["text"], letter["depth"]))
        return words
    def getHookableLetters(self):
        pass
    def getHookWords(self):
        pass
    def getMoves(self):
        allPossibleWords = self.getHookWords() + self.getOpenWords()
    def getBestMove(self):
        moves = self.getMoves()
        bestMove = {"score":0}
        for move in moves:
            if move["score"] > bestMove["score"]:
                bestMove = move
        return bestMove
    def playMove(self):
        pass
    def resetBoard(self):
        pass
    def endTurn(self):
        pass
    
class Game():
    def __init__(self, name1, name2, mode1, mode2):
         self.root = Tk()
         self.root2 = Tk()
         self.mainRoot = Tk()
         self.mainRoot.withdraw()

         self.name1 = name1
         self.name2 = name2
         self.mode1 = mode1[0]
         self.mode2 = mode2[0]

         self.gameNum = -1
         self.gameAlreadyInFile = False
    def startGame(self):
        self.player1 = Player(self.root, 1, self.name1, 150, 550, self.mode1, self.mode2)
        self.player2 = Player(self.root2, 2, self.name2, 150, 550, self.mode1, self.mode2)
        self.playerGoing = 1
        
        self.scoreRoot = Toplevel(self.root)
        self.scoreWindow = Toplevel(self.scoreRoot)
        self.scoreWindow.wm_title("Scoreboard")
        self.scoreRoot.withdraw()
        self.scoreWindow.resizable(0, 0)
        self.scoreWindow.geometry("%dx%d%+d%+d"%(200, 75, 700, 0))
        self.player1ScoreLabel = Label(self.scoreWindow, text="%s's Score: %d" % (self.player1.name, self.player1.score), height=1, width=20, relief=SUNKEN)
        self.player2ScoreLabel = Label(self.scoreWindow, text="%s's Score: %d" % (self.player2.name, self.player2.score), height=1, width=20, relief=SUNKEN)
        self.player1ScoreLabel.grid(row=1, column=1)
        self.player2ScoreLabel.grid(row=2, column=1)
        self.tilesLabel = Label(self.scoreWindow, text = "%d tiles left" % len(distribution), height = 1, width = 20)
        self.player1ScoreLabel.grid(row=1, column=1)
        self.player2ScoreLabel.grid(row=2, column=1)
        self.tilesLabel.grid(row = 3, column = 1)        
    def updateScores(self):
        self.player1ScoreLabel.config(text = "%s's Score: %d" % (self.player1.name, self.player1.score))
        self.player2ScoreLabel.config(text = "%s's Score: %d" % (self.player2.name, self.player2.score))
        self.tilesLabel.config(text = "%d tiles left" % len(distribution))        
    def doTurn(self):
        if self.playerGoing == 1:
            self.root1 = Toplevel(self.root)
            self.player1.reRoot(self.root1)
            self.player1.startTurn(self.player2.name, self.player2.score)
            self.player2.board = self.player1.board
            self.playerGoing = 2
            popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player2.name, self.player1.screenHeight, self.player1.screenWidth)
        else:
            self.root2 = Toplevel(self.root)
            self.player2.reRoot(self.root2)
            self.player2.startTurn(self.player1.name, self.player1.score)
            self.player1.board = self.player2.board
            self.playerGoing = 1
            popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player1.name, self.player2.screenHeight, self.player2.screenWidth)
        if self.gameAlreadyInFile is False:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = False)
            self.gameAlreadyInFile = True
        else:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = True)
    def main(self):
        #self.startGame()
        if self.mode2.lower() == "n":
            while len(distribution) > 0 or (len(self.player1.rack) > 0 and len(self.player2.rack) > 0):
                self.doTurn()
                self.updateScores()
        else:
            while self.player1.score < 75 and self.player2.score < 75:
                self.doTurn()
                self.updateScores()
        if self.player1.score > self.player2.score:
            popup(root, "Player 1 Won", "Player 1 Won", self.player1.screenHeight, self.player1.screenWidth)
        else:
            popup(root, "Player 2 Won", "Player 2 Won", self.player2.screenHeight, self.player2.screenWidth)
        self.player1.root.destroy()
        self.player2.root.destroy()
        self.mainRoot.destroy()

###Algorithms for saving games below.
class SavedGame(Game):
    def __init__(self, root, file="savedGame.txt"):
        self.root = Toplevel(root)
        self.root.withdraw()
        self.gameWindow = Toplevel(self.root, height = root.winfo_screenheight(), width = root.winfo_screenwidth())
        self.gameWindow.resizable(0,0)
        self.gameWindow.wm_title("Saved Games")
        gameTexts = open(file).read()
        gameTexts.split("New Game\n")
        gameTexts = [gameTexts]
        self.gameTexts = gameTexts
        gameLabels = []
        gameButtons = []
        deleteButtons = []
        for gameText in gameTexts:
            fullText = self.setGameVars(gameText)
            text = """%s's score: %s
%s's score: %s
Mode 1: %s
Mode 2: %s""" % (fullText[0], fullText[1], fullText[2], fullText[3], fullText[4], fullText[5])
            gameLabel = Label(self.gameWindow, text=text, height=4, width=20, relief=RAISED) #Definetly changeable
            gameLabels.append(gameLabel)
            gameLabels[-1].place(x=0, y=0)
            
            gameButton = Button(self.gameWindow, text="Play!", height=1, width=5, \
                                command=lambda game=gameText: self.play(game))
            gameButtons.append(gameButton)
            gameButtons[-1].place(x=(gameTexts.index(gameText)*100)+350, y=(gameTexts.index(gameText)*100))
    def setGameVars(self, gameText):
            gameText = gameText.split("\n")
            del gameText[0]
            p1Atts = gameText[0].split()
            p2Atts = gameText[1].split()
            score1, score2 = p1Atts[-1], p2Atts[-1]
            del p1Atts[-1]
            del p2Atts[-1]
            name1 = ""
            for namePiece in p1Atts:
                name1 += namePiece
                name1 += " "
            name2 = ""
            for namePiece in p2Atts:
                name2 += namePiece
                name2 += " "

            tiles = gameText[2].split(",")
            
            modes = gameText[3].split()
            if modes[0] == "n":
                    mode1 = "normal"
            else:
                    mode1 = "hardcore"
            
            if modes[1] == "n":
                    mode2 = "normal"
            else:
                    mode2 = "short"
            playerGoing = int(modes[2])
            rack1 = list(gameText[4])
            rack2 = list(gameText[5])
            
            del gameText[:6]
            
            board = []
            currentRowIndex = 0
            for row in gameText:
                    board.append([])
                    parse = row.split("|")
                    for column in parse:
                            board[currentRowIndex].append(column)
                    del board[currentRowIndex][-1]
                    currentRowIndex += 1
            del board[-1]
            return name1, score1, name2, score2, mode1, mode2, board, rack1, rack2, playerGoing
    def play(self, gameText):
        global played
        played = 1
        self.gameNum = self.gameTexts.index(gameText)
        self.gameAlreadyInFile = True
        gameVars = self.setGameVars(gameText)
        popup(root, "Pass Device", "Pass Device to %s\n\n" % [gameVars[0], gameVars[2]][gameVars[9]-1], root.winfo_screenheight(), root.winfo_screenwidth())
        super(SavedGame, self).__init__(gameVars[0], gameVars[2], gameVars[4], gameVars[5])
        self.gameWindow.destroy()
        self.startGame()
        self.player1.board, self.player2.board = gameVars[6], gameVars[6]
        self.player1.score, self.player2.score = int(gameVars[1]), int(gameVars[3])
        self.player1.rack, self.player2.rack = gameVars[7], gameVars[8]
        self.playerGoing = gameVars[9]
        self.main()
        played = 0
    def startGame(self):
        super(SavedGame, self).startGame()
    def updateScores(self):
        super(SavedGame, self).updateScores()
    def doTurn(self):
        super(SavedGame, self).doTurn()
    def main(self):
        super(SavedGame, self).main()
def playSavedGame(file="savedGame.txt"):
        #popup(root, "Under construction", "Under construbtion\n\n\n", \
     #     root.winfo_screenheight(), root.winfo_screenwidth())
    if len(open(file).read()) > 0:
##        try:
##            del scrabble
##        except NameError:
##            pass
##        finally:
##            global scrabble
        played = 1
        global scrabble
        scrabble = SavedGame(root)
        played = 0
    else:
        popup(root, "No saved games", "No saved games\n\n\n", root.winfo_screenheight(), root.winfo_screenwidth())
def writeVars(game, file):
    file.write("New Game\n")
    
    file.write("%s %d\n" % (game.player1.name, game.player1.score))
    file.write("%s %d\n" % (game.player2.name, game.player2.score))
    for letter in distribution:
        file.write(letter)
        file.write(",")
    file.write("\n")
    file.write("%s %s %d\n" % (game.mode1, game.mode2, game.playerGoing))
    game.player1.drawTiles()
    game.player2.drawTiles()
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
##    os.ftruncate(file, 0)
##    os.lseek(file, 0, os.SEEK_SET)
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
    #print(gameAlreadyInFile)
    if not gameAlreadyInFile:
        file = open(file, "w")
        writeVars(game, file)
    else:
        file = open(file, "r+")
        fileText = file.read().split("New Game\n")
        text = "%s %d\n%s %d\n" % (game.player1.name, game.player1.score, game.player2.name, game.player2.score)
        for letter in distribution:
            text += letter
            text += ","
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

        fileText[gameNum] = text
        setFileTextToList(fileText)

        
def instructions():
    text = """Instructions for Scrabble:

    You get a rack of 7 tiles to start the game. You must play words with these
    7 tiles so that each word formed vertically and horizontally is a word.

    "?" tiles are blank tiles. They can be played as any letter and are worth
    no points.
    
    Note: When you play a word, make sure that all the tiles are connected to a
    previously played word.
    
    You get a certain amount of points based on the letters you played.
    Special Score Tiles:
    \tTWS (triple word score): Multiplies your score for that turn by 3.
    \tDWS (double word score): Multiplies your score for that turn by 2.
    \tTLS (triple letter score): Multiplies your score for that letter by 3.
    \tDLS (double letter score): Multiplies your score for that letter by 2.
    
    Once you play a word, you draw tiles until you have seven again.
    The game ends when there are no tiles left in the bag.

    Modes:
    Normal: wrong word -> continue
    Hardcore: wrong word -> lose turn

    Normal: play until no tiles in bag
    Short: play to 75 points"""

    popup(root, "Instructions", text, root.winfo_screenheight(), root.winfo_screenwidth())
def mode1questions():
    text="""Normal: wrong word --> continue
    Hardcore: wrong word --> lose turn."""
    popup(root, "Mode 1 Description", text, root.winfo_screenheight(), root.winfo_screenwidth())
def mode2questions():
    text="""Normal: play until bag and one of the player's racks are empty
    Short: play until one person reaches 75 points.\n\n\n
    Note: normal play can take at least an hour, but short play is very fast."""
    popup(root, "Mode 2 Description", text, root.winfo_screenheight(), root.winfo_screenwidth())    
def play():
    global enterWindow, name1Var, name2Var, mode1Var, mode2Var, played

    played = 1
    enterWindow = Toplevel(root, height = root.winfo_screenheight(),\
                           width = root.winfo_screenwidth())
    enterWindow.wm_title("Enter Names and Modes")

    label1 = Label(enterWindow, text = "Enter name 1:")
    label1.place(x = 50, y = 50, height = 20, width = 95)
    name1Var = StringVar()
    name1Var.set("Name 1")
    name1 = Entry(enterWindow, textvariable=name1Var)
    name1.place(x = 150, y = 50, height = 20, width = 100)

    label2 = Label(enterWindow, text = "Enter name 2:")
    label2.place(x = 50, y = 175, height = 20, width = 95)
    name2Var = StringVar()
    name2Var.set("Name 2")
    name2 = Entry(enterWindow, textvariable=name2Var)
    name2.place(x = 150, y = 175, height = 20, width = 100)

    mode1Label = Label(enterWindow, text = "Enter mode 1 (normal or hardcore):")
    mode1Label.place(x = 50, y = 295, height = 20, width = 210)
    mode1Var = StringVar()
    mode1Var.set("Mode 1")
    mode1 = Entry(enterWindow, textvariable=mode1Var)
    mode1.place(x = 270, y = 295, height = 20, width = 100)

    mode1Questions = Button(enterWindow, text= "?", command = mode1questions)
    mode1Questions.place(x=370, y=280, height=50, width=50)
    
    mode2Label = Label(enterWindow, text = "Enter mode 2 (normal or short):")
    mode2Label.place(x = 50, y = 465, height = 20, width = 200)
    mode2Var = StringVar()
    mode2Var.set("Mode 2")
    mode2 = Entry(enterWindow, textvariable=mode2Var)
    mode2.place(x = 270, y = 465, height = 20, width = 100)

    mode2Questions = Button(enterWindow, text = "?", command = mode2questions)
    mode2Questions.place(x=370, y=450, height=50, width=50)
    
    enterButton = Button(enterWindow, text = "Enter data", command = checkData)
    enterButton.place(x = 100, y = 500)
def check(string, validInputs, popupHeader, popupText):
    if string in validInputs:
        return True
    else:
        popup(root, popupHeader, popupText, root.winfo_screenheight(), root.winfo_screenwidth())
        return False
def checkData():
    if check(mode1Var.get(), ['n', 'h', 'N', 'H', 'normal', 'hardcore'], "Invalid Mode 1", "Invalid Mode 1"):
        if check(mode2Var.get(), ['n', 's', 'N', 'S', 'normal', 'short'], "Invalid Mode 2", "Invalid Mode 2"):
            played = 1
            enterWindow.destroy()
            popup(root, "Pass Device", "Pass Device to %s\n\n" % name1Var.get(), root.winfo_screenheight(), root.winfo_screenwidth())
            global scrabble
            scrabble = Game(name1Var.get(), name2Var.get(), mode1Var.get(), mode2Var.get())
            scrabble.startGame()
            scrabble.main()
            played = 0
def scrabbleDestroy():
    print(played)
    if played == 1:
        print(scrabble)
        #writeAllGames([scrabble])
        writeAllGames([scrabble, scrabble])
        try:
            scrabble.root.destroy()
        except:
            pass
def exitGame():
    scrabbleDestroy()
    root.destroy()
    quit()
distribution = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r", "r", "r","s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", "v", "v", "w", "w", "x", "y", "y", "z", "?", "?"] #"?" is a blank tile, can be any letter.
               # "?", "?", "?", "?", "?", "?", "?", "?","?", "?","?", "?", "?", "?"] #Just for fun :)
welcomeLabel = Label(root, text = "Welcome to Scrabble in Python!")
instructionsButton = Button(root, text = "Instructions", command = instructions)
playButton = Button(root, text = "Play", command = play)
playSavedButton = Button(root, text = "Play Saved Game", command = playSavedGame)
exitButton = Button(root, text = "Exit", command = exitGame)

welcomeLabel.place(x = 40, y = 0)
instructionsButton.place(x = 90, y = 50)
playButton.place(x = 110, y = 100)
playSavedButton.place(x = 76, y = 150)
exitButton.place(x = 112, y = 200)

root.mainloop()
