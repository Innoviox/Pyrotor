
class MovingLetter():
    def __init__(self, root, text, x, y, frame):
        self.board = [[' ', 'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J ', 'K ', 'L', 'M', 'N', 'O'],
     ['01 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['02 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['03 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['04 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['05 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['06 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['07 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['08 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['09 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['10 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['11 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['12 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['13 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['14 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['15 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]  
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
        self.board = [[' ', 'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J ', 'K ', 'L', 'M', 'N', 'O'],
     ['01 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['02 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['03 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['04 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['05 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['06 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['07 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['08 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['09 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['10 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['11 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['12 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['13 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['14 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
     ['15 ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        
        self.ospd = open("dict.txt").read().split() #taken from http://www.puzzlers.org/pub/wordlists/ospd.txt


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

        self.returnButton = Button(self.root, text = "Return", command = self.returnMovables)
        self.returnButton.place(x=self.x+150, y=self.y+100)

        self.exchangeButton = Button(self.root, text = "Exchange", command= self.exchange)
        self.exchangeButton.place(x = self.x-50, y=self.y+100)
    def getMovables(self, x, y):
        row = 0
        self.movables = []
        for letter in self.rack:
            self.movables.append(MovingLetter(self.root, letter, row*30+x, y+12.5, self.root))
            row += 1
    def exchange(self):
        exchangeWindow = Toplevel(height=self.root.winfo_screenheight(), \
                                  width = self.root.winfo_screenwidth())
        exchangeWindow.wm_title("Exchange")

        label = Label(exchangeWindow, text="Enter the letters you want to exchange")
        label.place(x=550, y=230)

        #rackLabelFrame = Frame(
        rackLabels = []
        row = 1
        for letter in self.rack:
            rackLabel = Label(exchangeWindow, text=letter)
            rackLabels.append(label)
            rackLabels[-1].place(x=500+(row*30), y=330)
            row += 1
            
        button = Button(exchangeWindow, text="Done", command=exchangeWindow.destroy)
        button.place(x=550, y=660)
    def getNewWord(self):
##        checkBoard = []
##        #self.displayBoard(self.board)
##        for row in self.board:
##            checkBoard.append(row)
        if self.board[8][8] == "*":
            isFirstTurn = True
        else:
            isFirstTurn = False
        places = []
        rows = []
        columns = []
        word = ""
        
        for movable in self.movables:
            movable.row = movable.hoveringOver.split(",")[0]
            movable.column = movable.hoveringOver.split(",")[1]
        for movable in self.movables:
            if not(movable.row == "NA"):
                movable.row = int(movable.row)
                movable.column = int(movable.column)
                if self.board[movable.row][movable.column][0] != " " and \
                    self.board[movable.row][movable.column] != "*":
                    print("Letters cannot overlap.")
                    self.displayBoard(self.board)
                    for movable in self.movables:
                        movable.returnToOrig()
                    return False
                else:
                    self.board[movable.row][movable.column] = movable.text
                    self.displayBoard(self.board)
                    #self.displayBoard(checkBoard)
                    word += movable.text
       # if self.checkContiguous():
        print(isFirstTurn)
        boardCheck = self.checkWholeBoard(self.board, isFirstTurn)
 #      self.displayBoard(board)
 #       self.displayBoard(self.board)
        if boardCheck[0]:
            for movable in self.movables:
                movable.f.place_forget()
            for letter in word:
                self.rack.remove(letter)
            self.drawTiles()
            self.getMovables(self.x, self.y)
            for movable in self.movables:
                movable.board = self.board
                movable.getPositions()
                movable.returnToOrig()
            self.movables[-1].getBoard()
            #return word
        else:
            print(boardCheck[1]) #self.popup(self.root, "Invalid Word", "Invalid Word\n", self.root.winfo_screenheight(), self.root.winfoscreenwidth())
            for movable in self.movables:
                movable.returnToOrig()
                if movable.row != "NA":
                    row = int(movable.row)
                    column = int(movable.column)
                    if row == 8 and column == 8:
                        self.board[row][column] = "*"
                    else:
                        self.board[row][column] = " "
            #return False
        self.displayBoard(self.board)
 #       self.displayBoard(self.lastBoard)
##        else:
##            print("INVALID WORD")
##            self._undo(self.lastBoard)
##            for movable in self.movables:
##                movable.returnToOrig()
        
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
            letter = random.choice(distribution)
            distribution.remove(letter)
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

    def checkWholeBoard(self, boardToCheck, isFirstTurn):
        touchingList = []
        for row in range(1, 16):
            for column in range(1, 16):
                attributes = self.getAttributes("%d,%d" % (row, column), boardToCheck)
                if attributes['text'][0] != " ":
                    touchingList.append(attributes)
        touchingList = self.removeDuplicates(touchingList)
        for item in touchingList:
            if item['numTouchingLetters'] == 0:
                return False, "Must Be Connected2"
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
        for word in words:
            print(word)
            letters = words[word]
            numOnes = 0
            numTwos = 0
            numGreater = 0
            length = len(word)
            #print(words)
            if length > 2:
                for letter in letters:
##                    if letter['numTouchingLetters'] >2:
##                        numTwos += 1
## #                       numGreater += 1
##                    elif letter['numTouchingLetters'] == 2:
##                        numTwos += 1
                    if letter['numTouchingLetters'] >= 2:
                        numTwos += 1
                if numTwos < (len(word) - 2):
                    return False, "Must Be Connected"
##                if not isFirstTurn:
##                    if numGreater < 1:
##                        return False, "Must Be Connected"
            else:
                for letter in letters:
##                    if letter['numTouchingLetters'] > 1:
##                        numGreater += 1
##                        numOnes += 1
##                    elif letter['numTouchingLetters'] == 1:
##                        numOnes += 1
                    if letter['numTouchingLetters'] >= 2:
                        numOnes += 1
                if numOnes < 1:
                    return False, "Must Be Connected"
##                if not isFirstTurn:
##                    if numGreater < 1:
##                        return False, "Must Be Connected"
        incorrectWords = []
        if len(words) < 1:
            return False
        else:
            for word in words:
                if not(self.checkWord(word.lower())):
                    incorrectWords.append(word)
        

        if incorrectWords:
            return False, words, incorrectWords.keys()
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
            #print(up)
            touching['up'] = up
            if up[0].isalpha():
                numTouching += 1

        else:
            touching['up'] = 'NA'
            
        if not row+1>15:
            down = boardToCheck[row+1][column]
            #print(down)
            touching['down'] = down
            if down[0].isalpha():
                numTouching += 1

        else:
            touching['down'] = 'NA'

        if not column+1 > 15:
            right = boardToCheck[row][column+1]
            #print(right)
            touching['right'] = right
            if right[0].isalpha():
                numTouching += 1
        else:
            touching['right'] = 'NA'

        if not column-1 < 1:
            left = boardToCheck[row][column-1]
            #print(left)
            touching['left'] = left
            if left[0].isalpha():
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
def popup(root, text):
    length = len(text)
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    
from tkinter import *
import random
distribution = ["a", "a", "a", "a", "a", "a", "a", "a", "a", \
                        "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", \
                        "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", \
                        "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", \
                        "i", "i", "i", "i", "i", "j", "k", "l", "l", "l", \
                        "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", \
                        "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", \
                        "r", "r", "r", "r", "r", "r", "s", "s", "s", "s", \
                        "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", \
                        "v", "v", "w", "w", "x", "y", "y", "z"]
player1 = Player(1, 's', 150, 550)
player1.startTurn()
player1.root.mainloop()
