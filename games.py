from cpu import *

class Game():
    def __init__(self, name1, name2, mode1, mode2):
         self.mainRoot = Tk()
         self.root = Toplevel(self.mainRoot)
         self.root2 = Toplevel(self.mainRoot)
         self.mainRoot.withdraw()

         self.name1 = name1
         self.name2 = name2
         self.mode1 = mode1[0]
         self.mode2 = mode2[0]

         self.gameNum = -1
         self.gameAlreadyInFile = False
         
    def startGame(self):
        self.player1 = Player(self.root, 1, self.name1, 150, 550, self.mode1, self.mode2, [])
        if self.name2 == "CPU":
            self.player2 = CPU(self.root2, [])
        else:
            self.player2 = Player(self.root2, 2, self.name2, 150, 550, self.mode1, self.mode2, [])
        self.player1.otherName = self.name2
        self.player2.otherName = self.name1
        self.playerGoing = 1
        
    def doTurn(self):
        print(self.name2)
        if self.playerGoing == 1:
            self.root1 = Toplevel(self.mainRoot)
            self.player1.reRoot(self.root1)
            self.player1.startTurn(self.player2.name, self.player2.score)
            self.player2.board = self.player1.board
            self.playerGoing = 2
            popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player2.name, 500, 500)
        else:
            if self.player2.name == "CPU":
                self.playerGoing = 1
                self.player2.takeTurn()
                self.player2.turnrotation = 0
                self.player1.board = self.player2.board
            else:
                self.root2 = Toplevel(self.mainRoot)
                self.player2.reRoot(self.root2)
                self.player2.startTurn(self.player1.name, self.player1.score)
                self.player1.board = self.player2.board
                self.playerGoing = 1
                popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player1.name, 500, 500)
        if self.gameAlreadyInFile is False:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = False)
            self.gameAlreadyInFile = True
        else:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = True)
            
    def main(self):
        #self.startGame()
        if self.mode2.lower() == "n":
            while len(distribution) > 0 or (len(self.player1.rack) > 0 and len(self.player2.rack) > 0):
                self.doTurn()
                #self.updateScores()
        else:
            while self.player1.score < 75 and self.player2.score < 75:
                self.doTurn()
                #self.updateScores()
        if self.player1.score > self.player2.score:
            popup(root, "Player 1 Won", "Player 1 Won", self.player1.screenHeight, self.player1.screenWidth)
        else:
            popup(root, "Player 2 Won", "Player 2 Won", self.player1.screenHeight, self.player1.screenWidth)
        self.player1.root.destroy()
        self.player2.root.destroy()
        self.mainRoot.destroy()


class GameWithCPU(Game):
    def __init__(self, name1, mode1, mode2, name2="CPU"):
        super(GameWithCPU, self).__init__(name1, name2, mode1, mode2)
        
    def startGame(self):
        self.player1 = Player(self.root, 1, self.name1, 150, 550, self.mode1, self.mode2, [])
        self.player2= CPU(self.root, [])
        self.player1.otherName = self.name2
        self.player2.otherName = self.name1
        self.playerGoing = 1
        
    def doTurn(self):
        if self.playerGoing == 1:
            self.root1 = Toplevel(self.mainRoot)
            self.player1.reRoot(self.root1)
            self.player1.startTurn(self.player2.name, self.player2.score)
            self.player2.board = self.player1.board
            self.playerGoing = 2
            #popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player2.name, 500, 500)
        else:
            self.playerGoing = 1
            self.player2.takeTurn()
            self.player2.turnrotation = 0
            self.player1.board = self.player2.board
        if self.gameAlreadyInFile is False:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = False)
            self.gameAlreadyInFile = True
        else:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = True)
            
    def main(self):
        #self.startGame()
        if self.mode2.lower() == "n":
            while len(distribution) > 0 or (len(self.player1.rack) > 0 and len(self.player2.rack) > 0):
                self.doTurn()
                #self.updateScores()
        else:
            while self.player1.score < 75 and self.player2.score < 75:
                self.doTurn()
                #self.updateScores()
        if self.player1.score > self.player2.score:
            popup(root, "Player 1 Won", "Player 1 Won", self.player1.screenHeight, self.player1.screenWidth)
        else:
            popup(root, "Player 2 Won", "Player 2 Won", self.player1.screenHeight, self.player1.screenWidth)
        self.player1.root.destroy()
        self.player2.root.destroy()
        self.mainRoot.destroy()
###############End of class definitions.###############
        
###############Start of algorithms for saving games: SavedGame, writeVars, writeAllGames, writeGameToFile, setFileTextToList, playSavedGame.###############
class SavedGame(Game):
    def __init__(self, root, file="savedGame.txt"):
        self.root = Toplevel(root)
        self.root.withdraw()
        self.gameWindow = Toplevel(self.root, height = root.winfo_screenheight(), width = root.winfo_screenwidth())
        self.gameWindow.resizable(0,0)
        self.gameWindow.wm_title("Saved Games")
        gameTexts = open(file).read()
        gameTexts = gameTexts.split("New Game\n")
        newGameTexts = []
        for i in gameTexts:
            newGameTexts.append(i.strip())
        #print(gameTexts)
        self.gameTexts = newGameTexts
        gameLabels = []
        gameButtons = []
        deleteButtons = []
        column = 0
        for gameText in gameTexts:
            if gameText:
                fullText = self.setGameVars(gameText)
                if fullText != "nogame":
                    text = """%s's score: %s
        %s's score: %s
        Mode 1: %s
        Mode 2: %s""" % (fullText[0], fullText[1], fullText[2], fullText[3], fullText[4], fullText[5])
                    gameLabel = Label(self.gameWindow, text=text, height=4, width=20, relief=RAISED) #Definetly changeable
                    gameLabels.append(gameLabel)
                    gameLabels[-1].place(x=0, y=column * 100)
                    
                    gameButton = Button(self.gameWindow, text="Play!", height=1, width=5, \
                                        command=lambda game=gameText: self.play(game))
                    gameButtons.append(gameButton)
                    gameButtons[-1].place(x=350, y=(gameTexts.index(gameText)*100))

                    column += 1
    def setGameVars(self, gameText):
        if "|" in gameText:
            #print(gameText)
            gameText = gameText.split("\n")
            if gameText[0] == "New Game":
                del gameText[0]
            #print(gameText)
            p1Atts = gameText[0].split()
            p2Atts = gameText[1].split()
            score1, score2 = p1Atts[-1], p2Atts[-1]
            del p1Atts[-1]
            del p2Atts[-1]
            name1 = ""
            for namePiece in p1Atts:
                name1 += namePiece
                name1 += " "
            name1 = name1.strip()
            
            name2 = ""
            for namePiece in p2Atts:
                name2 += namePiece
                name2 += " "
            name2 = name2.strip()
            
            tiles = gameText[2].split(",")
            if tiles[-1] == "":
                del tiles[-1]
                
            modes = gameText[3].split()
            
            if modes[0] == "n":
                    mode1 = "normal"
            else:
                    mode1 = "hardcore"
            
            if modes[1] == "n":
                    mode2 = "normal"
            else:
                    mode2 = "short"
            playerGoing = int(modes[2])
            rack1 = list(gameText[4])
            rack2 = list(gameText[5])
            
            del gameText[:6]
            
            board = []
            currentRowIndex = 0
            for row in gameText:
                    board.append([])
                    parse = row.split("|")
                    for column in parse:
                            board[currentRowIndex].append(column)
                    del board[currentRowIndex][-1]
                    currentRowIndex += 1
            del board[-1]
            return name1, score1, name2, score2, mode1, mode2, board, rack1, rack2, playerGoing, tiles
        else:
            return "nogame"
    def play(self, gameText):
        global playing
        playing = 1

        self.gameNum = -1 #self.gameTexts.index(gameText)
        self.gameAlreadyInFile = True
        gameVars = self.setGameVars(gameText)
        global distribution
        distribution = gameVars[10]
        #print(distribution)
        popup(root, "Pass Device", "Pass Device to %s\n\n" % [gameVars[0], gameVars[2]][gameVars[9]-1], 500, 500)
        super(SavedGame, self).__init__(gameVars[0], gameVars[2], gameVars[4], gameVars[5])
        self.gameWindow.destroy()
        self.startGame(gameVars[7], gameVars[8])
        self.player1.board, self.player2.board = gameVars[6], gameVars[6]
        self.player1.score, self.player2.score = int(gameVars[1]), int(gameVars[3])
        #self.player1.rack, self.player2.rack = gameVars[7], gameVars[8]
        self.playerGoing = gameVars[9]
        self.main()
        playing = 0
        
    def startGame(self, rack1, rack2):
        self.player1 = Player(self.root, 1, self.name1, 150, 550, self.mode1, self.mode2, rack1)
        if self.name2 == "CPU":
            self.player2 = CPU(self.root2, [])
        else:
            self.player2 = Player(self.root2, 2, self.name2, 150, 550, self.mode1, self.mode2, [])
        self.playerGoing = 1
        
    def updateScores(self):
        super(SavedGame, self).updateScores()
        
    def doTurn(self):
        super(SavedGame, self).doTurn()
        
    def main(self):
        super(SavedGame, self).main()
