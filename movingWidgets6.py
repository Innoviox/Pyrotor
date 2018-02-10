class MovingWidget():
    def __init__(self, root, text, x, y):
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
        
        self.x = x
        self.y = y
        
        self.f = Frame(self.root, bd=1, relief=SUNKEN)
        self.f.place(x=self.x, y=self.y, width=25, height=25)

        self.l = Label(self.f, bd=1, relief=RAISED, text=text, width=25)
        self.l.pack(fill=X, padx=1, pady=1)

        self.l.bind('<ButtonPress-1>', self.startMoveWindow)
        self.l.bind('<B1-Motion>', self.MoveWindow)
        self.f.bind('<ButtonPress-1>', self.startMoveWindow)
        self.f.bind('<B1-Motion>', self.MoveWindow)
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
                #print(labelPosition[0], labelPosition[1])
                self.f.place_configure(x=labelPosition[0], y=labelPosition[1])
                self.hoveringOver = self.labels_positionList[(labelPosition[0], labelPosition[1])]
                #print(self.hoveringOver)
                #break
                self.hoveringOver_letter = self.board[self.hoveringOver[0]][self.hoveringOver[1]]
                #print(self.board[self.hoveringOver[0]][self.hoveringOver[1]])
##                self.x = labelPosition[0]
##                self.y = labelPosition[1]
        self.f.lift()
        #print(f1Position)
    def isTouching(self, position1, position2, width1, height1, width2, height2):
        #print(position1, position2, width1, height1, width2, height2)
##        if ((position1[0] > position2[0]) or (position1[0] + width1) > position2[0]) and \
##           ((position1[1] > position2[1]) or (position1[1] + height1) > position2[1]) and \
##           ((position1[0] < (position2[0] + width2)) and (position1[1] < (position2[1] + height2))):
##            return True
##        elif ((position2[0] > position1[0]) or (position2[0] + width2) > position1[0]) and \
##           ((position2[1] > position1[1]) or (position2[1] + height2) > position1[1]) and \
##            ((position2[0] < (position1[0] + width1)) and (position2[1] < position1[1] + height1)):
##            return True
##
##        else:
##            return False
        if ((position1[0] > position2[0]) or (position1[0] > (position2[0] + width1)))and \
           ((position1[1] > position2[1]) or (position1[1] > (position2[1] + height1))) and \
           ((position1[0] < (position2[0] + width2)) and (position1[1] < (position2[1] + height2))):
            #print(position1, position2)
            return True
        elif ((position2[0] > position1[0]) or (position2[0] > (position1[0] + width2))) and \
             ((position2[1] > position1[1]) or (position2[1] > (position1[1] + height2))) and \
             ((position2[0] < (position1[0] + width1)) and (position2[1] < (position1[1] + height1))):
            #print(position1, position2)
            return True
        else:
            return False
    def getPositions(self):
        self.labels_positionList = {}
        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                if not(label[0] == "0" or label[0] == "1" or label[0].isalpha()):
                    self.labels_positionList[((i*30)+2.5, (j*30)+2.5)] = (j, i)
##        print(self.labels_positionList.keys())
        for i in self.labels_positionList.keys():
            if i == (200,225):
                print(self.labels_positionList[i])
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
root.title("Moving Widgets Test...attempt 6 :)")
root.resizable(0,0)
root.geometry("%dx%d%+d%+d"%(550, 700, 0, 0))

rack = getRack(distribution)
row = 0
movables = []
for letter in rack:
    movables.append(MovingWidget(root, letter, row*30+150, 550))
    row += 1
    
movables[-1].getBoard()

root.mainloop()
