class MovingWidget():

    def startMoveWindow(self, event):
        self.__lastX, self.__lastY = event.x_root, event.y_root

    def MoveWindow(self, event):
        self.root.update_idletasks()
        self.__winX += event.x_root - self.__lastX
        self.__winY += event.y_root - self.__lastY
        self.__lastX, self.__lastY = event.x_root, event.y_root
        self.f.place_configure(x=self.__winX, y=self.__winY)

        f1Position = (self.__winX, self.__winY)
        for labelPosition in self.labels_positionList.keys():
            if self.isTouching(f1Position, labelPosition,
                               self.f.winfo_width(), self.f.winfo_height(),
                               25, 25):
                self.f.place_configure(x=labelPosition[0], y=labelPosition[1])

        self.f.lift()
    def isTouching(self, position1, position2, width1, height1, width2, height2):
        #print(position1, position2, width1, height1, width2, height2)
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
    def getPositions(self):
        self.labels_positionList = {}
        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                if not(label[0] == "0" or label[0] == "1" or label[0].isalpha()):
                    self.labels_positionList[((i*25), (j*25))] = (j, i)
    def __init__(self, text, x, y):
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


        self.root = Tk()
        self.root.title("...")
        self.root.resizable(0,0)
        self.root.geometry("%dx%d%+d%+d"%(640, 480, 0, 0))
        self.getPositions()
        
        self.__winX, self.__winY = x, y
        self.f = Frame(self.root, bd=1, relief=SUNKEN)
        self.f.place(x=self.__winX, y=self.__winY, width=25, height=25)

        self.l = Label(self.f, bd=1, relief=RAISED, text=text, width=25)
        self.l.pack(fill=X, padx=1, pady=1)

        self.l.bind('<ButtonPress-1>', self.startMoveWindow)
        self.l.bind('<B1-Motion>', self.MoveWindow)
        self.f.bind('<ButtonPress-1>', self.startMoveWindow)
        self.f.bind('<B1-Motion>', self.MoveWindow)
        self.f.lift()

        self.root.mainloop()
    def getBoard(self):
        self.boardFrame = Frame(self.root, bd=1, relief=SUNKEN)
        self.boardFrame.place(x=0, y=0, width=450, height = 450)
        labels = list()
        squares = list()

        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                entry = Frame(self.boardFrame, bd=1, relief=RAISED)
                entry.place(x=(i*25), y=(j*25)+25, width=25, height=25)
                if label[0] == "0" or label[0] == "1" or label[0].isalpha():
                    labels.append(Label(entry, text = label,
                                        height = 25, width = 25))
                    labels[-1].pack()
                else:
                    squares.append(Label(entry, text=label,
                                         height=25, width=25))
                    squares[-1].pack()

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

def getRack(distribution):
    rack = ['', '', '', '', '', '', '']
    for i in range(7):
        letter = random.choice(distribution).upper()
        rack[i] = letter
    return rack

root = Tk()
root.title("...")
root.resizable(0,0)
root.geometry("%dx%d%+d%+d"%(740, 480, 0, 0))

rack = getRack(distribution)
row = 1
movables = []
for letter in rack:
    movables.append(MovingWidget(letter, row*30+400, 0))
    
movables[-1].getBoard()

root.mainloop()
