class MovingLetter():
    def __init__(self, root, text, x, y, frame):
        self.board = [['  ', 'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J ', 'K ', 'L', 'M', 'N', 'O'],
     ['01 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['02 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['03 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['04 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['05 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['06 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['07 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['08 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '* ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['09 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['10 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['11 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['12 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['13 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['14 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['15 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']]   
        self.root = root
        self.rackFrame = frame
        self.x = x
        self.y = y

        self.origX = x
        self.origY = y

        self.text = text
        
        self.f = Frame(self.rackFrame, bd=1, relief=SUNKEN)
        self.f.place(x=self.x, y=self.y, width=25, height=25)

        self.l = Label(self.f, bd=1, relief=RAISED, text=text, width=25)
        self.l.pack(fill=X, padx=1, pady=1)

        self.l.bind('<ButtonPress-1>', self.startMoveWindow)
        self.l.bind('<B1-Motion>', self.MoveWindow)
        self.f.bind('<ButtonPress-1>', self.startMoveWindow)
        self.f.bind('<B1-Motion>', self.MoveWindow)
        self.l.bind("<ButtonRelease-1>", self.checkForReturn)
        self.f.bind("<ButtonRelease-1>", self.checkForReturn)
        self.f.lift()

        self.hoveringOver = "%s,%s" % ("NA", "NA")
        self.getPositions()
    def startMoveWindow(self, event):
        self.lastX, self.lastY = event.x_root, event.y_root

    def MoveWindow(self, event):
        self.root.update_idletasks()
        self.x += event.x_root - self.lastX
        self.y += event.y_root - self.lastY
        self.lastX, self.lastY = event.x_root, event.y_root
        self.f.place_configure(x=self.x, y=self.y)

        f1Position = (self.x, self.y)
        for labelPosition in self.labels_positionList.keys():
            if self.isTouching(f1Position, labelPosition,
                               self.f.winfo_width(), self.f.winfo_height(),
                               25, 25):
                self.f.place_configure(x=labelPosition[0], y=labelPosition[1])
                self.hoveringOver = "%d,%d" % (self.labels_positionList[(labelPosition[0], labelPosition[1])][0],
                                               self.labels_positionList[(labelPosition[0], labelPosition[1])][1])
                #print(self.hoveringOver)

        if not(self.isTouching(f1Position, (0, 0),
                          self.f.winfo_width(), self.f.winfo_height(),
                          481, 481)):
            self.f.place_configure(x=self.origX, y=self.origY)
        self.f.lift()
        
    def isTouching(self, position1, position2, width1, height1, width2, height2):
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
        
    def checkForReturn(self, event):
        f1Position = (self.x, self.y)
        if not(self.isTouching(f1Position, (self.boardX, self.boardY),
                          self.f.winfo_width(), self.f.winfo_height(),
                          self.boardWidth, self.boardHeight)):
            self.f.place_configure(x=self.origX, y=self.origY)
            self.hoveringOver = "NA,NA"
    def getPositions(self):
        self.labels_positionList = {}
        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                if not(label[0] == "0" or label[0] == "1" or label[0].isalpha()):
                    self.labels_positionList[((i*30)+2.5, (j*30)+2.5)] = (j, i)

        self.boardWidth, self.boardHeight = 481, 481
        self.boardX, self.boardY = 0, 0
        
    def _update(self, board):
        self.board = board
        self.getPositions()

    def getBoard(self):
        self.boardFrame = Frame(self.root, bd=1, relief=SUNKEN)
        self.boardFrame.place(x=0, y=0, width=481, height = 481)
        labels = list()
        squares = list()

        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                entry = Frame(self.boardFrame, bd=1, relief=RAISED)
                entry.place(x=(i*30), y=(j*30), width=30, height=30)
                if label[0] == "0" or label[0] == "1" or label[0].isalpha():
                    labels.append(Label(entry, text = label,
                                        height = 30, width = 30))
                    labels[-1].pack()
                else:
                    squares.append(Label(entry, text=label,
                                         height=30, width=30))
                    squares[-1].pack()
    def returnToOrig(self):
        self.x = self.origX
        self.y = self.origY
        self.f.place_configure(x=self.x, y=self.y)
        self.hoveringOver = "NA,NA"

class Player():
    def __init__(self, playerNumber, name, x, y):
        self.board = [['  ', 'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J ', 'K ', 'L', 'M', 'N', 'O'],
     ['01 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['02 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['03 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['04 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['05 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['06 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['07 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['08 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '* ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['09 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['10 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['11 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['12 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['13 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['14 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['15 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']]
        self.distribution = ["a", "a", "a", "a", "a", "a", "a", "a", "a", \
                        "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", \
                        "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", \
                        "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", \
                        "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", \
                        "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", \
                        "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", \
                        "r", "r", "r", "r", "r", "r", "s", "s", "s", "s", \
                        "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", \
                        "v", "v", "w", "w", "x", "y", "y", "z"]
        

        self.conversion = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, \
              'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, \
                            '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, '11':11, \
                           '12':12, '13':13, '14':14, '15':15}
        self.ospd = open("dict.txt").read().split() #taken from http://www.puzzlers.org/pub/wordlists/ospd.txt
        self.lastBoard = [['  ', 'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J ', 'K ', 'L', 'M', 'N', 'O'],
     ['01 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['02 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['03 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['04 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['05 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['06 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['07 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['08 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '* ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['09 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['10 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['11 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['12 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['13 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['14 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
     ['15 ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']]

        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10}
        self.score = 0
        self.playerNumber = playerNumber
        self.name = name
        
        self.rack = []
        self.drawTiles()
        
        self.x = x
        self.y = y
        
        self.root = Tk()
        if self.board is self.lastBoard:print("HIIHI")
        else: print("rjg")
    def startTurn(self):
        self.root.title("%s's Turn" % self.name)
        self.root.resizable(0,0)
        self.root.geometry("%dx%d%+d%+d"%(550, 700, 0, 0))


        self.rackFrame = Frame(self.root, bd=1, relief=RAISED)
        self.rackFrame.place(x=self.x-50, y=self.y, width=300, height=50)

        self.getMovables(self.x, self.y)

        self.rackFrame.lower()
        self.movables[-1].getBoard()

        self.enterButton = Button(self.root, text = "Enter Word", command = self.getNewWord)
        self.enterButton.place(x=self.x+50, y=self.y+100)
        
    def getMovables(self, x, y):
        row = 0
        self.movables = []
        for letter in self.rack:
            self.movables.append(MovingLetter(self.root, letter, row*30+x, y+12.5, self.root))
            row += 1
    def placeWord(self, word, place, direction):
        start = board[int(place[1])][self.conversion[place[0]]]
        length = len(word)
        for num in range(length):
            row = int(place[1])
            column = self.conversion[place[0]]
            if direction == 'A':
                column += num
                if not(column > 15):
                    if self.board[row][column] not in string.ascii_uppercase: #checks if space isn't letter
                        self.board[row][column] = word[num]
                    else:
                        if not(column+1 > 15):
                            self.board[row][column + 1] = word[num]
                        else:
                            return False
                else:
                    return False
            else:
                row += num
                if not(row > 15):
                    if self.board[row][column] not in string.ascii_uppercase: 
                        self.board[row][column] = word[num]
                    else:
                        if not(row+1 > 15):
                            self.board[row+1][column] = word[num]
                        else:
                            return False
                else:
                    return False
        return True
    
    def getNewWord(self):
        word = ""
        board = self.board
        places = []
        rows = []
        columns = []
        for movable in self.movables:
            movable.row = movable.hoveringOver.split(",")[0]
            movable.column = movable.hoveringOver.split(",")[1]
        for movable in self.movables:
            if not(movable.row == "NA"):
                movable.row = int(movable.row)
                movable.column = int(movable.column)
                if board[movable.row][movable.column] != "  " and board[movable.row][movable.column] != "* ":
                    print("INVALID WORD")
                    for movable in self.movables:
                        movable.returnToOrig()
                    return False
                else:
                    board[movable.row][movable.column] = movable.text

        if self.lastBoard is self.board: print("shpiparlo")
        else: print("YES")
        self.board = board
        if self.lastBoard == self.board: print("IHWEOFIWHEF")
        else: print("HI")
       # if self.checkContiguous(): 
        if self.checkWholeBoard():
            for movable in self.movables:
                movable.f.place_forget()
            for letter in self.rack:
                self.rack.remove(letter)
            self.drawTiles()
            self.getMovables(self.x, self.y)
            for movable in self.movables:
                movable.board = self.board
                movable.returnToOrig()
            self.movables[-1].getBoard()
            #return word
            self.lastBoard = self.board
        else:
            if self.lastBoard == self.board: print("IHEF")
            else: print("HIuu")
            print("INVALID WORD") #self.popup(self.root, "Invalid Word", "Invalid Word\n", self.root.winfo_screenheight(), self.root.winfoscreenwidth())
            self.board = self.lastBoard
            for movable in self.movables:
                movable.returnToOrig()
            #return False
        if self.lastBoard == self.board: print("IHWEOFIWHEF")
        else: print("HI")
        self.displayBoard(self.board)
        self.displayBoard(self.lastBoard)
##        else:
##            print("INVALID WORD")
##            self._undo(self.lastBoard)
##            for movable in self.movables:
##                movable.returnToOrig()
    def _update(self, newBoard):
        self.board = newBoard

    def _undo(self, oldBoard):
        self.board = oldBoard
        
    def checkContiguous(self):
        return True
    
    def displayBoard(self, board):
        count = 0
        text = ""
        text += "|"
        for i in range(16):
            line = board[i]
            for j in line:
                text += j
                text += "|"
                count += 1
                if count == 16 and i != 15:
                    text += "\n"
                    text += "-" * 34
                    text += "\n"
                    text += "|"
                    count = 0
        text += "\n"
        print(text)

    def getScore(self, word): #Rudimentary; does not include hooked letters.
        self.lastWordScore = 0
        for letter in word:
            self.lastWordScore += scores[letter]
        self.score += self.lastWordScore

    def drawTiles(self):
        while len(self.rack) < 7:
            letter = random.choice(self.distribution)
            self.distribution.remove(letter)
            self.rack.append(letter.upper())
            
    def checkWord(self, word):
        if word in self.ospd:
            return True
        else:
            return False

    def removeDuplicates(self, oldList):
          newList = []
          for item in oldList:
            if item not in newList:
              newList.append(item)
          return newList

    def checkWholeBoard(self):
        touchingList = []
        for row in range(1, 16):
            for column in range(1, 16):
                attributes = self.getAttributes("%d,%d" % (row, column))
                if attributes['text'] != "  ":
                    touchingList.append(attributes)
        touchingList = self.removeDuplicates(touchingList)
        preservedList = []
        for item in touchingList:
            preservedList.append(item)
        words = []
        touchingListAcross = []
        touchingListDown = []
        for item in touchingList:
            if item['right'] != "NA":
                touchingListAcross.append(item)
            if item['down'] != "NA":
                touchingListDown.append(item)
        usedLetters = []
        while touchingList:
            wordAcross = ""
            wordStart = touchingList[0]
            column = wordStart['column']
            row = wordStart['row']
            wordAcross += wordStart['text'][0]
            while wordStart['right'] != "  " and wordStart['right'] != "NA":
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
                        if wordStart['text'] == "Y ":
                            print(wordStart)
                if wordStart in usedLetters:
                    break
                else:
                    usedLetters.append(wordStart)
            usedLetters = []
            wordDown = ""
            wordStart = touchingList[0]
            column = wordStart['column']
            row = wordStart['row']
            wordDown += wordStart['text'][0]
            while wordStart['down'] != "  " and wordStart['down'] != "NA":
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
                if wordStart in usedLetters:
                    break
                else:
                    usedLetters.append(wordStart)
            touchingList.remove(touchingList[0])
            if len(wordAcross) > 1:
                words.append(wordAcross)
            if len(wordDown) > 1:
                words.append(wordDown)
        print(words)
        if len(words) < 1:
            return False
        else:
            for word in words:
                if not(self.checkWord(word.lower())):
                    return False


        return True
        
    def getAttributes(self, place):
        touching = {}
        place = place.split(',')
        row = int(place[1])
        column = self.conversion[place[0]]
        numTouching = 0
        if not row-1<1:
            up = self.board[row-1][column]
            #print(up)
            touching['up'] = up
            if up[0].isalpha():
                numTouching += 1

        else:
            touching['up'] = 'NA'
            
        if not row+1>15:
            down = self.board[row+1][column]
            #print(down)
            touching['down'] = down
            if down[0].isalpha():
                numTouching += 1

        else:
            touching['down'] = 'NA'

        if not column+1 > 15:
            right = self.board[row][column+1]
            #print(right)
            touching['right'] = right
            if right[0].isalpha():
                numTouching += 1
        else:
            touching['right'] = 'NA'

        if not column-1 < 1:
            left = self.board[row][column-1]
            #print(left)
            touching['left'] = left
            if left[0].isalpha():
                numTouching += 1
        else:
            touching['left'] = 'NA'
            

        touching['numTouchingLetters'] = numTouching
        touching['row'] = row
        touching['column'] = column
        touching['text'] = self.board[row][column]
        return touching

    def checkWord(self, word):
        if word in self.ospd:
            return True
        else:
            return False

def popup(root, text):
    length = len(text)
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    
from tkinter import *
import random

player1 = Player(1, 's', 150, 550)
player1.startTurn()
player1.root.mainloop()
