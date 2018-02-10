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

        self.label = Label(self.frame, bd=1, relief=RAISED, text=text, width=25)
        self.label.pack(fill=X, padx=1, pady=1)

        self.label.bind('<ButtonPress-1>', self.startMoveWindow)
        self.label.bind('<B1-Motion>', self.MoveWindow)
        self.frame.bind('<ButtonPress-1>', self.startMoveWindow)
        self.frame.bind('<B1-Motion>', self.MoveWindow)
        
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
        self.lastX, self.lastY = event.x_root, event.y_root
        self.frame.place_configure(x=self.x, y=self.y)

        f1Position = (self.x, self.y)
        for labelPosition in self.labels_positionList.keys():
            if self.isTouching(f1Position, labelPosition,
                               self.frame.winfo_width(), self.frame.winfo_height(),
                               25, 25):
                self.frame.place_configure(x=labelPosition[0], y=labelPosition[1])
                self.hoveringOver = "%d,%d" % (self.labels_positionList[(labelPosition[0], labelPosition[1])][0],
                                               self.labels_positionList[(labelPosition[0], labelPosition[1])][1])

                if self.text == "?" and self.blankChosen != 1:
                    self.chooseBlank()


        self.checkForReturn()
        self.frame.lift()
        
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
        
    def checkForReturn(self, *event):
        f1Position = (self.x, self.y)
        if not(self.isTouching(f1Position, (self.boardX, self.boardY),
                          self.frame.winfo_width(), self.frame.winfo_height(),
                          self.boardWidth, self.boardHeight)):
            self.frame.place_configure(x=self.origX, y=self.origY)
            self.hoveringOver = "NA,NA"
##            if self.origText == "?":
##                self.blankChosen = 0
##                self.setBlank("?")
            
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
        extraList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
                     "TWS", "DWS", "TLS", "DLS", \
                     "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ", \
                     "*", " "]
        self.boardFrame = Frame(self.root, bd=1, relief=SUNKEN)
        self.boardFrame.place(x=0, y=0, width=497, height = 497)
        labels = list()
        squares = list()

        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                if label in extraList:
                    entry = Frame(self.boardFrame, bd=1, relief=RAISED)
                    entry.place(x=(i*31), y=(j*31), width=31, height=31)
                    labels.append(Label(entry, text = label,
                                        height = 31, width = 31))
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
            #buttons[-1].grid(row = row, column = column)
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
    
class Player():
    def __init__(self, root, playerNumber, name, x, y, mode1, mode2):
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

        
        self.ospd = open("dict.txt").read().split() #taken from http://www.puzzlers.org/pub/wordlists/ospd.txt


        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10, "?" : 0}
        
        self.scoreList = ['TWS', 'DWS', 'TLS', 'DLS']
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
        self.player1ScoreLabel.place(x=500, y=0)
        self.player2ScoreLabel.place(x=500, y=20)
        self.tilesLabel.place(x=500, y=40)
        
    def updateSelfScore(self):
        self.player1ScoreLabel.config(text = "%s's Score: %d" % (self.name, self.score))
        
    def scoreAnimation(self, scoreLabel, startX, startY, endX, endY, endWidth, endHeight, travelTime = .1, changesPerSecond = 50):
        frame = Frame(self.root, relief=RAISED)
        frame.place(x=startX, y=startY, height = 25, width = 25)
        label = Label(frame, text = "+" + str(scoreLabel), bd=1, relief=RAISED, height = 25, width = 25)
        label.pack()

        frame.lift()

        newX = startX
        newY = startY

##        changeNum = travelTime * changesPerSecond
##        changeSpeed = travelTime / changesPerSecond
##        if startX > endX:
##            xChange = round((startX - endX) / changeNum)
##        else:
##            xChange = round((endX - startX) / changeNum)
##
##        if startY > endY:
##            yChange = round((endY - startY) / changeNum)
##        else:
##            yChange = round((startY - endY) / changeNum)
##            
##        print(changeNum, changeSpeed, startX, startY, endX, endY, xChange, yChange)
##        
##        for change in range(changeNum):
####            for changeCount in range(xChange):
####                if xChange > 0:
####                    newX += 1
####                elif xChange < 0:
####                    newX -= 1
####                frame.place_configure(x=newX, y=newY)
####                frame.update()
####            for changeCount in range(yChange):
####                if yChange > 0:
####                    newY += 1
####                elif YChange < 0:
####                    newY -= 1
####                frame.place_configure(x=newX, y=newY)
####                frame.update()                
##            newX += xChange
##            newY += yChange
##            frame.place_configure(x=newX, y=newY)
##            time.sleep(changeSpeed)   
##            frame.lift()
##            frame.update()
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
##        while not(self.movables[-1].isTouching((newX, newY), \
##                                               (endX, endY), \
##                                               25, 25, endWidth, endHeight)):
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
            #time.sleep(0.005)   
            frame.lift()
            frame.update()
        #time.sleep(1)
        frame.destroy()
        label.destroy()
        #frame.quit()
        #label.quit()

    def isTouchingScoreboard(self, x, y):
        if x > 474 and y < 26:
            return True
        else:
            return False
        
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

        exchangeButton = Button(self.exchangeWindow, text="Enter", command=self.getNewTiles)
        exchangeButton.place(x=550, y=230)
        
    def getNewTiles(self, *event):
        letters = list(self.exchangeString.get())
        lettersNotInRack = []
        for letter in letters:
            if letter in self.rack:
                self.rack.remove(letter)
            else:
                lettersNotInRack.append(letter)
        if lettersNotInRack:
            text = ""
            for letter in lettersNotInRack:
                text += letter
                text += " "
            popup(self.root, "Letters Not In Rack", "Exchange Error: \n\n\nLetters Not In rack: %s\n" % text, self.screenHeight, self.screenWidth)
        else:
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
        
    def getNewWord(self):
        #self.scoreAnimation(50, 245, 245, 500, 0, 50, 100)
        if self.board[8][8] == "*":
            isFirstTurn = True
        else:
            isFirstTurn = False
        places = []
        self.rows = []
        self.columns = []
        specialScores = {}
        word = ""
        for movable in self.movables:
            movable.row = movable.hoveringOver.split(",")[0]
            movable.column = movable.hoveringOver.split(",")[1]
            if movable.row != "NA":
                self.rows.append(movable.row)
                self.columns.append(movable.column)

        if self.rows:
            startRow = int(min(list(row for row in self.rows if row != "NA")))
            startColumn = int(min(list(column for column in self.columns if column != "NA")))

            direction = ""
            for movable in self.movables:
                if movable.row != "NA":
                    if int(movable.row) == startRow + 1:
                        if direction == "A":
                            return False
                        else:
                            direction = "D"
                    elif int(movable.column) == startColumn + 1:
                        if direction == "D":
                            return False
                        else:
                            direction = "A"
                            
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
                        if self.board[movable.row][movable.column][0] == "*":
                            self.addKey(specialScores, "DWS", "")
                        self.board[movable.row][movable.column] = movable.text #Place the letter
            boardCheck = self.checkWholeBoard(self.board, isFirstTurn)
            if boardCheck[0]:
                self.getScore(specialScores)
                if len(word) == 7:
                    popup(self.root, "Bingo!!!", "Bingo!!!\n\n\nYou used all your tiles!\n\n\n+50 points!", self.screenHeight, self.screenWidth)
                    self.score += 50
                    self.scoreAnimation(50, 245, 245, 500, 0, 50, 100)
            
                for movable in self.movables:
                    movable.frame.place_forget()
                for letter in word:
                    self.rack.remove(letter)
                self.drawTiles()
                self.movables[-1].boardFrame.destroy()
                self.endTurn()
            else:
                if boardCheck[1] == "Invalid Word":
                    text = "Invalid Words: \n\n"
                    for invalidWord in boardCheck[2]:
                        text += invalidWord
                        text += "\n"
                    popup(self.root, "Invalid Word", text, self.screenHeight, self.screenWidth)
                    if self.mode1 == "h" or self.mode1 == "H":
                        self.endTurn()
                else:
                    popup(self.root, boardCheck[1], boardCheck[1], self.screenHeight, self.screenWidth)
                    
                for movable in self.movables:
                    movable.returnToOrig()
                    if movable.row != "NA":
                        row = int(movable.row)
                        column = int(movable.column)
                        if row == 8 and column == 8:
                            self.board[row][column] = "*"
                        else:
                            self.board[row][column] = " "
                        
        else:
            popup(self.root, "No tiles played", "No tiles played\n\n\n", self.screenHeight, self.screenWidth)
            
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
          oldList = newList
          return newList

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
                "b", "b", \
                "c", "c", \
                "d", "d", "d", "d", \
                "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", \
                "f", "f", \
                "g", "g", "g", \
                "h", "h", \
                "i", "i", "i", "i", "i", "i", "i", "i", "i", \
                "j", \
                "k", \
                "l", "l", "l", "l", \
                "m", "m", \
                "n", "n", "n", "n", "n", "n", \
                "o", "o", "o", "o", "o", "o", "o", "o", \
                "p", "p", \
                "q", \
                "r", "r", "r", "r", "r", "r",\
                "s", "s", "s", "s", \
                "t", "t", "t", "t", "t", "t", \
                "u", "u", "u", "u", \
                "v", "v", \
                "w", "w", \
                "x", \
                "y", "y", \
                "z", \
                "?", "?"] #"?" is a blank tile, can be any letter.
               # "?", "?", "?", "?", "?", "?", "?", "?","?", "?","?", "?", "?", "?"] #Just for fun :)
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
         
    def startGame(self):
        self.player1 = Player(self.root, 1, self.name1, 150, 550, self.mode1, self.mode2)
        self.player2 = Player(self.root2, 2, self.name2, 150, 550, self.mode1, self.mode2)
        self.playerGoing = 1
        
        self.scoreRoot = Tk()
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
            self.root1 = Tk()
            self.player1.reRoot(self.root1)
            self.player1.startTurn(self.player2.name, self.player2.score)
            self.player2.board = self.player1.board
            self.playerGoing = 2
            popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player2.name, self.player1.screenHeight, self.player1.screenWidth)
        else:
            self.root2 = Tk()
            self.player2.reRoot(self.root2)
            self.player2.startTurn(self.player1.name, self.player1.score)
            self.player1.board = self.player2.board
            self.playerGoing = 1
            popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player1.name, self.player2.screenHeight, self.player2.screenWidth)
            
    def main(self):
        self.startGame()
        if self.mode2.lower() == "n":
            while distribution and (self.player1.rack or self.player2.rack):
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
        
from tkinter import *
import random, string, time
            
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
    
    mode2Label = Label(enterWindow, text = "Enter mode 2 (normal or short):")
    mode2Label.place(x = 50, y = 465, height = 20, width = 200)
    mode2Var = StringVar()
    mode2Var.set("Mode 2")
    mode2 = Entry(enterWindow, textvariable=mode2Var)
    mode2.place(x = 270, y = 465, height = 20, width = 100)

    enterButton = Button(enterWindow, text = "Enter data", command = checkData)
    enterButton.place(x = 100, y = 500)

def check(string, validInputs, popupHeader, popupText):
    if string in validInputs:
        return True
    else:
        popup(root, popupHeader, popupText, root.winfo_screenheight(), root.winfo_screenwidth())
        return False

def checkData():
    global scrabble
    if check(mode1Var.get(), ['n', 'h', 'N', 'H', 'normal', 'hardcore'], "Invalid Mode 1", "Invalid Mode 1"):
        if check(mode2Var.get(), ['n', 's', 'N', 'S', 'normal', 'short'], "Invalid Mode 2", "Invalid Mode 2"):
            enterWindow.destroy()
            popup(root, "Pass Device", "Pass Device to %s\n\n" % name1Var.get(), root.winfo_screenheight(), root.winfo_screenwidth())
            scrabble = Game(name1Var.get(), name2Var.get(), mode1Var.get(), mode2Var.get())
            scrabble.main()
            
def exitGame():
    if played == 1:
        scrabble.root.destroy()
        scrabble.root2.destroy()
        scrabble.mainRoot.destroy()
        
    root.destroy()
    
root = Tk()
root.resizable(0,0)
root.title("Scrabble")
root.geometry("%dx%d%+d%+d" % (250, 200, 0, 0))
welcomeLabel = Label(root, text = "Welcome to Scrabble in Python!")
instructionsButton = Button(root, text = "Instructions", command = instructions)
playButton = Button(root, text = "Play", command = play)
exitButton = Button(root, text = "Exit", command = exitGame)
played = 0
welcomeLabel.place(x = 40, y = 0)
instructionsButton.place(x = 90, y = 50)
playButton.place(x = 110, y = 100)
exitButton.place(x = 112, y = 150)
root.mainloop()
