from tkinter import *

class blah:

    def startMoveWindow(self, event):
        ## When the movement starts, record current root coordinates
        self.__lastX, self.__lastY = event.x_root, event.y_root

    def MoveWindow(self, event):
        self.root.update_idletasks()
        ## Use root coordinates to compute offset for inside window coordinates
        self.__winX += event.x_root - self.__lastX
        self.__winY += event.y_root - self.__lastY
        ## Remember last coordinates
        self.__lastX, self.__lastY = event.x_root, event.y_root
        ## Move inside window
        self.f.place_configure(x=self.__winX, y=self.__winY)
 #       f1Position = [self.f.winfo_rootx(), self.f.winfo_rooty()]

        f1Position = [self.__winX, self.__winY]
        for labelPosition in self.labels_positionList:
            if self.isTouching(f1Position, labelPosition,
                               self.f.winfo_width(), self.f.winfo_height(),
                               25, 25):
                self.f.place_configure(x=labelPosition[0], y=labelPosition[1])
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


        self.root = Tk()
        self.root.title("...")
        self.root.resizable(0,0)
        self.root.geometry("%dx%d%+d%+d"%(640, 480, 0, 0))
        self.getBoard()
        ## Record coordinates for window to avoid asking them every time
        self.__winX, self.__winY = 0, 0
        self.f = Frame(self.root, bd=1, relief=SUNKEN)
        self.f.place(x=self.__winX, y=self.__winY, width=25, height=25)

        self.l = Label(self.f, bd=1, relief=RAISED, text="A", width=25)
        self.l.pack(fill=X, padx=1, pady=1)

        ## When the button is pressed, make sure we get the first coordinates
        self.l.bind('<ButtonPress-1>', self.startMoveWindow)
        self.l.bind('<B1-Motion>', self.MoveWindow)
        self.f.bind('<ButtonPress-1>', self.startMoveWindow)
        self.f.bind('<B1-Motion>', self.MoveWindow)

        self.root.mainloop()

x = blah()
