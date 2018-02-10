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
    def __init__(self, root, playerNumber, name, x, y, mode1, mode2):
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

        self.mode1 = mode1
        self.mode2 = mode2
        
        self.overRoot = root
##        #self.overRoot.withdraw()
        
        self.root = root
    def reRoot(self, root):
        self.root.deiconify()
        self.overRoot.deiconify()
    def startTurn(self):
        self.switchTurn = 0
        
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

        self.screenHeight = self.root.winfo_screenheight()
        self.screenWidth = self.root.winfo_screenwidth()

        self.root.mainloop()
        
    def getMovables(self, x, y):
        row = 0
        self.movables = []
        for letter in self.rack:
            self.movables.append(MovingLetter(self.root, letter, row*30+x, y+12.5, self.root))
            row += 1
            
    def exchange(self):
        self.root.update_idletasks()
        
        self.exchangeWindow = Toplevel(self.root, height=self.screenHeight, \
                                  width = self.screenWidth)
        self.exchangeWindow.wm_title("Exchange")

        label = Label(self.exchangeWindow, text="Enter the letters you want to exchange", relief=RAISED)
        label.place(x=450, y=130, height=50, width=250)

        rackLabelFrame = Frame(self.exchangeWindow, relief=RAISED)
        rackLabelFrame.place(x=450, y=330, height=100, width=250)
        rackLabels = []
        column = 1
        for letter in self.rack:
            rackLabel = Label(rackLabelFrame, text=letter)
            rackLabels.append(rackLabel)
            rackLabels[-1].grid(row=1, column=column)
            column += 1
            
        button = Button(self.exchangeWindow, text="Back", command=self.exchangeWindow.destroy)
        button.place(x=500, y=360)
        
        self.exchangeString = Entry(self.exchangeWindow)
        self.exchangeString.place(x=450, y=230, height=20, width=100)
        self.exchangeString.focus_set()
        #self.exchangeString.bind("<Return>", self.getNewTiles)

        exchangeButton = Button(self.exchangeWindow, text="Enter", command=self.getNewTiles)
        exchangeButton.place(x=550, y=230)
        
    def getNewTiles(self, *event):
        letters = self.exchangeString.get()
        print(letters)
        for letter in letters:
            if letter in self.rack:
                self.rack.remove(letter)
        for movable in self.movables:
            movable.f.place_forget()
        self.drawTiles()
        self.getMovables(self.x, self.y)
        for movable in self.movables:
            movable.board = self.board
            movable.getPositions()
            movable.returnToOrig()
        self.movables[-1].getBoard()
        self.exchangeWindow.destroy()
        self.endTurn()
        
    def getNewWord(self):
        print(self.switchTurn)
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
        direction = ""
        for movable in self.movables:
            movable.row = movable.hoveringOver.split(",")[0]
            movable.column = movable.hoveringOver.split(",")[1]
            rows.append(movable.row)
            columns.append(movable.column)
        startRow = int(min(list(row for row in rows if row != "NA")))
        startColumn = int(min(list(column for column in columns if column != "NA")))
        for movable in self.movables:
            if movable.row != "NA":
                if int(movable.row) == startRow + 1:
                    direction = "D"
                    break
                elif int(movable.column) == startColumn + 1:
                    direction = "A"
                    break
            
        for movable in self.movables:
            if not(movable.row == "NA"):
                movable.row = int(movable.row)
                movable.column = int(movable.column)
                if self.board[movable.row][movable.column][0] != " " and \
                    self.board[movable.row][movable.column] != "*":
                    print("Letters cannot overlap.")
                    popup(self.root, "Letters Cannot Overlap", "Letters Cannot Overlap\n\n\n", \
                          self.screenHeight, self.screenWidth)
                    self.displayBoard(self.board)
                    for movable in self.movables:
                        movable.returnToOrig()
                        if movable.row != "NA":
                            row = int(movable.row)
                            column = int(movable.column)
                            if row == 8 and column == 8:
                                self.board[row][column] = "*"
                            else:
                                self.board[row][column] = " "
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
            self.getScore(direction)
            for movable in self.movables:
                movable.f.place_forget()
            for letter in word:
                self.rack.remove(letter)
            self.drawTiles()
##            self.getMovables(self.x, self.y)
##            for movable in self.movables:
##                movable.board = self.board
##                movable.getPositions()
##                movable.returnToOrig()
##            self.movables[-1].getBoard()
            self.movables[-1].boardFrame.destroy()
            self.endTurn()
            #return word
        else:
            print(boardCheck[1])
            if boardCheck[1] == "Invalid Word":
                text = ""
                for invalidWord in boardCheck[1]:
                    text += invalidWord
                    text += "\n"
                popup(self.root, "Invalid Word", text, self.screenHeight, self.screenWidth)
            else:
                popup(self.root, "Invalid Word", "Invalid Word", self.screenHeight, self.screenWidth)
                
            for movable in self.movables:
                movable.returnToOrig()
                if movable.row != "NA":
                    row = int(movable.row)
                    column = int(movable.column)
                    if row == 8 and column == 8:
                        self.board[row][column] = "*"
                    else:
                        self.board[row][column] = " "
                        
            if self.mode1 == "h" or self.mode1 == "H":
                self.endTurn()
            
        print(direction, self.score)
        
    def endTurn(self):
        #self.overRoot.withdraw()
        #self.root.destroy()
        self.root.quit()
        self.root.withdraw()
        self.overRoot.quit()
        self.overRoot.withdraw()
        self.switchTurn = 1

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

    def getScore(self, direction):
##        self.lastWordScore = 0
##        for letter in word:
##            self.lastWordScore += scores[letter]
##        self.score += self.lastWordScore
        lettersToScore = []
        for movable in self.movables:
            if movable.row != "NA":
               lettersToScore.append(movable.text)
            
        for movable in self.movables:
            if movable.row != "NA":
                touching = self.getAttributes("%d,%d" % (movable.row, movable.column), self.board)
                if direction == "A":
                    lettersToScore.append(touching['up'])
                    lettersToScore.append(touching['down'])
                elif direction == "D":
                    lettersToScore.append(touching['right'])
                    lettersToScore.append(touching['left'])
        for letter in lettersToScore:
            if letter[0] != " " and letter != "NA":
                self.score += self.scores[letter.lower()]
        print(lettersToScore)
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
        if isFirstTurn and boardToCheck[8][8][0] != "*":
            pass
        else:
            if isFirstTurn and boardToCheck[8][8][0] == "*":
                return False, "Must Touch Star"
            else:
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
                        if numOnes < 1 and not(isFirstTurn):
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
            return False, words, incorrectWords
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
            
def popup(root, header, text, windowHeight, windowWidth):
    global popupClosed, window
    popupClosed = 0
    window = Toplevel(root, height=windowHeight, width=windowWidth)
    window.wm_title(header)

    label = Label(window, text=text, relief = SUNKEN)
    label.place(x=(windowWidth//2)-250, y=(windowHeight//2)-250, \
                height = 500, width = 500)


    button = Button(window, text="Close", command=destroyPopup)
    button.place(x=0, y=0)
def destroyPopup():
    window.destroy()
    popupClosed = 1
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
class Game():
    def __init__(self):
         self.root = Tk()
         self.root2 = Tk()
         self.root3 = Tk()
         self.root3.withdraw()
         self.main()
         
    def startGame(self):
        name1 = input("Enter the First Player's Name: ")
        name2 = input("Enter the Second Player's Name: ")

        validMode1Inputs = ['n', 'h', 'N', 'H']
        validMode2Inputs = ['n', 's', 'N', 'S']
        mode1Flag = False
        mode2Flag = False
        while not mode1Flag:
            self.mode1 = input("Normal (wrong word -> continue) or Hardcore (wrong word -> lose turn)?(n/h) ")
            if self.mode1 in validMode1Inputs:
                mode1Flag = True
            else:
                print("Invalid")

        while not mode2Flag:
            self.mode2 = input("Normal (play until no tiles left) or Short (up to 125 points)? (n/s) ")
            if self.mode2 in validMode2Inputs:
                mode2Flag = True
            else:
                print("Invalid")
                      
        self.player1 = Player(self.root, 1, name1, 150, 550, self.mode1, self.mode2)
        self.player2 = Player(self.root2, 2, name2, 150, 550, self.mode1, self.mode2)

        self.playerGoing = 1
        self.scoreRoot = Tk()
        self.scoreWindow = Toplevel(self.scoreRoot)
        self.scoreWindow.wm_title("Scoreboard")
        self.scoreRoot.withdraw()
        self.scoreWindow.resizable(0,0)
        self.scoreWindow.geometry("%dx%d%+d%+d"%(200, 100, 700, 0))
        self.player1ScoreLabel = Label(self.scoreWindow, text="%s's Score: %d" % (self.player1.name, self.player1.score), height=1, width=20, relief=SUNKEN)
        self.player2ScoreLabel = Label(self.scoreWindow, text="%s's Score: %d" % (self.player2.name, self.player2.score), height=1, width=20, relief=SUNKEN)
        self.player1ScoreLabel.grid(row=1, column=1)
        self.player2ScoreLabel.grid(row=2, column=1)
        
    def updateScores(self):
        self.scoreRoot = Tk()
        self.scoreWindow = Toplevel(self.scoreRoot)
        self.scoreWindow.wm_title("Scoreboard")
        self.scoreRoot.withdraw()
        self.scoreWindow.resizable(0,0)
        self.scoreWindow.geometry("%dx%d%+d%+d"%(200, 100, 700, 0))
        self.player1ScoreLabel = Label(self.scoreWindow, text="%s's Score: %d" % (self.player1.name, self.player1.score), height=1, width=20, relief=SUNKEN)
        self.player2ScoreLabel = Label(self.scoreWindow, text="%s's Score: %d" % (self.player2.name, self.player2.score), height=1, width=20, relief=SUNKEN)
        self.player1ScoreLabel.grid(row=1, column=1)
        self.player2ScoreLabel.grid(row=2, column=1)
        
    def doTurn(self):
        if self.playerGoing == 1:
            self.root1 = Tk()
            self.player1.reRoot(self.root1)
            self.player1.startTurn()
            while self.player1.switchTurn != 1:
                pass

            self.player2.getMovables(self.player2.x, self.player2.y)
            for movable in self.player2.movables:
                movable.board = self.player1.board
            self.player2.board = self.player1.board
            self.playerGoing = 2
            popup(self.root3, "Pass Device", "Pass Device to %s\n\n" % self.player2.name, self.player1.screenHeight, self.player1.screenWidth)
        else:
            self.root2 = Tk()
            self.player2.reRoot(self.root2)
            self.player2.startTurn()
            while self.player2.switchTurn != 1:
                pass

            for movable in self.player1.movables:
                movable.board = self.player2.board
            self.player1.board = self.player2.board
            self.playerGoing = 1
            popup(self.root3, "Pass Device", "Pass Device to %s\n\n" % self.player1.name, self.player2.screenHeight, self.player2.screenWidth)
    def main(self):
        self.startGame()
        if self.mode2.lower() == "n":
            while distribution and (self.player1.rack or self.player2.rack):
                self.doTurn()
                self.updateScores()
        else:
            while self.player1.score < 75 or self.player2.score < 75:
                self.doTurn()
                self.updateScores()
                
from tkinter import *
import random

scrabble = Game()


