from tkinter import *
from random import choice
class Movement:
     def drawTiles(self, distribution, number):
        rack = ['', '', '', '', '', '', '']
        for num in range(number):
            letter = choice(distribution)
            rack[num] = letter.upper()
            distribution.remove(letter)
        return rack
    
     def getButtons(self):
        self.buttonFrame = Frame(self.root, bd=1, relief=SUNKEN)
        self.buttonFrame.place(x=450, y=0, width=300, height = 50)
        gridRow = 1
        gridColumn = 1
##        rowChange = 0
        buttons = list()
        for i in range(len(self.rack)):
            letter = self.rack[i]
            self.f = Frame(self.root, bd=1, relief=SUNKEN)
            self.f.place(x=i*30, y=25, width=25, height=25)
            self.labelTest = Label(self.f, bd=1, relief=RAISED, text="A", width = 25)
            self.labelTest.pack(fill=X, padx=1, pady=1)
            self.labelTest.bind('<ButtonPress-1>', self.startMoveWindow)
            self.labelTest.bind('<B1-Motion>', lambda event, widget=self.labelTest:
                                 self.MoveWindow(event,widget))
            self.f.bind('<ButtonPress-1>', self.startMoveWindow)
            self.f.bind('<B1-Motion>', lambda event, widget=self.f:
                                 self.MoveWindow(event,widget))


##            rowChange += 1
 #           gridColumn += 1
##            if rowChange % 5 == 0:
##                gridRow += 1
##                gridColumn = 1
            
##         self.movingWindows = []
##         for i in range(len(self.rack)):
##             letter = self.rack[i]
##             self.movingWindows.append(self.getMovingWindow(letter))
## #            self.movingWindows[-1][0].grid(0, i)
     def startMoveWindow(self, event):
        self.__lastX, self.__lastY = event.x_root, event.y_root

     def MoveWindow(self, event, widget):
        #print(event, widget)
        self.root.update_idletasks()
        self.__winX += event.x_root - self.__lastX
        self.__winY += event.y_root - self.__lastY
        self.__lastX, self.__lastY = event.x_root, event.y_root
        widget.place_configure(x=self.__winX, y=self.__winY)
##        f2Position = [self.f2.winfo_rootx(),self.f2.winfo_rooty()]
##        f1Position = [self.__winX, self.__winY]
##        if self.isTouching(f1Position, f2Position,
##                           self.f.winfo_width(), self.f.winfo_height(),
##                           self.f2.winfo_width(), self.f2.winfo_height()):
##            print("touching!")
        f1Position = [widget.winfo_rootx(), widget.winfo_rooty()]
        print(f1Position)
        for labelPosition in self.labels_positionList:
            if self.isTouching(f1Position, labelPosition,
                               widget.winfo_width(), widget.winfo_height(),
                               25, 25):
                widget.place_configure(x=labelPosition[0], y=labelPosition[1])
                #print("touching!")
            #break
        widget.lift()
        
     def isTouching(self, position1, position2, width1, height1, width2, height2):
        #print(position1, position2, width1, height1, width2, height2)
##        if (position2[0] < width1 or position2[1] < height1) and (position2[0] > position1[0] or position2[1] < position1[1]):
##            return True
##        elif (position1[0] < width2 or position1[1] < height2) and (position1[0] < position2[0] or position1[1] > position1[1]):
##            return True
##        else:
##            return False
        if ((position1[0] > position2[0]) or (position1[0] + width1) > position2[0]) and \
           ((position1[1] > position2[1]) or (position1[1] + height1) > position2[1]) and \
           ((position1[0] < (position2[0] + width2)) and (position1[1] < (position2[1] + height2))):
            return True
        elif ((position2[0] > position1[0]) or (position2[0] + width2) > position1[0]) and \
           ((position2[1] > position1[1]) or (position2[1] + height2) > position1[1]) and \
            ((position2[0] < (position1[0] + width1)) and (position2[1] < position1[1] + height1)):
            return True

        else:
            return False
     def goToEntry(self,event):
        entryXY=choice(self.labels_positionList)
        entryX,entryY=entryXY[0],entryXY[1]
        
        self.f.place_configure(x=entryX,y=entryY)
     def getBoard(self):
        self.boardFrame = Frame(self.root, bd=1, relief=SUNKEN)
        self.boardFrame.place(x=0, y=0, width=450, height = 450)
        self.labels_positionList = []
        labels = list()
        squares = list()
        self.labels = []
        self.labels_positionList = []
        self.labels_dimensionList = {}
##        for i in range(16):
##            label = self.board[0][i]
##            labels.append(Label(self.boardFrame, text = label,
##                                height = 1, width = 1))
##            labels[-1].place(x=i*25+10, y=0, width=25, height=25)
        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                entry = Frame(self.boardFrame, bd=1, relief=RAISED)
                entry.place(x=(i*25), y=(j*25)+25, width=25, height=25)
                if label[0] == "0" or label[0] == "1" or label[0].isalpha():
                    labels.append(Label(entry, text = label,
                                        height = 25, width = 25))
                    labels[-1].pack()
##                    labels[-1].grid(row=i+1, column = j)
##                    self.labels_positionList.append([labels[-1].winfo_rootx(),
##                                                    labels[-1].winfo_rooty()])
                else:
                    squares.append(Label(entry, text=label,
                                         height=25, width=25))
                    squares[-1].pack()
                    self.labels_positionList.append([(i*25), (j*25)])
                
     def getMovingWindow(self, text):
        self.__winX, self.__winY = 500, 200
        self.f = Frame(self.root, bd=1, relief=SUNKEN)
        self.f.place(x=self.__winX, y=self.__winY, width=25, height=25)

        self.labelTest = Label(self.f, bd=1, relief=RAISED, text=text, width = 25)
        self.labelTest.pack(fill=X, padx=1, pady=1)

        self.f.bind('<ButtonPress-1>', self.startMoveWindow)
        self.f.bind('<B1-Motion>', self.MoveWindow)
        self.labelTest.bind('<ButtonPress-1>', self.startMoveWindow)
        self.labelTest.bind('<B1-Motion>', self.MoveWindow)


        return [self.f, self.labelTest]
     def __init__(self):
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
        #self.rack = self.drawTiles(self.distribution, 7)
        self.root = Tk()
        self.root.title("Movement Test")
        self.root.resizable(0,0)
        self.root.geometry("%dx%d%+d%+d"%(1000, 850, 0, 0))

        self.__winX, self.__winY = 500, 200
        self.f = Frame(self.root, bd=1, relief=SUNKEN)
        self.f.place(x=self.__winX, y=self.__winY, width=25, height=25)

        self.labelTest = Label(self.f, bd=1, relief=RAISED, text="A", width = 25)
        self.labelTest.pack(fill=X, padx=1, pady=1)
        self.labelTest.bind('<ButtonPress-1>', self.startMoveWindow)
        self.labelTest.bind('<B1-Motion>', lambda event, widget=self.labelTest:
                            self.MoveWindow(event,widget))
        self.f.bind('<ButtonPress-1>', self.startMoveWindow)
        self.f.bind('<B1-Motion>', lambda event, widget=self.f:
                            self.MoveWindow(event,widget))
        #print(self.labelTest.cget("text"))
        
        #self.drawTiles(self.distribution, 7)

##        self.labelTest.focus_set()
##        self.f.focus_set()
        #self.getButtons()
        self.getBoard()
        self.f.lift()
        self.root.mainloop()

x = Movement()
