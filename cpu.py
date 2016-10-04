import player
import functions as func

class CPU(player.Player):
    def __init__(self, root, rack, distribution):
        self.root = root
        if distribution != ():
           self.distribution = distribution
        else:
            self.distribution = False
        self.name = "CPU"
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
            ['08', 'TWS', ' ', ' ', 'DLS', ' ', ' ', ' ', 'B', 'O', 'G', ' ', 'DLS', ' ', ' ', 'TWS'],
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
        self.rack = rack
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
        self.turnrotation = 0
        self.valuations = {"?":0}
        ospdcomp=""
        for i in self.ospd:
            ospdcomp += i

        for letter in func.ascii_uppercase:
            self.valuations[letter] = ospdcomp.count(letter)
        #Leaves from http://quackle.cvs.sourceforge.net/viewvc/quackle/quackle/data/strategy/twl06/superleaves?revision=1.1
        valut = open("leaves.txt")
        self.rv = {}
        q = valut.read().split()
       # print(q[:20])
       # print(len(q))
        for i in range(0, len(q), 2):
            self.rv[q[i]] = float(q[i+1])
            #print(q[i], q[i+1])

    def getAllCorrectCombinations(self, iterable, maxDepth):
        allWords = []
        wordsWithBlanks = {}
        alreadyChecked = []
        for depth in range(4, maxDepth + 1): #only needs to get length 3 and above
            for word in func.permutations(iterable, depth):
                allWords.append("".join(word))
        naw = allWords[:]
        for i in range(len(naw)):
            word = naw[i]
            if "?" in word:
                allWords.remove(word)
                for l in func.ascii_uppercase:
                    nWord = list(word)
                    q = nWord.index("?")
                    nWord[q] = l
                    nWord = self.tostr(nWord)
                    if self.checkWord(nWord):
                        allWords.append(nWord)
                        alreadyChecked.append(nWord)
                        wordsWithBlanks[nWord] = q
        allWords.pop(0)
        correctWords = []
        for word in allWords:
            if word in alreadyChecked:
                correctWords.append(word)
            elif self.checkWord(word):
                correctWords.append(word)

        return correctWords#, wordsWithBlanks
    def tostr(self, l):
        h = ""
        for i in l: h += i
        return h
    def checkWord(self, word):
        if len(word) > 1:
            try:
                subdict = open("resources/" + word[:2] + ".txt").read().split()
            except:
                return False
            if word.upper() in subdict:
                return True
            return False
        return False
        
        

    def addKey(self, dictToCheck, key, value):
        super(CPU, self).addKey(dictToCheck, key, value)
        
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
    #Here's some functions that are in the player class but unfortunately could
    #not be supered because they had to be changed slightly
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
            
    def getAttributes(self, place, boardToCheck):
        touching = {}
        place = place.split(",")
        row = int(place[0])
        column = int(place[1])
        numTouching = 0
        if not row-1<1:
            try:
                up = boardToCheck[row-1][column]
            except:
                up = "NA"
            touching['up'] = up
            if up.upper() in func.ascii_uppercase:
                numTouching += 1

        else:
            touching['up'] = 'NA'
            
        if not row+1>15:
            try:
                down = boardToCheck[row+1][column]
            except:
                down = "NA"
            touching['down'] = down
            if down.upper() in func.ascii_uppercase:
                numTouching += 1

        else:
            touching['down'] = 'NA'

        if not column+1 > 15:
            try:
                right = boardToCheck[row][column+1]
            except:
                right = "NA"
            touching['right'] = right
            if right.upper() in func.ascii_uppercase:
                numTouching += 1
        else:
            touching['right'] = 'NA'

        if not column-1 < 1:
            try:
                left = boardToCheck[row][column-1]
            except:
                left = "NA"
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

    def getEvaluation(self, move):
        word = move["word"]
        p_xR = self.rack[:]
        p_xR.sort()
        for i in word:
            if i in p_xR:
                p_xR.remove(i)
        move["valuation"] = self.rv["".join(j for j in p_xR)]
                                       
    def playAllWords(self, maxlength = None):
        self.rackonv()
        if self.board[8][8] == "*":
            self.isFirstTurn = True
        else:
            self.isFirstTurn = False
            
        print("Loading...This step will take approximately", round(func.uniform(0.9, 1.2), 4), "seconds.")
        a = func.time()
        allMoves = []
        allWords = self.removeDuplicates(self.getAllCorrectCombinations(self.rack, 7))
        print("That step actually took", func.time() - a, "seconds.")
        boards = 0
        possboards = 0
        longwords = []
        if len(allWords) > 0:
            currmaxlen = max(len(i) for i in allWords)
            for word in allWords:
##                if 3 < len(word):
##                    possboards += 344
##                    longwords.append(word)
                if maxlength is None:
                    if len(word) == max(len(i) for i in allWords):
                        possboards += 344
                        longwords.append(word)
                else:
                    if len(word) == maxlength:
                        possboards += 344
                        longwords.append(word)
            
            print("Generating...This step will take approximately", round(possboards * 0.0023, 4), "seconds.")
            a = func.time()
            for word in longwords:
                    for row in range(1, len(self.board)):
                        for column in range(1, len(self.board[row])):
                            for direction in ["A", "D"]:
                                nbo = self.rNab()
                                d = self.getDepth(self.getAttributes("%d,%d" % (row, column), nbo), direc=direction)
                                #print(d, "%d,%d" % (row, column), word)
                                #self.displayBoard(nbo)
##                                func.sleep(1)
                                if d <= len(word):
                                    if self.placeWord(word, nbo, [row, column], direction):
                                        if self.checkWholeBoard(nbo, self.isFirstTurn)[0]:
                                            qbox = {"word":word, "board":nbo, "place":[row, column], "direction":direction}
                                            self.getEvaluation(qbox)
                                            allMoves.append(qbox)
                                            self.getScore(qbox)
            print("That step actually took", func.time() - a, "seconds.")

            return allMoves

        else:
            print("Exchanging...")
            self.exchange()
            self.drawTiles()
            return "Non"
    def takeTurn(self, maxlen = None):
        plays = self.playAllWords(maxlength = maxlen)
        if plays != "Non":
            self.turnrotation += 1
            self.nondisplay = False
            bestplay = {"score":0, "valuation":0}
            for play in plays:
                if play["score"]+play["valuation"] > bestplay["score"]+bestplay["valuation"]:
                    bestplay = play
            if bestplay == {"score":0, "valuation":0}:
                print("Something went wrong. Reloading...")
                maxleng = max(len(i) for i in self.getAllCorrectCombinations(self.rack, 7))
                self.turnrotation += 1
                if self.turnrotation >= 3:
                    print("Exchanging...")
                    self.exchange()
                    self.drawTiles()
                    self.nondisplay = True
                else:
                    self.takeTurn(maxlen = maxleng - 1)
            else:
                play = bestplay
                #for play in plays:
                self.displayBoard(play["board"])
                print("Word:", play["word"])
                print(self.placonv(play["place"]))
                print("Direction:", self.dirconv(play["direction"]))
                print("Score:", play["score"])
                print("Evaluation:", play["valuation"])
                print("Total Score:", play["score"] + play["valuation"])
                #self.rackonv()
            if not self.nondisplay and bestplay != {"score":0, "valuation":0}:
                self.turnrotation += 1
                self.score += bestplay["score"]
                self.board = bestplay["board"]
                for letter in bestplay["word"]:
                    self.rack.remove(letter)
            
    def dirconv(self, dirinit):
        if dirinit == "A":
            return "Across"
        return "Down"

    def placonv(self, place):
        return "Row: %d\nColumn: %s" % (int(place[0]), func.ascii_uppercase[int(place[1])-1])

    def rackonv(self):
##        pass
        print("Rack:", end = " ")
        for i in range(len(self.rack)):
            if i != len(self.rack)-1:
                print(self.rack[i], end = ", ")
            else:
                print(self.rack[i])
        #print("\n")
        
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
                if j[0] in func.ascii_uppercase and len(j) < 3:
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
        
    def placeWord(self, word, board, place, direction): 
        start = board[int(place[0])][int(place[1])]
        length = len(word)
        row = int(place[0])
        column = int(place[1])
        score = 0
        for num in range(0, length):

            if direction == 'A':
                try:
                    if board[row][column] not in func.ascii_uppercase: #checks if space isn't letter
                        if board[row][column] in self.scoreList:
                            pass 
                        board[row][column] = word[num]
                        
                        column += 1
                    else:
                        return False
                except:
                    return False
            else:
                try:
                    if board[row][column] not in func.ascii_uppercase:
                        board[row][column] = word[num]
                        row += 1
                    else:
                        return False
                except:
                    return False
        return True

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
            elif sp == "DWS" or sp == "*":
                specialScores["DWS"] = [moveAtts["word"]]
            elif sp == "TLS":
                specialScores["TLS"].append(moveAtts["word"][letter])
            elif sp == "DLS":
                specialScores["DLS"].append(moveAtts["word"][letter])
            if moveAtts["direction"] == "A":
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["up"] in func.ascii_uppercase:
                    nrow = row
                    word = spAtts["text"]
                    while spAtts["up"] in func.ascii_uppercase:
                        word += spAtts["up"]
                        if nrow + 1 < 16:
                            nrow += 1
                            spAtts = self.getAttributes("%d,%d" % (nrow, column), moveAtts["board"])
                        else:
                            break
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                    
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["down"] in func.ascii_uppercase:
                    nrow = row
                    word = spAtts["text"]
                    while spAtts["down"] in func.ascii_uppercase:
                        word += spAtts["down"]
                        if nrow + 1 < 16:
                            nrow += 1
                            spAtts = self.getAttributes("%d,%d" % (nrow, column), moveAtts["board"])
                        else:
                            break
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                column += 1
            else:
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["right"] in func.ascii_uppercase:
                    ncol = column
                    word = spAtts["text"]
                    while spAtts["right"] in func.ascii_uppercase:
                        word += spAtts["right"]
                        if ncol + 1 < 16:
                            ncol += 1
                            spAtts = self.getAttributes("%d,%d" % (row, ncol), moveAtts["board"])
                        else:
                            break
                    if len(word) == 3:
                        word = word[:2]
                    wordsToScore.append(word)
                    
                spAtts = self.getAttributes("%d,%d" % (row, column), moveAtts["board"])
                if spAtts["left"] in func.ascii_uppercase:
                    ncol = column
                    word = spAtts["text"]
                    while spAtts["left"] in func.ascii_uppercase:
                        word += spAtts["left"]
                        if ncol + 1 < 16:
                            ncol += 1
                            spAtts = self.getAttributes("%d,%d" % (row, ncol), moveAtts["board"])
                        else:
                            break
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
        if len(moveAtts["word"]) == 7:
            wordScore += 50
        moveAtts["score"] = wordScore
        

    def rNab(self):
        nbo = []
        for row in self.board:
            nbo.append([])
            for col in row:
                nbo[-1].append(col)
        return nbo
    def exchange(self):
        minVals = [1000000, 1000000, 1000000, 1000000] #Letters to keep; exchange 3 tiles
        for letter in self.rack:
            for val in minVals:
                if str(val) not in func.ascii_uppercase and self.valuations[letter] < val:
                    minVals[minVals.index(val)] = self.rack.index(letter)
                    break
        nar = self.rack[:]
        for index in range(len(self.rack)):
            if index not in minVals:
                nar.remove(self.rack[index])
        self.rack = nar[:]
        self.drawTiles()
    def getDepth(self, attributes, direc=None):
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
        if direc is None:
            if leftDepth == 0 or rightDepth == 0:
                return upDepth + downDepth
            elif upDepth == 0 or downDepth == 0:
                return leftDepth + rightDepth
        else:
            if direc == "A":
                return rightDepth
            elif direc=="D":
                return downDepth
            elif direc == "A1":
                return leftDepth + rightDepth
            else:
                return upDepth + downDepth
#c = CPU(func.root, [], func.distribution)
#c.rack = ["A", "G", "C", "P", "E", "N", "?"]
#print(c.getAllCorrectCombinations(c.rack, 7))
if __name__ == "main":
    c = CPU(func.root, [], func.distribution)
    #print(c.getDepth(
