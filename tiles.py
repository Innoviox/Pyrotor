import functions as func
import sys
def genstr():
    s = ""
    for i in list((func.choice(func.printable[:-6]) for i in range(func.randint(5, 10)))):
        s+=i
    return s

def genidstr(obj):
    s = ""
    idq = id(obj)
    for i in str(idq):
        s += func.printable[10:-6][(int(i)+func.randint(15, 450)) % 65]
    return s
try:
    from matplotlib.mathtext import math_to_image, MathTextParser
    from matplotlib.font_manager import FontProperties
    from io import BytesIO
    from PIL import ImageTk, Image
    from tkinter import PhotoImage
    #from matplotlib.mathtext import MathTextParser
    from matplotlib.image import imsave

    class Subscript():#tk.Frame):
        def __init__(self, root, letter, x, y, board=False):
            #tk.Frame.__init__(self, frame)
            #self.pack()
            self.scores = {'r': '1', 'v': '4', 'e': '1', 'h': '4', 'u': '1', 'y': '4', '?': '0', 'k': '5', 'f': '4', 'a': '1', 's': '1', 'i': '1   ', 'o': '1', 'm': '3', 't': '1', 'z': '10', 'x': '8', 'q': '10', 'n': '1', 'l': '1', 'w': '4', 'd': '2', 'g': '2', 'b': '3', 'p': '3', 'c': '3', 'j': '8'}
            
            self.frame = func.Frame(root, width=29, height=29, bd=1, relief=func.SUNKEN)
            self.frame.place_configure(x=x, y=y)
            self.letter = letter
            #self.root = root
            #print(x, y)
            self.x_pos = x
            self.y_pos = y
            self.board = board
            self.createN(letter.upper())
            #print(letter)


        def createN(self, letter):
            font = FontProperties()
            font.set_family('sans-serif')
            parser =  MathTextParser('bitmap')
            data, someint = parser.parse(r'%s$_{%s}$' % (letter, self.scores[letter.lower()]), dpi=130)
            if self.board:
                cap='gist_gray_r'
            else:
                cap='gnuplot_r'
            imsave("resources/%s.png" % letter,data.as_array(),cmap=cap)
            img = ImageTk.PhotoImage(master = self.frame, file="resources/%s.png" % letter, width=29, height=29)
            #print(self.frame)
            #self.frame.pack()
            self.label = func.Label(self.frame, image=img, relief=func.RAISED)#, width=31, height=31)
            self.label.image = img
            #print(self.x_pos, self.y_pos)
            #self.label.place_configure(x=self.x_pos, y=self.y_pos, width=31, height=31)
            self.label.pack()
            
        def createWidgets(self, letter):
            buffer = BytesIO()
            math_to_image(r'$%s_%d$' % (letter, self.scores[letter.lower()]), buffer, dpi=100, format='png')
            buffer.seek(0)
            pimage= Image.open(buffer)
            imag = ImageTk.PhotoImage(pimage)
            self.label = func.Label(self.frame,image=imag)
            self.label.image = imag
            self.label.pack()#side="bottom")
    mpl_in = 1
    _w, _h, _d = 31, 31, 0
except ImportError:

    #print("matplotlib at %s not found" % genstr(), file = sys.stderr)
    #print("PIL at %s not found" % genstr(), file=sys.stderr)
    #print("io at %s not found" % genstr(), file=sys.stderr)
    mpl_in = 0
    _w, _h, _d = 31, 31, 0
#q = open("unicode_data.txt", encoding="utf-8")
#print(q.read().split())
class MovingLetter():
    """Base tile class. 31x31 frame, moves with mouse. Main graphics of the entire game; can create board."""
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
        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
       "x": 8, "z": 10, "?" : 0}
        
        self. root = root
        self.rackFrame = frame
        self.x = x
        self.y = y

        self.origX = x
        self.origY = y

        self.text = text
        self.origText = text
        if text == "?": #Blank tile
            self.blankChosen = 0
            self.blankWindow = func.Toplevel(self.root)
            self.blankWindow.geometry("%dx%d%+d%+d" % (self.root.winfo_screenwidth(), self.root.winfo_screenheight(), 0, 0))
            self.blankWindow.resizable(0, 0)
            self.blankWindow.withdraw()
            self.blankWindow.title("Choose Blank")
                      
        self.getFrame(31) #Same size as spaces on board
        
        self.hoveringOver = "%s,%s" % ("NA", "NA") #Not hovering over anything = "NA", you see this a lot
        self.getPositions() #So it knows where the board spaces are so it can go to them in snapToGrid()

    def getFrame(self, size):
        """Gets a frame of size {size} (normally 31) with text {self.text + subscirpt of score}"""
     
        #self.frame.pack()
        if mpl_in == 1:
            #self.frame.config(bd=0)
            overarch = Subscript(self.rackFrame, self.text, self.x, self.y)
            self.label = overarch.label
            self.frame = overarch.frame
            #print(self.x, self.y)
            #self.label.place_configure(x=self.x, y=self.y)
            self.label.bind('<ButtonPress-1>', self.startMoveWindow)
            self.label.bind('<B1-Motion>', self.MoveWindow)
            self.label.bind('<ButtonRelease-1>', self.checkForReturn)
            
            self.frame.bind('<ButtonPress-1>', self.startMoveWindow)
            self.frame.bind('<B1-Motion>', self.MoveWindow)
            self.frame.bind('ButtonRelease-1>', self.checkForReturn)

        else:
            self.frame = func.Frame(self.rackFrame, bd=1, relief=func.SUNKEN)
            self.frame.place(x=self.x, y=self.y, width=size, height=size)   
            self.label = func.Label(self.frame, bd=1, relief=func.RAISED, \
                               text=self.text+self.getSubscript(self.scores[self.text.lower()]),  #Puts the points for the letter on the label\
                               height=size, width=size, bg="yellow")
            self.label.pack(fill=func.X, padx=1, pady=1)

            self.label.bind('<ButtonPress-1>', self.startMoveWindow)
            self.label.bind('<B1-Motion>', self.MoveWindow)
            self.label.bind('<ButtonRelease-1>', self.checkForReturn)
            
            self.frame.bind('<ButtonPress-1>', self.startMoveWindow)
            self.frame.bind('<B1-Motion>', self.MoveWindow)
            self.frame.bind('ButtonRelease-1>', self.checkForReturn)
        
        self.frame.lift()

    def getSubscript(self, number):
        """Uses unicode characters to generate subscript letters; used for point values"""
        codes = {0:"\u2080", 1:"\u2081", 2:"\u2082", 3:"\u2083", 4:"\u2084", 5:"\u2085", 6:"\u2086", 7:"\u2087", 8:"\u2088", 9:"\u2089", 10:"\u2081\u2080"}
        return codes[number]
    
    def startMoveWindow(self, event):
        """Gets the last position when clicked, magnifies tile (does not work)"""
        self.lastX = event.x_root
        self.lastY = event.y_root
        self.magnify()

    def magnify(self, newSize=62):
        """Sets tile size to any size, default is double normal. very slow on my computer."""
##        if self.frame["width"] != newSize:
##            self.frame.destroy()
##            self.label.destroy()
##
##            self.getFrame(newSize)
        pass
    
    def MoveWindow(self, event):
        """Noves the frame to the mouse; event is mouse motion"""
        self.root.update_idletasks()
        self.x += event.x_root - self.lastX
        self.y += event.y_root - self.lastY
        if self.x > 644: self.x = 644 #So it can't go off the root
        if self.y > 669: self.y = 669
        if self.x < 0: self.x = 0
        if self.y < 0: self.y = 0
        
        self.lastX, self.lastY = event.x_root, event.y_root
        self.frame.place_configure(x=self.x, y=self.y)

        #self.snapToGrid()
            
        f1Position = (self.x, self.y)
        if self.isTouching(f1Position, (100, 550),
                           self.frame.winfo_width(), self.frame.winfo_height(),
                           300, 50):
            self.senseMovables()

        self.frame.lift()
        
    def snapToGrid(self):
        """Go to the nearest square on the board"""
        f1Position = [self.x, self.y]
        for labelPosition in self.labels_positionList.keys():
            #print(self.labels_positionList[labelPosition][0])
            #if self.isIn(self.x, self.y, labelPosition[0], labelPosition[1], _w, _h) 
            if self.isTouching(f1Position, labelPosition, self.frame["width"], self.frame["height"],
                               _w, _h):
                tempHover = self.formatPos(self.labels_positionList[labelPosition])
                if self.isEmpty(self.labels_positionList[labelPosition], coords=False): 
                    self.frame.place_configure(x=labelPosition[0]+_d, y=labelPosition[1]+_d)
                    self.hoveringOver = tempHover
                    self.x = labelPosition[0]
                    self.y = labelPosition[1]
                    f1Position = [self.x, self.y]
                    if self.text == "?" and self.blankChosen != 1:
                        self.chooseBlank()
                    break
                else:
                    pass
                    #self.goToNearestOpenSquare(labelPosition)
        #print(self.hoveringOver)

    def isEmpty(self, squarePos, coords=True):
        #So it can't go onto a tile already played
        if coords:
            if self.board[self.labels_positionList[squarePos][0]][self.labels_positionList[squarePos][1]] in \
                                   func.ascii_uppercase or self.formatPos(squarePos) in \
                                                   [movable.hoveringOver for movable in self.movables]:
                return False
            else:
                return True
        else:
            if self.board[squarePos[0]][squarePos[1]] in func.ascii_uppercase or self.formatPos(squarePos) in \
                                                   [movable.hoveringOver for movable in self.movables]:
                return False
            else:
                return True
            
    def isFull(self, squarePos, coords=True):
        return not self.isEmpty(squarePos, coords=coords)
    
    def formatPos(self, squarePos):
        return "%d,%d" % (squarePos[0], squarePos[1])

    def gkfv(self, dict, value):
        """gkfv == 'get key from value'"""
        return list(dict.keys())[list(dict.values()).index(value)]
    
    def goToNearestOpenSquare(self, startSquare):
        row = self.labels_positionList[startSquare][0]
        column = self.labels_positionList[startSquare][1]
        #fprint(row, column)
        rowAdd = 0
        rowSub = 0
        colAdd = 0
        colSub = 0

        while (row + rowAdd <= 15 and row - rowSub >= 1 and \
              column + colAdd <= 15 and column - colSub >= 1) and \
              (self.isFull([row, column+colAdd], coords=False) and \
              self.isFull([row, column-colSub], coords=False) and \
              self.isFull([row+rowAdd, column], coords=False) and \
              self.isFull([row-rowSub, column], coords=False)):
            rowAdd += 1
            rowSub += 1
            colAdd += 1
            colSub += 1

        if self.isEmpty([row, column+colAdd], coords=False):
            #print(row, column+colAdd, "1")
            self.frame.place_configure(x=(row*31)+50, y=((column+colAdd)*31)+50)
            self.hoveringOver = self.formatPos([row, column+colAdd])
            self.x = (row*31)+50
            self.y = ((column+colAdd)*31)+50
            if self.text == "?" and self.blankChosen != 1:
                self.chooseBlank()
                
        elif self.isEmpty([row, column-colSub], coords=False):
            #print(row, column-colSub, "2")
            self.frame.place_configure(x=(row*31)+50, y=((column-colSub)*31)+50)
            self.hoveringOver = self.formatPos([row, column-colSub])
            self.x = (row*31)+50
            self.y = ((column-colSub)*31)+50
            if self.text == "?" and self.blankChosen != 1:
                self.chooseBlank()
                
        elif self.isEmpty([row+rowAdd, column], coords=False):
            #print(row+rowAdd, column, "3")
            self.frame.place_configure(x=((row+rowAdd)*31)+50, y=((column)*31)+50)
            self.hoveringOver = self.formatPos([row+rowAdd, column])
            self.x = ((row+rowAdd)*31)+50
            self.y = ((column)*31)+50
            if self.text == "?" and self.blankChosen != 1:
                self.chooseBlank()
                
        elif self.isEmpty([row-rowSub, column], coords=False):
            #print(row-rowSub, column, "4")
            self.frame.place_configure(x=((row-rowSub)*31)+50, y=((column)*31)+50)
            self.hoveringOver = self.formatPos([row-rowSub, column])
            self.x = ((row-rowSub)*31)+50
            self.y = ((column)*31)+50
            if self.text == "?" and self.blankChosen != 1:
                self.chooseBlank()
                
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
        #self.magnify(newSize = 31)
        f1Position = (self.x, self.y)
        #If not touching board: go back; else go to nearest square on board
        if not(self.isTouching(f1Position, (self.boardX, self.boardY),
                          self.frame.winfo_width(), self.frame.winfo_height(),
                          self.boardWidth, self.boardHeight)):
            self.returnToOrig()
        else:
            self.snapToGrid()
            
    def getPositions(self):
        self.labels_positionList = {}
        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                if not(label[0] == "0" or label[0] == "1" or label[0].isalpha()):
                    self.labels_positionList[(i*31)+50, (j*31)+50] = (j, i)
                elif label in self.scoreList:
                    self.labels_positionList[(i*31)+50, (j*31)+50] = (j, i)
        self.boardWidth, self.boardHeight = 497, 497
        self.boardX, self.boardY = 50, 50
        
    def getBoard(self):
        """Main graphics point of the program; shows the board."""
        self.extraList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", \
                     "TWS", "DWS", "TLS", "DLS", \
                     "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ", \
                     "*", " "]
        colors = {"TWS":"red", "DWS":"pink", "TLS":"light green", "DLS":"light blue", "*":"pink"}
        self.boardFrame = func.Frame(self.root, bd=1, relief=func.SUNKEN)
        self.boardFrame.place(x=50, y=50, width=497, height = 497)
        labels = list()
        squares = list()

        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                if label in self.extraList:
                    entry = func.Frame(self.boardFrame, bd=1, relief=func.RAISED)
                    entry.place(x=(i*31), y=(j*31), width=31, height=31)
                    labels.append(func.Label(entry, text = label,
                                            height = 31, width = 31))
                    if label in colors.keys():
                        labels[-1].config(bg=colors[label])
                        
                    labels[-1].pack()
                else:
                    if mpl_in == 0:
                        frame = func.Frame(self.boardFrame, bd=1, relief=func.RAISED)
                        frame.place(x=(i*31), y=(j*31), width=31, height=31)
                        entry = func.Frame(self.boardFrame, bd=1, relief=func.SUNKEN)
                        entry.place(x=(i*31) + 3, y=(j*31) + 3, width=25, height=25)
                        squares.append(func.Label(entry, bd = 1, text=label+self.getSubscript(self.scores[label.lower()]),
                                             height=25, width=25, relief=func.RAISED))
                        squares[-1].pack(fill=func.X, padx=1, pady=1)
                        entry.lift()
                        
                    else:
                        #frame = func.Frame(self.boardFrame, bd=1, relief=func.RAISED)
                        #frame.place(x=(i*31), y=(j*31), width=31, height=31)
                        #entry = func.Frame(self.boardFrame, bd=1, relief=func.SUNKEN)
                        #entry.place(x=(i*31) + 3, y=(j*31) + 3, width=25, height=25)
                        hf = Subscript(self.boardFrame, label, i*31, j*31, board=True)
                        #squares.append(hf.label)
                        #squares[-1].pack(fill=func.X, padx=1, pady=1)
                        print(hf.letter)
                    
                    
        self.helpLabel = func.Label(self.root, text = "Note: For best tile placement, \naim for below and to the right of the square.", )
        self.helpLabel.place(x=50, y=10, height=35, width=497)
        
    def returnToOrig(self):
        self.magnify(newSize=31)
        self.x = self.origX
        self.y = self.origY
        self.frame.place_configure(x=self.x, y=self.y)
        self.hoveringOver = "NA,NA"
        if self.origText == "?":
            self.blankChosen = 0
            self.setBlank("?")
            
    def chooseBlank(self):
        self.blankWindow.deiconify()
        chooseLabel = func.Label(self.blankWindow, text = "Choose the tile you want your blank to be.")
        chooseLabel.place(x = 400, y = 200, width = 300, height = 100)
        self.choiceWindow = func.Frame(self.blankWindow)
        self.choiceWindow.place(x=400, y=400, width=500, height = 500)
        buttons = []
        row = 1
        column = 1
        for letter in func.ascii_uppercase:
            button = func.Button(self.choiceWindow, text = letter,
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
        self.label.config(text=self.text+self.getSubscript(0))
        #self.label.config(background="white") #should blanks be different color? no-score isn't implemented
        
    def senseMovables(self, *event):
        #To sense if it needs to switch with any other tiles on the rack. the event tag is unnecessary, right?
        for movable in self.movables:
            if self.isTouching((self.x, self.y), (movable.x, movable.y), 
                               _w, _h, _w, _h):
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
    """For dragging to the exchange rack (see player.exchange). Child of MovingLetter."""
    def __init__(self, root, text, x, y, frame):
        super(MovingExchangeLetter, self).__init__(root, text, x, y, frame)
        self.boundaryX, self.boundaryY = 1000, 350
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
        self.exchangeRackX, self.exchangeRackY = 150, 100
        self.labels_positionList = {}
        for column in range(7):
            self.labels_positionList[(self.exchangeRackX, column)] = ((column*30)+self.exchangeRackX, self.exchangeRackY+5)
    def getExchangeRack(self):
        self.exchangeRack = func.Frame(self.root, bd=1, relief=func.RAISED)
        self.exchangeRack.place(x=self.exchangeRackX, y=self.exchangeRackY, width=self.exchangeRackWidth, height = self.exchangeRackHeight)
        labels = []
        for i in range(7):
            labels.append(func.Label(self.exchangeRack, relief=func.SUNKEN))
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
        if not(self.isTouching(f1Position, (0, 0),
                          self.frame.winfo_width(), self.frame.winfo_height(),
                          425, 300)):
            self.frame.place_configure(x=self.origX, y=self.origY)
            #self.x = self.origX
            #self.y = self.origY
            self.onExchangeRack = False
    def weed_els(self):
        for el in self.els:
            if el is self:
                self.els.remove(el)
