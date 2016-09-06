import itertools
from scrabble import *
class CPU(Player):
    def __init__(self):
        self.h = 0
        self.extraList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
             "TWS", "DWS", "TLS", "DLS", \
             "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ", \
             "*", " "]
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
        self.score = 0
        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10, "?" : 0}
        
        self.scoreList = ['TWS', 'DWS', 'TLS', 'DLS']
        self.rack = []
        super(CPU, self).drawTiles()
        #OSPD stands for official scrabble player's dictionary
        #taken from http://www.puzzlers.org/pub/wordlists/ospd.txt #/Volumes/PYTHONDISK/
        try:
            ospd = open("newDict.txt").read().split("\n") #taken from https://raw.githubusercontent.com/xjtian/PyScrabble/master/wordlists/OSPD4_stripped.txt
            self.ospd = []
            for word in ospd:
                self.ospd.append(word.strip())
        except:
            popup(self.root, "Dictionary File Not Found", "Dictionary File Not Found\n\n\n", 500, 500)
            end()

            
    def getAllWordsOnRack(self):
        self.getAllCorrectCombinations(self, self.rack, len(self.rack))
        
    def getAllCorrectCombinations(self, iterable, maxDepth):
        allWords = []
        for depth in range(0, maxDepth + 1):
            for word in itertools.permutations(iterable, depth):
                allWords.append("".join(word))

        #print(len(allWords))
        allWords.pop(0)
        correctWords = []
        numcw = 0
        numwc = 0
        curt = time()
        for word in allWords:
            if self.checkWord(word):
                correctWords.append(word)
        #print(time() - curt)
        #return super(CPU, self).removeDuplicates(correctWords)
        return correctWords
    
   # def checkWord(self, word):
     #   super(CPU, self).checkWord(word)
    def checkWord(self, word):
        #print(word, word.upper(), word.lower())
        #print(self.ospdict[word[0]])
        #print(word)
        if len(word) > 1:
            try:
                h = open("resources/" + word[:2] + ".txt").read().split()
            except:
                return False
            if word.upper() in h:
                return True
            return False
        return False
        
        
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
        words = {}
        for letter in self.getAllOpenLetters():
            allWords = self.getAllCorrectCombinations(self.rack+letter["text"], letter["depth"])
            for word in allWords:
                words[word] = "%d,%d" % letter["column"], letter["row"] - list(word).index(letter)
        return words
    
    def getHookableLetters(self):
        pass
    
    def getHookWords(self):
        pass
    
    def getHooks(self, word):
        hooks = {word:{"back":[], "front":[]}, has_hooks:False}
        for letter in string.ascii_uppercase:
            if self.checkWord(letter + word):
                self.addKey(hooks[word]["front"], letter + word)
                hooks[has_hooks] = True
            if self.checkWord(word + letter):
                self.addKey(hooks[word]["back"], word + letter)
                hooks[has_hooks] = True
        return hooks
    
    def addKey(self, dictToCheck, key, value):
        super(CPU, self).addKey(dictToCheck, key, value)
        
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
                if words:
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
                else:
                    return False
        
        incorrectWords = []
        if words and len(words) < 1:
            return False
        else:
            if words:
                for word in words:
                    if not(self.checkWord(word.lower())):
                        incorrectWords.append(word)
            else:
                return False
            
        if incorrectWords:
            return False, "Invalid Word", incorrectWords
        else:
            return True, words
    def getMoves(self):
        allPossibleWords = {}
        for (key, value) in self.getHookWords().items():
            allPossibleWords[key] = value
        for (key, value) in self.getOpenWords().items():
            allPossibleWords[key] = value
        moves = {}
        for (word, startPosition) in allPossibleWords.keys():
            moves[word] = self.getMoveAttributes(word, startPosition)
            
    def getAttributes(self, place, boardToCheck):
        touching = {}
        place = place.split(",")
        row = int(place[0])
        column = int(place[1])
        numTouching = 0
        if not row-1<1:
            up = boardToCheck[row-1][column]
            touching['up'] = up
            if up.upper() not in self.extraList:
                numTouching += 1

        else:
            touching['up'] = 'NA'
            
        if not row+1>15:
            down = boardToCheck[row+1][column]
            touching['down'] = down
            if down.upper() not in self.extraList:
                numTouching += 1

        else:
            touching['down'] = 'NA'

        if not column+1 > 15:
            right = boardToCheck[row][column+1]
            touching['right'] = right
            if right.upper() not in self.extraList:
                numTouching += 1
        else:
            touching['right'] = 'NA'

        if not column-1 < 1:
            left = boardToCheck[row][column-1]
            touching['left'] = left
            if left.upper() not in self.extraList:
                numTouching += 1
        else:
            touching['left'] = 'NA'
            

        touching['numTouchingLetters'] = numTouching
        touching['row'] = row
        touching['column'] = column
        touching['text'] = boardToCheck[row][column]
        return touching
    
    def getBestMove(self):
        moves = self.getMoves()
        bestMove = {"score":0}
        for move in moves:
            if move["score"] > bestMove["score"]:
                bestMove = move
        return bestMove
#5400-12-10.03
#3150-7-5.24
#3150-7-5.72
#2250-5-4.46
#1350-3-2.48
#900-2-1.62
#450-1-0.882
#450-1-1.034
    def playAllWords(self, maxlength = None):
        self.rackonv()
        print("Loading...This step will take approximately 1 second.")
        allMoves = []
        allWords = self.removeDuplicates(self.getAllCorrectCombinations(self.rack, 7))
        #print(self.rack, allWords)
        boards = 0
        possboards = 0
        longwords = []
        currmaxlen = max(len(i) for i in allWords)
        for word in allWords:
            if maxlength is None:
                if len(word) == max(len(i) for i in allWords):
                    possboards += 344
                    longwords.append(word)
            else:
                if len(word) == maxlength:
                    possboards += 344
                    longwords.append(word)
        print("Generating...This step will take approximately", round(possboards * 0.0023, 4), "seconds.")
        #t = time()
        for word in longwords:
                for row in range(1, len(self.board)):
                    for column in range(1, len(self.board[row])):
                        for direction in ["A", "D"]:
                            nbo = self.rNab()
                            if self.placeWord(word, nbo, [row, column], direction):
                                if self.checkWholeBoard(nbo, True)[0]:
                                    qbox = {"word":word, "board":nbo, "place":[row, column], "direction":direction}
                                    allMoves.append(qbox)
                                    self.getScore(qbox)
        
                            #boards += 1
        #print(time()-t)
        #if allMoves is None:
            #self.playAllWords(maxlength = currmaxlen - 1)
        return allMoves

    def takeTurn(self, maxlen = None):
        plays = self.playAllWords(maxlength = maxlen)

        bestplay = {"score":0}
        for play in plays:
            if play["score"] > bestplay["score"]:
                bestplay = play
        if bestplay == {"score":0}:
            print("Something went wrong. Reloading...")
            maxleng = max(len(i) for i in self.getAllCorrectCombinations(self.rack, 7))
            self.takeTurn(maxlen = maxleng - 1)
        else:
            self.displayBoard(bestplay["board"])
            print("Word:", bestplay["word"])
            print(self.placonv(bestplay["place"]))
            print("Direction:", self.dirconv(bestplay["direction"]))
            print("Score:", bestplay["score"])
            self.rackonv()

    def dirconv(self, dirinit):
        if dirinit == "A":
            return "Across"
        return "Down"

    def placonv(self, place):
        return "Row: %d\nColumn: %d" % (int(place[0]), int(place[1]))

    def rackonv(self):
        print("Rack:", end = " ")
        for i in self.rack:
            print(i, end = "  ")
        print("\n")
        
    def displayBoard(self, board):
        count = 0
        text = ""
        text += "|"
        for i in range(16):
            line = board[i]
            for j in line:
                if j == " ":
                    if i == 0:
                        j = "  "
                    else:
                        j = "   "
                if j[0] in ascii_uppercase and len(j) < 3:
                    j = " " + j[0] + " "
                text += j
                text += "|"
                count += 1
                if count == 16 and i != 15:
                    text += "\n"
                    text += "-" * 64
                    text += "\n"
                    text += "|"
                    count = 0
        text += "\n"
        print(text)
        
    def placeWord(self, word, board, place, direction): #From old text version; uses conversion; assumes direction
        #Needs to calculate score
        #print(place)
        #print(board)
        
        start = board[int(place[0])][int(place[1])]
        length = len(word)
        row = int(place[0])
        column = int(place[1])
        score = 0
        for num in range(0, length):

            if direction == 'A':
                try:
                    if board[row][column] not in ascii_uppercase: #checks if space isn't letter
                        if board[row][column] in self.scoreList:
                            pass 
                        board[row][column] = word[num]
                        
                        column += 1
                    else:
                        return False
                except:
                    #print("nope")
                    return False
            else:
                #row += 1
                try:
                    if board[row][column] not in ascii_uppercase:
                        board[row][column] = word[num]
                        row += 1
                    else:
                        return False
                except:
                    #print("nope")
                    return False
        return True
    
    #def getBoardWords(self, board): #Needs to get the exact placing of the word for getMoveAttributes
#        super(CPU, self).getBoardWords(board)
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

    def getScore(self, moveAtts):
        row = moveAtts["place"][0]
        column = moveAtts["place"][1]
        specialScores = {"TLS":[], "DLS":[], "DWS":[], "TWS":[]}
        wordsToScore = [moveAtts["word"]]
        for letter in range(len(moveAtts["word"])):
            sp = self.board[row][column]
            if sp == "TWS":
                specialScores["TWS"] = [moveAtts["word"]]
            elif sp == "DWS":
                specialScores["DWS"] = [moveAtts["word"]]
            elif sp == "TLS":
                specialScores["TLS"].append(moveAtts["word"][letter])
            elif sp == "DLS":
                specialScores["DLS"].append(moveAtts["word"][letter])
            if moveAtts["direction"] == "A":
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["up"] in ascii_uppercase:
                    nrow = row
                    word = spAtts["text"]
                    while spAtts["up"] in ascii_uppercase:
                        word += spAtts["up"]
                        nrow += 1
                        spAtts = self.getAttributes("%d,%d" % (nrow, column), moveAtts["board"])
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                    
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["down"] in ascii_uppercase:
                    nrow = row
                    word = spAtts["text"]
                    while spAtts["down"] in ascii_uppercase:
                        word += spAtts["down"]
                        nrow -= 1
                        spAtts = self.getAttributes("%d,%d" % (nrow, column), moveAtts["board"])
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                column += 1
            else:
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["right"] in ascii_uppercase:
                    ncol = column
                    word = spAtts["text"]
                    while spAtts["right"] in ascii_uppercase:
                        word += spAtts["right"]
                        ncol += 1
                        spAtts = self.getAttributes("%d,%d" % (row, ncol), moveAtts["board"])
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                    
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["left"] in ascii_uppercase:
                    ncol = column
                    word = spAtts["text"]
                    while spAtts["left"] in ascii_uppercase:
                        word += spAtts["left"]
                        ncol -= 1
                        spAtts = self.getAttributes("%d,%d" % (row, ncol), moveAtts["board"])
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                row += 1

        wordScore = 0
        for letter in moveAtts["word"]:
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
            scoreLetters = item[1]
            if scoreType == "DWS":
                try:
                    if scoreLetters[0] == moveAtts["word"]:
                        wordScore *= 2
                except:
                    pass
            elif scoreType == "TWS":
                try:
                    if scoreLetters[0] == moveAtts["word"]:
                        wordScore *= 3
                except:
                    pass

        for word in wordsToScore:
            if word != moveAtts["word"]:
                for letter in word:
                    wordScore += self.scores[letter.lower()]

        moveAtts["score"] = wordScore
        
    def getMoveAttibutes(self, move):
        testBoard = [].extend(self.board) #Non-aliasing copy of self.board

    def rNab(self):
        nbo = []
        for row in self.board:
            nbo.append([])
            for col in row:
                nbo[-1].append(col)
        return nbo
    
    def resetBoard(self):
        pass
    
    def endTurn(self):
        pass

class ScoreMovable(MovingLetter):
    def __init__(self, root, text, row, column, frame):
        self.root = root
        self.overframe = frame
        self.row = row
        self.column = column
        self.text = text
        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10, "?" : 0}
    def getFrame(self):
        self.mainframe = Frame(self.overframe, bd  = 1, relief = SUNKEN)
        self.mainframe.place(x = (self.column * 31) + 50, y = (self.row * 31) + 50, \
                             width = 31, height = 31)
        self.label = Label(self.mainframe, bd=1, relief=RAISED, \
                           text=self.text+self.getSubscript(self.scores[self.text.lower()]),  #Puts the points for the letter on the label\
                           height=size, width=size, bg="yellow")
        self.label.pack(fill=X, padx=1, pady=1)
        self.mainframe.lift()
        
cpu = CPU()
#cpu.rack = ["O", "F", "L", "N", "H", "E", "C"]
cpu.takeTurn()
#cpu = CPU()
