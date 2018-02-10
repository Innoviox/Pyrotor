from tkinter import *
import random
class scrabble:


    class moving:
        all = []
        def clamp(self, lo, hi, x):
            return min(max(x, lo), hi)
        def MoveWindowStart(self, event):
            self.move_lastx = event.x_root
            self.move_lasty = event.y_root
            self.focus()
        def MoveWindow(self, event):
            self.root.update_idletasks()
            dx = event.x_root - self.move_lastx
            dy = event.y_root - self.move_lasty
            self.move_lastx = event.x_root
            self.move_lasty = event.y_root
            self.x = self.clamp(0, 640-self.f.winfo_width(), self.x + dx)
            self.y = self.clamp(0, 480-self.f.winfo_height(), self.y + dy)
            self.f.place_configure(x=self.x, y=self.y)

            f1Position = [self.x, self.y]
            for labelPosition in self.labels_positionList:
                if self.isTouching(f1Position, labelPosition,
                                   self.f.winfo_width(), self.f.winfo_height(),
                                   25, 25):
                    self.f.place_configure(x=labelPosition[0], y=labelPosition[1])
                    break
    ##                #print("touching!")
    ##            #break
            self.f.lift()
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

        def getBoard(self):
            self.boardFrame = Frame(self.root, bd=1, relief=SUNKEN)
            self.boardFrame.place(x=0, y=0, width=450, height = 450)
            self.labels_positionList = []
            self.labels = list()
            self.squares = list()
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
                        self.labels.append(Label(entry, text = label,
                                            height = 25, width = 25))
                        self.labels[-1].pack()
    ##                    labels[-1].grid(row=i+1, column = j)
    ##                    self.labels_positionList.append([labels[-1].winfo_rootx(),
    ##                                                    labels[-1].winfo_rooty()])
                    else:
                        self.squares.append(Label(entry, text=label,
                                             height=25, width=25))
                        self.squares[-1].pack()
                        self.labels_positionList.append([(i*25), (j*25)])
                    
        def __init__(self, root, title, x, y):
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
            self.getBoard()
            self.x = x; self.y = y
            self.f = Frame(self.root, bd=1, relief=RAISED)
            self.f.place(x=x, y=y, width=25, height=25)

            self.l = Label(self.f, bd=1, bg="#08246b", fg="white",text=title, width = 25)
            self.l.pack(fill=X)

            self.l.bind('<ButtonPress-1>', self.MoveWindowStart)
            self.f.bind('<1>', self.focus)
            self.l.bind('<B1-Motion>', self.MoveWindow)
            # self.f.bind('<B1-Motion>', self.MoveWindow)
            self.all.append(self)
            self.focus()
            
        def focus(self, event=None):
            self.f.tkraise()
            for w in self.all:
                if w is self:
                    w.l.configure(bg="#08246b", fg="white")
                else:
                    w.l.configure(bg="#d9d9d9", fg="black")
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

    def getRack(self, distribution):
        rack = ['', '', '', '', '', '', '']
        for i in range(7):
            letter = random.choice(distribution).upper()
            rack[i] = letter
        return rack
    def __init__(self):          
        root = Tk()
        root.title("...")
        root.resizable(0,0)
        root.geometry("%dx%d%+d%+d"%(740, 480, 0, 0))

        self.rack = self.getRack(self.distribution)
        row = 1
        movables = []
        for letter in self.rack:
            movables.append(self.moving(root, letter, (row*30)+450, 10))
            row += 1

                    


        root.mainloop()
scrabble = scrabble()
