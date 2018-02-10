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
                print(self.hoveringOver)

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

from tkinter import *
import random

class Turn():
    def __init__(self, x, y):
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
        


        self.root = Tk()
        self.root.title("Moving Widgets Test...attempt 8 :)")
        self.root.resizable(0,0)
        self.root.geometry("%dx%d%+d%+d"%(550, 700, 0, 0))
        
        self.rack = []
        self.drawTiles(7)
        
        self.rackFrame = Frame(self.root, bd=1, relief=RAISED)
        self.rackFrame.place(x=x-50, y=y, width=300, height=50)
        
        row = 0
        self.movables = []
        for letter in self.rack:
            self.movables.append(MovingLetter(self.root, letter, row*30+x, y+12.5, self.root))
            row += 1

        self.rackFrame.lower()
        self.movables[-1].getBoard()

        self.enterButton = Button(self.root, text = "Enter Word", command = self.get)
        self.enterButton.pack()
    def drawTiles(self, num):
        for i in range(num):
            letter = random.choice(self.distribution).upper()
            self.rack.append(letter)
    def get(self):
        for i in movables:
            
class Player():
    def __init__(self, playerNumber, name, board, conversion, distribution, ospd):
        self.rack = getRack(distribution)
        self.score = 0
        self.playerNumber = playerNumber
        self.name = name
        self.board = board
        self.conversion = conversion
        self.distribution = distribution
        self.ospd = ospd
        
    def _update(self):
        self.board = board
        
    def get(self):
        done = False
        while not done:
            word = input("Enter word: ")
            if checkWord(word, self.ospd):
                done = True
            else:
                print("Invalid word")

        done = False
        while not done:
            place = input("Enter word (letter for column, number for row): ")
            if place[0] in conversion.keys() and place[1] in conversion.values():
                done = True
            else:
                print("Invalid place")

        done = False
        while not done:
            direction = input("Enter direction ('a' for across, 'd' for down): ")
            if direction == "A" or direction == "D":
                done = True
            elif direction == "a":
                direction = "A"
                done = True
            elif direction == "d":
                direction = "D"
                done = True
            else:
                print("Invalid direction")
                
        return [word, place, direction]
        
    def play(self):
        done = False
        while not done:
            prompts = self.get()
            word = prompts[0]
            place = prompts[1]
            direction = prompts[2]
            if checkPlay(word, self.board, place, direction, self.conversion, self.ospd):
                self._update()
                self.getScore(word)
                print("You just scored", self.lastWordScore, \
                      "points.\nYour total is ", self.score, ".")
                drawTiles(word, self.rack)
                displayBoard(self.board)
                displayRack(self.rack, self.name)
                
                done = True
            else:
                print("Invalid play")
                
    def playOne(self):
        done = False
        while not done:
            prompts = self.get()
            word = prompts[0]
            place = prompts[1]
            direction = prompts[2]
            if checkPlayOne(word, self.board, place, direction, self.conversion, self.ospd):
                self._update()
                self.getScore(word)
                print("You just scored", self.lastWordScore, \
                      "points.\nYour total is ", self.score, ".")
                drawTiles(word, self.rack)
                displayBoard(self.board)
                displayRack(self.rack, self.name)
                
                done = True
            else:
                print("Invalid play")

    def getScore(self, word): #Rudimentary; does not include hooked letters.
        self.lastWordScore = 0
        for letter in word:
            self.lastWordScore += conversion[letter]
        self.score += self.lastWordScore




    def displayBoard(self):
        count = 0
        text = ""
        text += "|"
        for i in range(16):
            line = self.board[i]
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


    def drawTiles(self, numToAdd):
        while len(self.rack) < 7:
            self.rack.append('')
        for num in range(numToAdd):
            letter = random.choice(self.distribution)
            self.rack[num] = letter.upper()
            self.distribution.remove(letter)
            
    def displayRack(self):
        print(self.name + ", your tiles are:", end = " ")
        for letter in self.rack:
            print(letter, end = "")
        print()
        
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
        for i in touchingList: print(i)
        words = []

        touchingListAcross = []
        touchingListDown = []
        for item in touchingList:
            if item['right'] != "NA" and item['right'] != "  ":
                touchingListAcross.append(item)
            if item['down'] != "NA" and item['down'] != "  ":
                touchingListDown.append(item)
        usedLetters = []
        while touchingList:
            wordAcross = ""
            wordStart = touchingList[0]
            column = wordStart['column']
            row = wordStart['row']
            wordAcross += wordStart['text'][0]
            while column <= 15:
                right = wordStart['right']
                if right != "NA" and right != "  ":
                    column += 1
                    for item in touchingList:
                        if item['text'] == right and \
                           item['column'] == column and \
                           item['row'] == row and \
                           item in touchingListAcross:
                            touchingListAcross.remove(item)
                            wordStart = item
                            wordAcross += wordStart['text'][0]

                else:
                    break

            if len(wordAcross) > 1:
                for item in touchingList:
                    if item['column'] == wordStart['column'] + 1 and \
                       item['row'] == wordStart['row']:
                        wordAcross += item['text'][0]
                                    
            wordDown = ""
            wordStart = touchingList[0]
            column = wordStart['column']
            row = wordStart['row']
            wordDown += wordStart['text'][0]
            while row <= 15:
                down = wordStart['down']
                if down != "NA" and down != "  ":
                    row += 1
                    for item in touchingList:
                        if item['text'] == down and \
                           item['column'] == column and \
                           item['row'] == row and \
                           item in touchingListDown:
                            touchingListDown.remove(item)
                            wordStart = item
                            wordDown += wordStart['text'][0]
                else:
                    break
            if len(wordDown) > 1:
                for item in touchingList:
                    if item['column'] == wordStart['column'] and \
                       item['row'] == wordStart['row'] + 1:
                        wordDown += item['text'][0]
            touchingList.remove(touchingList[0])
            if len(wordAcross) > 1:
                words.append(wordAcross)
            if len(wordDown) > 1:
                words.append(wordDown)
        print(words)
    def isInTwice(self, letter, list):
        numTimesIn = 0
        for item in list:
            if item == letter:
                numTimesIn += 1
        if numTimesIn <= 2:
            return True
        else:
            return False
        
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

    
    def checkWholeBoard(self):
        touchingList = []
        for row in range(1, 16):
            for column in range(1, 16):
                touchingList.append([self.getNumTouchingLetters("%d%d" % (row, column))])
        print(touchingList)
        
    def placeWord(self, word, place, direction):
        start = board[int(place[1])][self.conversion[place[0]]]
        length = len(word)
        for num in range(length):
            row = int(place[1])
            column = self.conversion[place[0]]
            if direction == 'A':
                column += num
                if self.board[row][column] not in string.ascii_uppercase: #checks if space isn't letter
                    self.board[row][column] = word[num]
                else:
                    return False
            else:
                row += num
                if self.board[row][column] not in string.ascii_uppercase: 
                    self.board[row][column] = word[num]
                else:
                    return False
        return True
                
    def checkPlay(self, word, place, direction):
        #if checkWord(word, ospd):
        if self.placeWord(word, place, direction):
            touchingList = []
            for num in range(length):
                if direction == 'A':
                    touchingList.append(self.getAttributes(place, num)['numTouchingLetters'])
                else:
                    touchingList.append(self.getAttributes(place, num)['numTouchingLetters'])
            numTwos = 0
            for num in touchingList:
                if num >= 2:
                    numTwos += 1
            if self.checkWord(word):
                if len(word) > 2:
                    if numTwos >= (length - 2):
                        self.displayBoard(self.board)
                        return True
                    else:
                        return False
                else:
                    if numTwos >= 1:
                        self.displayBoard(self.board)
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False
        #else:
            #return False
        
    def checkPlayOne(self, word, place, direction):
        if self.checkPlay(word, place, direction):
            if board[8][8] == '*':
                return False
            else:
                return True

test = Turn(150, 550)
test.root.mainloop()
