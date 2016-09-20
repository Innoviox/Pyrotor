import tiles
import functions as func

class Player():
    def __init__(self, root, playerNum, name, x, y, mode1, mode2, rack, distribution):
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

        self.root = root
        if distribution != ():
           self.distribution = distribution
        else:
            self.distribution = False
        #OSPD stands for official scrabble player's dictionary
        #self.ospd = open("dict.txt").read().split() #taken from http://www.puzzlers.org/pub/wordlists/ospd.txt #/Volumes/PYTHONDISK/
        try:
            ospd = open("newDict.txt").read().split("\n") #taken from https://raw.githubusercontent.com/xjtian/PyScrabble/master/wordlists/OSPD4_stripped.txt
            self.ospd = []
            for word in ospd:
                self.ospd.append(word.strip())
        except:
            func.popup(self.root, "Dictionary File Not Found", "Dictionary File Not Found\n\n\n", 500, 500)
            end()
        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10, "?" : 0}
        
        self.scoreList = ['TWS', 'DWS', 'TLS', 'DLS']
        self.score = 0
        self.playerNum = playerNum
        self.name = name
        
        self.rack = rack
        self.drawTiles()
        
        self.x = x
        self.y = y

        self.mode1 = mode1
        self.mode2 = mode2
        
        #self.overRoot = root
               
    def reRoot(self, root):
        self.root = root
        self.root.withdraw()
        #self.root.deifonify()
        #self.overRoot.deiconify()
        pass
    
    def placeButtons(self):
        self.shuffleButton = func.Button(self.root, text = "Shuffle", command = self.shuffleRack)
        self.shuffleButton.place(x=self.x-50, y=self.y+100)
        
        self.enterButton = func.Button(self.root, text = "Enter Word", command = self.getNewWord)
        self.enterButton.place(x=self.x+150, y=self.y+100)
        
        self.returnButton = func.Button(self.root, text = "Return", command = self.returnMovables)
        self.returnButton.place(x=self.x+250, y=self.y+100)

        self.exchangeButton = func.Button(self.root, text = "Exchange", command= self.exchange)
        self.exchangeButton.place(x = self.x+50, y=self.y+100)
        
    def hideButtons(self):
        self.shuffleButton.place_forget()
        self.enterButton.place_forget()
        self.returnButton.place_forget()
        self.exchangeButton.place_forget()
        
    def startTurn(self, otherName, otherScore):
        self.drawTiles()
        self.switchTurn = 0

        self.root.deiconify()
        self.root.title("%s's Turn" % self.name)
        self.root.resizable(0,0)
        self.root.geometry("%dx%d%+d%+d"%(675, 700, 0, 0))
        self.root.config(bg=func.generateRandomColor())
#        self.root.config(
        self.rackFrame = func.Frame(self.root, bd=1, relief=func.RAISED)
        self.rackFrame.place(x=self.x, y=self.y+25, width=300, height=50)


        self.getMovables(self.x+50, self.y+25)
        for movable in self.movables:
            movable.board = self.board

        self.coverUp = func.Button(self.root, text="Click to see tiles", command=self.showTiles)
        self.coverUp.place(x=self.x, y=self.y+25, width=300, height=50)
        self.coverUp.lift()
        
        self.rackFrame.lower()
        self.movables[-1].getBoard()

        self.placeButtons()

        self.screenHeight = self.root.winfo_screenheight()
        self.screenWidth = self.root.winfo_screenwidth()

        self.getScoreBoard(otherName, otherScore)

        
        self.root.mainloop()

    def showTiles(self):
        self.coverUp.place_forget()
        
    def getScoreBoard(self, otherName, otherScore):
        
        self.player1ScoreLabel = func.Label(self.root, text="%s's Score: %d" % (self.name, self.score), height=1, width=15, relief=func.SUNKEN, justify=func.LEFT, anchor=func.W)
        self.player2ScoreLabel = func.Label(self.root, text="%s's Score: %d" % (otherName, otherScore), height=1, width=15, relief=func.SUNKEN, justify=func.LEFT, anchor=func.W)
        if self.distribution:
            self.tilesLabel = func.Label(self.root, text = "%d tiles left" % len(self.distribution), height = 1, width = 15, relief=func.SUNKEN)
        else:
            self.tilesLabel = func.Label(self.root, text = "%d tiles left" % len(func.distribution), height = 1, width = 15, relief=func.SUNKEN)
        if self.playerNum == 1:
            self.player1ScoreLabel.place(x=500, y=550)
            self.player2ScoreLabel.place(x=500, y=570)
            self.scoreX, self.scoreY = 500, 550
        else:
            self.player1ScoreLabel.place(x=500, y=550)
            self.player2ScoreLabel.place(x=500, y=570)
            self.scoreX, self.scoreY = 500, 570
        self.tilesLabel.place(x=500, y=590)
        
    def updateSelfScore(self):
        
        self.player1ScoreLabel.config(text = "%s's Score: %d" % (self.name, self.score))
        
    def scoreAnimation(self, scoreLabel, startX, startY):
        
        frame = func.Frame(self.root, relief=func.RAISED)
        frame.place(x=startX, y=startY, height = 25, width = 25)
        label = func.Label(frame, text = "+" + str(scoreLabel), bd=1, relief=func.RAISED, height = 25, width = 25)
        label.pack()

        frame.lift()
        
        fontsize = 12
        for i in range(1, 15, 1):
            self.player1ScoreLabel.config(height=round(i/10), width=round(15*(i/10)), font=("Courier", fontsize+(round((i/10)*3))))
            self.player1ScoreLabel.place_configure(x=self.scoreX-round((i/10)*25), y=self.scoreY-round((i/10)*25))
            self.player1ScoreLabel.lift()
            self.player1ScoreLabel.update()
            
            
        for scoreChange in range(scoreLabel):
            self.player1ScoreLabel.config(text = "%s's Score: %d" % (self.name, self.score + scoreChange + 1))
            self.player1ScoreLabel.update()
            func.sleep(0.05)
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
            self.movables.append(tiles.MovingLetter(self.root, letter, row*30+x, y+12.5, self.root))
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
        
        self.exchangeWindow = func.Toplevel(self.root, height=self.screenHeight/2, \
                                  width = self.screenWidth/2-200)
        self.exchangeWindow.wm_title("Exchange")

        label = func.Label(self.exchangeWindow, text="Drag the letters you wish to exchange to the rack.", relief=func.RAISED)
        label.place(x=90, y=30, height=50, width=320)

        self.exchangeLetters = []
        for letterCount in range(len(self.rack)):
            self.exchangeLetters.append(tiles.MovingExchangeLetter(self.exchangeWindow, self.rack[letterCount], letterCount*30+150, 300, self.exchangeWindow))
        for i in self.exchangeLetters:
            i.els = self.exchangeLetters
            i.weed_els()
        self.exchangeLetters[-1].getExchangeRack()
            
        button = func.Button(self.exchangeWindow, text="Back", command=self.exchangeWindow.destroy)
        button.place(x=250, y=175)

        exchangeButton = func.Button(self.exchangeWindow, text="Enter", command=self.getNewTiles)
        exchangeButton.place(x=175, y=175)
        
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
            #self.drawTiles()
            self.getMovables(self.x+50, self.y+25)
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
                        func.popup(self.root, "Letters Cannot Overlap", "Letters Cannot Overlap\n\n\n", \
                              self.screenHeight, self.screenWidth)
                        self.resetBoard()
                        self.enterButton.place(x=self.x+150, y=self.y+100)
                        return False
                else:
                    if self.board[movable.row][movable.column][0] == "*":
                        self.addKey(specialScores, "DWS", "")
                    self.board[movable.row][movable.column] = movable.text #Place the letter
                    
        return word, specialScores
    def getNewWord(self):
        for movable in self.movables:
            movable.snapToGrid()
            movable.frame.update()
            
        self.hideButtons()
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
                self.placeButtons()
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
                            func.popup(self.root, "Bingo!!!", "Bingo!!!\n\n\nYou used all your tiles!\n\n\n+50 points!", \
                                  self.screenHeight, self.screenWidth)
                            #self.score += 50
                            self.scoreAnimation(50, 245, 245, self.scoreX, self.scoreY, 50, 100)
                            self.score += 50
                            
                        for movable in self.movables:
                            movable.frame.place_forget()
                        for letter in word:
                            self.rack.remove(letter)
                        #self.drawTiles()
                        #self.movables[-1].boardFrame.destroy()
                        self.endTurn()
                    else:
                        if boardCheck[1] == "Invalid Word":
                            text = "Invalid Words: \n\n"
                            for invalidWord in boardCheck[2]:
                                text += invalidWord
                                text += "\n"
                            
                            self.resetBoard()
                            if self.mode1 == "h" or self.mode1 == "H":
                                #while func.popupClosed == 0: pass
                                text += "\n\n\nPass Device to " + self.otherName
                                func.popup(self.root, "Invalid Word", text, 500, 500)
                                self.endTurn()

                            else:
                                func.popup(self.root, "Invalid Word", text, 500, 500)
                        else:
                            func.popup(self.root, boardCheck[1], boardCheck[1], 500, 500)
                        self.placeButtons()
                        #self.resetBoard()
                        return False
                else:
                    self.resetBoard()
                    self.placeButtons()
                    return False
        else:
            func.popup(self.root, "No tiles played", "No tiles played\n\n\n", 500, 500)
            self.placeButtons()
            
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
                        #popup(self.root, 'a', 'a', 50, 50)
                        pass
                    
            sharedWord = self.getMode(sharedWords)
            movablesInWord = 0
            for movable in self.movables:
                if sharedWord[0] in movable.words:
                    movablesInWord += 1
                #print(sharedWord, movable.words)
            otherwords = []
            for movable in self.movables:
                for word in movable.words:
                    if word != sharedWord[0]:
                        otherwords.append(word)
                #print(otherwords, movable.words, sharedWord[0])

            for word in otherwords:
                if otherwords.count(word) > 1:
                    func.popup(self.root, "Same Word", "All movables must be in the same word\n\n\n", \
                          500, 500)
                    
                    return False
            if movablesInWord < sharedWord[1][0]:
                func.popup(self.root, "Same Word", "All movables must be in the same word\n\n\n", \
                      500, 500)
                
                return False
            
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
                     movable.hoveringOver == "3,3" or movable.hoveringOver == "3,13" or \
                     movable.hoveringOver == "4,4" or movable.hoveringOver == "4,12" or \
                     movable.hoveringOver == "5,5" or movable.hoveringOver == "5,11" or \
                     movable.hoveringOver == "11,5" or movable.hoveringOver == "11,11" or \
                     movable.hoveringOver == "12,4" or movable.hoveringOver == "12,12" or \
                     movable.hoveringOver == "13,3" or movable.hoveringOver == "13,13":
                    self.board[int(movable.row)][int(movable.column)] = "DWS"
                elif movable.hoveringOver == "2,6" or movable.hoveringOver == "2,11" or \
                     movable.hoveringOver == "6,2" or movable.hoveringOver == "6,6" or \
                     movable.hoveringOver == "6,10" or movable.hoveringOver == "6,14" or \
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

                #movable.returnToOrig()
                
    def addKey(self, dictToCheck, key, value):
        """Check if the key already exists. If it does, add the value, otherwise create one with the value.
           Note: this algorithm assumes all keys in the dictionary are lists."""
        if dictToCheck.get(key):
            dictToCheck[key].append(value)
        else:
            dictToCheck[key] = [value]
            
    def endTurn(self):
        """End the turn by quitting the root."""
        #for movable in self.movables:
        self.root.quit()

        self.root.destroy()
       
        #self.overRoot.quit()
        #self.overRoot.withdraw()
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
        self.scoreAnimation(wordScore, lastX, lastY, self.scoreX, self.scoreY, 50, 100)
        
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
                if specialScores.get("DWS"):
                    for i in range(2):
                        for letter in scoreLetters:
                            wordScore += self.scores[letter.lower()]
                elif specialScores.get("TWS"):
                    for i in range(3):
                        for letter in scoreLetters:
                            wordScore += self.scores[letter.lower()]
                else:
                    for letter in scoreLetters:
                        wordScore += self.scores[letter.lower()]
            elif scoreType == "TLS":
                if specialScores.get("DWS"):
                    for i in range(2):
                        for count in range(2):
                            for letter in scoreLetters:
                                wordScore += self.scores[letter.lower()]
                else:
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
                if movable.row * 31 + 50> lastY:
                    lastY = movable.row * 31 + 50
                if movable.column * 31 + 50> lastX:
                    lastX = movable.column * 31 + 50

        self.scoreAnimation(wordScore, lastX, lastY)
        
        self.score += wordScore

        self.updateSelfScore()
        
    def drawTiles(self):
        if self.distribution:
            if len(self.rack) < 7:
                while len(self.rack) < 7 and len(self.distribution) > 0:
                    letter = func.choice(self.distribution)
                    self.distribution.remove(letter)
                    self.rack.append(letter.upper())
        else:
             if len(self.rack) < 7:
                while len(self.rack) < 7 and len(func.distribution) > 0:
                    letter = func.choice(func.distribution)
                    func.distribution.remove(letter)
                    self.rack.append(letter.upper()) 
            
    def checkWord(self, word):
        #print(word, word.upper(), word.lower())
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
            try:
                up = boardToCheck[row-1][column]
            except:
                up = " "
            touching['up'] = up
            if up.upper() in func.ascii_uppercase:
                numTouching += 1

        else:
            touching['up'] = 'NA'
            
        if not row+1>15:
            try:
                down = boardToCheck[row+1][column]
            except:
                down = " "
            touching['down'] = down
            if down.upper() in func.ascii_uppercase:
                numTouching += 1

        else:
            touching['down'] = 'NA'

        if not column+1 > 15:
            try:
                right = boardToCheck[row][column+1]
            except:
                right = " "
            touching['right'] = right
            if right.upper() in func.ascii_uppercase:
                numTouching += 1
        else:
            touching['right'] = 'NA'

        if not column-1 < 1:
            try:
                left = boardToCheck[row][column-1]
            except:
                pass
            touching['left'] = left
            if left.upper() in func.ascii_uppercase:
                numTouching += 1
        else:
            touching['left'] = 'NA'
            

        touching['numTouchingLetters'] = numTouching
        touching['row'] = row
        touching['column'] = column
        touching['text'] = boardToCheck[row][column]
        return touching
    
    def checkWord(self, word):
        if word.upper() in self.ospd or word.lower() in self.ospd:
            return True
        else:
            return False
        
    def returnMovables(self):
        for movable in self.movables:
            movable.returnToOrig()
            
    def shuffleRack(self):
        
        func.shuffle(self.rack)
        for movable in self.movables:
            movable.frame.destroy()
        self.getMovables(self.x+50, self.y+25)


