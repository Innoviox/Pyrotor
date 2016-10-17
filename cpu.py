import player
import functions as func

class Proxy(player.Player):
    def __init__(self, rack, board, distribution, score, dict, vals, isFirstTurn):
        self.distribution = distribution[:]
        self.overdist = distribution[:]
        #print(id(distribution), id(self.distribution), id(self.overdist))
        #print(distribution is self.distribution, self.distribution is self.overdist)
        #print(len(self.distribution))
        #print(len(self.overdist))
        self.extraList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
             "TWS", "DWS", "TLS", "DLS", \
             "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "Kf ", "L ", "M ", "N ", "O ", \
             "*", " "]
        self.isFirstTurn = isFirstTurn
        self.board = board       
        self.score = score
        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10, "?" : 0}
        
        self.scoreList = ['TWS', 'DWS', 'TLS', 'DLS']
        self.rack = rack
        self.drawTiles()
        #super(Proxy, self).drawTiles()
        self.ospd = dict
        self.rv = vals
        self.turnrotation = 0
    def gac(self, iterable, minDepth, maxDepth):
        allWords = []
        for depth in range(minDepth, maxDepth + 1): #only needs to get length 3 and above
            for word in func.permutations(iterable, depth):
                allWords.append("".join(word))
        return allWords
    
    def gacc(self, iterable, maxDepth):
        allWords = self.gac(iterable, 3, maxDepth)
        wordsWithBlanks = {}
        alreadyChecked = []
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
        if len(allWords)>0:
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
        super(Proxy, self).addKey(dictToCheck, key, value)
        
    def drawTiles(self):
        #print("PROXY IS DRAWING TILES")
        #print("RACK:",self.rack)
##        if self.distribution:
        #print(self.distribution)
        if len(self.rack) < 7:
            while len(self.rack) < 7 and len(self.distribution) > 0:
                letter = func.choice(self.distribution)
                self.distribution.remove(letter)
                self.rack.append(letter.upper())
                #print(letter, end="")
##        else:
##             if len(self.rack) < 7:
##                while len(self.rack) < 7 and len(func.distribution) > 0:
##                    letter = func.choice(func.distribution)
##                    func.distribution.remove(letter)
##                    self.rack.append(letter.upper())
##                    print(letter, end="")
        print()
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
        try:
            move["valuation"] = self.rv["".join(j for j in p_xR)]
        except:
            move["valuation"] = 0
    def ge(self, simexch):
        p_xRs = self.rack[:]
        p_xRs.sort()
        for i in simexch:
            if i in p_xRs:
                p_xRs.remove(i)
        q = "".join(j for j in p_xRs)
        if q=="":
            return 0
        else:
            return self.rv[q]
    
    def playAllWords(self, maxlength = None): 
##        if self.board[8][8] == "*":
##            self.isFirstTurn = True
##        else:
##            self.isFirstTurn = False
            
        allMoves = []
        allWords = self.removeDuplicates(self.gacc(self.rack, 7))
        boards = 0
        possboards = 0
        longwords = []
        if len(allWords) > 0:
            currmaxlen = min(min(len(self.rack), 7), max(len(i) for i in allWords))
            print("PROXY {0}: Generating.".format(player.tiles.genidstr(id(self))))
            for word in allWords:
                if currmaxlen <= len(word):
                    possboards += 148
                    longwords.append(word)
            for word in longwords:
                    for row in range(1, len(self.board)):
                        for column in range(1, len(self.board[row])):
                            for direction in ["A", "D"]:
                                nbo = self.rNab()
                                #d = self.getDepth(self.getAttributes("%d,%d" % (row, column), nbo), direc=direction)
                                d = self.distances(int(row), int(column), direction)
                                if d >= len(word):
                                    if self.placeWord(word, nbo, [row, column], direction):
                                        if self.checkWholeBoard(nbo, self.isFirstTurn)[0]:
                                            qbox = {"word":word, "board":nbo, "place":[row, column], "direction":direction, 'type':'  Play  '}
                                            self.getScore(qbox)
                                            #print(qbox, qbox["score"])
                                            self.getEvaluation(qbox)
                                            allMoves.append(qbox)
                                            #print(qbox)


            return allMoves

        else:
            print("RELOAD ERROR {0}{1}{2}".format(player.tiles.genstr(), player.tiles.genstr(), player.tiles.genstr()))
            
            self.exchange()
 #           self.drawTiles()
            return "Non"

    def getBest(self, plays):
        bestplay = {"score":0, "valuation":0}
        for play in plays:
            if play is not None:
                if play["score"]+play["valuation"] > bestplay["score"]+bestplay["valuation"]:
                    bestplay = play
        return bestplay
    def takeTurn(self, maxlen = None):
        print("PROXY {0}: Generating.".format(player.tiles.genidstr(id(self))))
        plays = self.playAllWords(maxlength = maxlen)
        if type(plays)==type(""):
            #print("ABOUT TO BREAK", plays)
            self.distribution = self.overdist[:]
            self.rack = []
            self.drawTiles()
            print(self.rack)
            print(self.distribution)
            print(self.overdist)
            print(id(self.distribution))
            print(id(self.overdist))
            self.takeTurn()
            #pass
        else:
       # print("EJI", plays)
            plays.extend(self.exchange())
            pass
        #print("EJI", plays)
        if plays != "Non":
            self.turnrotation += 1
            self.nondisplay = False
            bestplay = self.getBest(plays)
            if bestplay == {"score":0, "valuation":0}:
                self.turnrotation += 1
                if self.turnrotation > 3:
##                    self.exchange()
####                    self.drawTiles()
                    self.nondisplay = True
                else:
                    self.takeTurn()
            else:
                play = bestplay
            if not self.nondisplay and bestplay != {"score":0, "valuation":0}:
                self.turnrotation += 1
                return bestplay
##                self.score += bestplay["score"]
##                self.board = bestplay["board"]
##                if bestplay["type"] == "Exchange":
##                    self.commit_exch(bestplay)
##                else:
##                    for letter in bestplay["word"]:
##                        self.rack.remove(letter)
            
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
        nar = self.gac(self.rack, 1, len(self.rack))
        vals = {}
        for c in nar:
            vals[self.ge(c)] = c
        exchs = []
        ep = vals.copy() 
        for i in range(min(len(vals), 10)):
            #print(i)
            ev = max(ep.keys())
            exch = vals[ev]
           # print("eijf", (ev, exch))
            exchs.append((exch, ev))
            #print(exchs)
            ep.pop(ev)
        ret = []
        for j in exchs:
            q = self.gmfev(j)
            #print(j, q)
            ret.append(q)
        return ret

    def gmfev(self, exch):
        move = {"score":0, "word":"".join(i for i in sorted(list(exch[0]))), "valuation":exch[1],"board":self.board, "direction":" ", "place":[" ", " "], 'type':'Exchange'}
        return move
    
    def commit_exch(self, exch):
        if type(exch) == type({}):
            exch = exch["word"]
        print(exch)
        nar = self.rack[:]
        for i in exch:
            print(i)
            nar.remove(i)
        self.rack = nar[:]
        #self.drawTiles()
        
    def distances(self, row_num, col_num, direc):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if not str(col_num).isdigit():
            col_num = ord(col_num.upper()) - ord('A') + 1
        col = [row[col_num] for row in self.board]
        row = self.board[row_num]
        rightDepth = next((i for i, c in enumerate(row[col_num+1:]) if c in letters), 15-col_num)
        leftDepth = next((i for i, c in enumerate(row[col_num-1:0:-1]) if c in letters), col_num-1)
        downDepth = next((i for i, c in enumerate(col[row_num+1:]) if c in letters), 15-row_num)
        upDepth = next((i for i, c in enumerate(col[row_num-1:0:-1]) if c in letters), row_num-1)

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
##        return {
##                'right': next((i for i, c in enumerate(row[col_num+1:]) if c in letters), 15-col_num),
##                'left': next((i for i, c in enumerate(row[col_num-1:0:-1]) if c in letters), col_num-1),
##                'down': next((i for i, c in enumerate(col[row_num+1:]) if c in letters), 15-row_num),
##                'up': next((i for i, c in enumerate(col[row_num-1:0:-1]) if c in letters), row_num-1)
##        }    
    def getDepth(self, attributes, direc=None):
        upDepth = 0
        downDepth = 0
        leftDepth = 0
        rightDepth = 0
        #print(attributes, direc)
        if attributes["up"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column, row-1)[::-1], self.board)
            while newLetter["up"] in self.extraList:
                upDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column, row-1)[::-1], self.board)
                
        if attributes["down"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column, row+1)[::-1], self.board)
            while newLetter["down"] in self.extraList:
                downDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column, row+1)[::-1], self.board)
                
        if attributes["left"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column-1, row)[::-1], self.board)
            while newLetter["left"] in self.extraList:
                leftDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column-1, row)[::-1], self.board)
                
        if attributes["right"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (row, column+1), self.board)
            while newLetter["right"] in self.extraList:
                rightDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (row, column+1), self.board)
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
            
class CPU(player.Player):
    def __init__(self, root, rack, distribution, otherPlayer):
        self.root = root
        self.otherPlayer = otherPlayer
        if distribution != ():
            self.distribution = distribution
            self.pd = self.distribution[:]
        else:
            self.distribution = False
            self.pd = func.distribution[:]
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
        self.drawTiles()
        #super(CPU, self).drawTiles()
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
    def gac(self, iterable, minDepth, maxDepth):
        allWords = []
        for depth in range(minDepth, maxDepth + 1): #only needs to get length 3 and above
            for word in func.permutations(iterable, depth):
                allWords.append("".join(word))
        return allWords
    
    def gacc(self, iterable, maxDepth):
        allWords = []
        wordsWithBlanks = {}
        alreadyChecked = []
        for depth in range(3, maxDepth + 1): #only needs to get length 3 and above
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
        if len(allWords)>0:
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
        #print("CPU IS DRAWING TILES")
        if self.distribution:
            if len(self.rack) < 7:
                while len(self.rack) < 7 and len(self.distribution) > 0:
                    letter = func.choice(self.distribution)
                    self.distribution.remove(letter)
                    self.rack.append(letter.upper())
                    #print(letter, end="")
        else:
             if len(self.rack) < 7:
                while len(self.rack) < 7 and len(func.distribution) > 0:
                    letter = func.choice(func.distribution)
                    func.distribution.remove(letter)
                    self.rack.append(letter.upper())
                    #print(letter, end="")
        #print()
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
        try:
            move["valuation"] = self.rv["".join(j for j in p_xR)]
        except:
            move["valuation"] = 0
        #print(move)
 #      move["valuation"] += self.lookahead(move, p_xR, move["board"])[0]
        
    def ge(self, simexch):
        p_xRs = self.rack[:]
        p_xRs.sort()
        for i in simexch:
            if i in p_xRs:
                p_xRs.remove(i)
        q = "".join(j for j in p_xRs)
        if q=="":
            return 0
        else:
            return self.rv[q]
    
    def playAllWords(self, maxlength = None):
        self.rackonv()
        if self.board[8][8] == "*":
            self.isFirstTurn = True
        else:
            self.isFirstTurn = False
            
        print("Loading...This step will take approximately", round(func.uniform(0.9, 1.2), 4), "seconds.")
        a = func.time()
        allMoves = []
        allWords = self.removeDuplicates(self.gacc(self.rack, 7))
        #print(allWords)
        print("That step actually took", func.time() - a, "seconds.")
        boards = 0
        possboards = 0
        longwords = []
        if len(allWords) > 0:
           # print(max(len(i) for i in allWords))
            currmaxlen = min(min(len(self.rack), 7), max(len(i) for i in allWords))
            #print(currmaxlen, max(len(i) for i in allWords))
            print("Should be only generating words of length {0} and above.".format(currmaxlen))
            for word in allWords:
                if currmaxlen <= len(word):
                    possboards += 148
                    longwords.append(word)
##                if maxlength is None:
##                    if len(word) == max(len(i) for i in allWords):
##                        possboards += 344
##                        longwords.append(word)
##                else:
##                    if 3<len(word):
##                        possboards += 344
##                        longwords.append(word)
            
            print("Generating...This step will take approximately", round(possboards * 0.0023, 4), "seconds.")
            a = func.time()
            for word in longwords:
                    for row in range(1, len(self.board)):
                        for column in range(1, len(self.board[row])):
                            for direction in ["A", "D"]:
                                nbo = self.rNab()
                                #d = self.getDepth(self.getAttributes("%d,%d" % (row, column), nbo), direc=direction)
                                #print(d, "Row:", row, "Column:", column, word)

                                #print(d, "%d,%d" % (row, column), word)
                                #self.displayBoard(nbo)
##                                func.sleep(1)
                                #d = 0 #self.getDepth deprecation :(
                                #print(int(row), int(column), direction)
                                d = self.distances(int(row), int(column), direction)
                                #print(d, int(row), int(column), direction, word, len(word))
                                #self.displayBoard(nbo)
                                if d >= len(word):
                                    if self.placeWord(word, nbo, [row, column], direction):
                                        if self.checkWholeBoard(nbo, self.isFirstTurn)[0]:
                                            qbox = {"word":word, "board":nbo, "place":[row, column], "direction":direction, 'type':'  Play  '}
                                            self.getScore(qbox)
                                            self.getEvaluation(qbox)
                                            allMoves.append(qbox)
                                else:
                                    pass
                                    #print(d, len(word), "DEPRECATION MUCH?")
                                    #func.sleep(10)
            print("That step actually took", func.time() - a, "seconds.")

            return allMoves

        else:
            print("Exchanging...")
            self.exchange()
            self.drawTiles()
            return "Non"

    def getBest(self, plays):
        bestplay = {"score":0, "valuation":0}
        for play in plays:
            if play["score"]+play["valuation"] > bestplay["score"]+bestplay["valuation"]:
                bestplay = play
        return bestplay
    def getBestN(self, plays, n):
        cSv = 0
        bPs = []
        ps = plays[:]
        for play in plays:
            pSv = play["score"]+play["valuation"]
            if play in ps and pSv>cSv:
                cSv = pSv
                bPs.append(play)
                ps.remove(play)
        #print(bPs)
        
    def takeTurn(self, exch = False):
        if self.distribution:
            self.pd = self.distribution[:]
        else:
            self.pd = func.distribution[:]
        plays = self.playAllWords()#maxlength = maxlen)
        if plays != "Non":
            if exch:
                plays.extend(self.exchange())
            if plays != []:
 #              plays.extend(self.exchange())
                #plays != []:
                self.turnrotation += 1
                self.nondisplay = False
                bestplays = []
                pNa = plays[:]
                #self.getBestN(plays, 7)
                bestplay = self.getBest(pNa)
                #self.getBestN(plays, 7)
 #               n = min(len(pNa), 10)
                #print("\n\n")
                #print("Plays to Consider:".center(80))
                #print()
     #           self.imps()
                #for i in plays:
                #    self.pm(i)
                #print("\n\n\n")
##                for i in range(n):
##                    bestplay = self.getBest(pNa)
##                    if bestplay == {"score":0, "valuation":0}:
##                        continue
##                    else:
##                        bestplays.append(bestplay)
##                        pNa.remove(bestplay)

                #print(bestplays)
    ##            if len(bestplays)>0:
    ##                bestplay = bestplays[0]
    ##                #print(bestplays)
                if bestplay == {"score":0, "valuation":0}:
                    #print("Something went wrong. Reloading...")
                    print("Reproxying...")
                    maxleng = max(len(i) for i in self.gacc(self.rack, 7))
                    self.turnrotation += 1
                    if self.turnrotation >= 3:
                        print("Exchanging...")
                        self.exchange()
                        self.drawTiles()
                        self.nondisplay = True
                    else:
                        self.takeTurn()#maxlen = maxleng - 1)
                else:
                    play = bestplay

                    #for i in bestplays:
    #                        self.pm(i)
                    #for play in plays:
                    print()
                    if play["type"] == "Exchange":
                        print("Exchanged Tiles:", play["word"])
                        self.commit_exch(play)
                    else:
                        self.displayBoard(play["board"])
                        print("Word:", play["word"])
                        print(self.placonv(play["place"]))
                        print("Direction:", self.dirconv(play["direction"]))
                        print("Score:", play["score"])
 #                       print("Evaluation:", play["valuation"])
 #                       print("Total Score:", play["score"] + play["valuation"])
                    #self.rackonv()
                if not self.nondisplay and bestplay != {"score":0, "valuation":0}:
                    self.turnrotation += 1
                    self.score += bestplay["score"]
                    self.board = bestplay["board"]
                    if play["type"] != "Exchange":
                        for letter in bestplay["word"]:
                            self.rack.remove(letter)
            else:
                self.takeTurn(exch=True)
        else:
            self.takeTurn(exch=True)
            
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
        nar = self.gac(self.rack, 3, len(self.rack))
        vals = {}
        for c in nar:
            #print(c, self.ge(c))
            vals[self.ge(c)] = c
        exchs = []
        ep = vals.copy()
       # print("Generating exchange values...this will take about {0} seconds.".format(func.uniform(3, 7)))
        
        for i in range(min(len(vals), 10)):
            ev = max(ep.keys())
            exch = vals[ev]
            exchs.append((exch, ev))#+self.lookahead(self.gmfev((exch, ev)), self.rack, self.board)[0]))
            ep.pop(ev)
        #self.imps()
        ret = []
        for i in exchs:
            ret.append(self.gmfev(i))
        return ret

    def gmfev(self, exch):
        "Get move from exchange value"
        move = {"score":0, "word":"".join(i for i in sorted(list(exch[0]))), "valuation":exch[1],"board":self.board, "direction":" ", "place":[" ", " "], 'type':'Exchange'}
        return move
        self.pm(move)
    def imps(self, *h):
        print("  Type   Word   Score  Valuation   Direction     Row       Column     Total")
        print("----------------------------------------------------------------------------", end="")
        if h:
            print("------------------------")
        else:
            print()
    def pm(self, m):
        def wijof(a):
            q=int(a)/10
            if q >= 1:
                return "%2.3f" % a
            elif q<=0:
                if q<=-1:
                    return "%2.2f" % a
                elif a<0:
                    return "%1.3f" % a
                else:
                    return "%1.4f" % a
            else:
                return "%1.4f" % a
        print("%s %7s   %2d      %s      %s         %2s          %2s       %s" % (m["type"], m["word"], m["score"], \
                                                                     wijof(m["valuation"]), m["direction"], \
                                                                     str(m["place"][0]), str(m["place"][1]), \
                                                                     wijof(m["score"] + m["valuation"])))
    def commit_exch(self, exch):
        if type(exch) == type({}):
            exch = exch["word"]
        #print(exch)
        nar = self.rack[:]
        for i in exch:
            #print(i, end="EXCH")
            #print(nar)
            nar.remove(i)
        self.rack = nar[:]
        self.drawTiles()
    def distances(self, row_num, col_num, direc):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if not str(col_num).isdigit():
            col_num = ord(col_num.upper()) - ord('A') + 1
        col = [row[col_num] for row in self.board]
        row = self.board[row_num]
        rightDepth = next((i for i, c in enumerate(row[col_num+1:]) if c in letters), 15-col_num)
        leftDepth = next((i for i, c in enumerate(row[col_num-1:0:-1]) if c in letters), col_num-1)
        downDepth = next((i for i, c in enumerate(col[row_num+1:]) if c in letters), 15-row_num)
        upDepth = next((i for i, c in enumerate(col[row_num-1:0:-1]) if c in letters), row_num-1)

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
##        return {
##                'right': next((i for i, c in enumerate(row[col_num+1:]) if c in letters), 15-col_num),
##                'left': next((i for i, c in enumerate(row[col_num-1:0:-1]) if c in letters), col_num-1),
##                'down': next((i for i, c in enumerate(col[row_num+1:]) if c in letters), 15-row_num),
##                'up': next((i for i, c in enumerate(col[row_num-1:0:-1]) if c in letters), row_num-1)
##        }  
    def getDepth(self, attributes, direc=None):
        upDepth = 0
        downDepth = 0
        leftDepth = 0
        rightDepth = 0
        #print(attributes, direc)
        if attributes["up"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column, row-1)[::-1], self.board)
            while newLetter["up"] in self.extraList:
                upDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column, row-1)[::-1], self.board)
                
        if attributes["down"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column, row+1)[::-1], self.board)
            while newLetter["down"] in self.extraList:
                downDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column, row+1)[::-1], self.board)
                
        if attributes["left"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (column-1, row)[::-1], self.board)
            while newLetter["left"] in self.extraList:
                leftDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (column-1, row)[::-1], self.board)
                
        if attributes["right"] in self.extraList:
            row = attributes["row"]
            column = attributes["column"]
            newLetter = self.getAttributes("%d,%d" % (row, column+1), self.board)
            while newLetter["right"] in self.extraList:
                rightDepth += 1
                row = newLetter["row"]
                column = newLetter["column"]
                newLetter = self.getAttributes("%d,%d" % (row, column+1), self.board)
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
            
    def initProxy(self, rack, board):
        return Proxy(rack, board, self.pd[:], self.score, self.ospd, self.rv, self.isFirstTurn)
    
    def execProxy(self, rack, board):
        p_X = self.initProxy(rack, board)
        move = p_X.takeTurn()
        return move
    
    def _pxDraw(self, rack):
        while len(rack) < 7 and len(self.pd)>0:
            letterChosen = func.choice(self.pd)
            self.pd.remove(letterChosen)
            rack.append(letterChosen.upper())
        #print(rack)
        return rack

    def pdset(self):
        if self.distribution:
            self.pd = self.distribution[:]
        else:
            self.pd = func.distribution[:]
    def lookahead(self, move, rack, board):
        oPPm = None
        
        while oPPm is None:
            self.pdset()
            oPPm = self.execProxy([], move["board"]) #other Player Proxy move
        sPm = None
        nAr = self.rack[:] #non-Aliased rack
        for i in move["word"]:
            nAr.remove(i)
        newRack = self._pxDraw(nAr)
        while sPm is None:
            self.pdset()
            sPm = self.execProxy(newRack, oPPm["board"]) #self Proxy move
        oPt = round(oPPm["score"] + oPPm["valuation"], 2)
        sPt = round(sPm["score"] + sPm["valuation"], 2)
        winning = self.score + sPm["score"] > self.otherPlayer.score + oPPm["score"] #crude win evaluation calculation
        #print(move)
        print("\nSample Proxy move at %s" % player.tiles.genidstr(oPPm))
        print()
        print("                        ", end="") 
        self.imps(True)
        print("Original Play:          ", end="")
        self.pm(move)
        print("Random Opponent's Play: ", end="")
        self.pm(oPPm)
        print("CPU's Response:         ", end="")
        self.pm(sPm)
##        print("Final scoring: {0} + {1} + ({2} - {3}) = {4}".format(move["score"], move["valuation"], \
##                                                              sPt, oPt, round(move["score"] + move["valuation"] + (sPt-oPt),2)))
        print("End\n\n")
        return move["score"] + move["valuation"] + (sPt-oPt), winning
#c = CPU(func.root, [], func.distribution)
#c.rack = ["A", "G", "C", "P", "E", "N", "?"]
#print(c.getAllCorrectCombinations(c.rack, 7))
if __name__ == "__main__":
    p = player.Player(func.root, 1, "ProxyStandInObject", 0, 0, 'n', 'n', [], func.distribution, True)
    c = CPU(func.root, [], [], p)
    #c.displayBoard(c.board)
    #print(c.getDepth(c.getAttributes("8,1", c.board), "D"))
    c.takeTurn()
    #print(c.distribution)
    #print(func.distribution)
    #c.exchange()
##    c.rackonv()
##    for i in range(5):
##        c.exchange()
##        c.rackonv()
##        bingos = []
##        for i in c.gacc(c.rack, 7):
##            if len(i)==7 and i not in bingos:
##                bingos.append(i)
##        print(bingos)
