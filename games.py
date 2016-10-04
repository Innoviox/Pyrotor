import cpu
import player
import functions as func

class Game():
    def __init__(self, name1, name2, mode1, mode2):
         self.mainRoot = func.Tk()
         self.root = func.Toplevel(self.mainRoot)
         self.root2 = func.Toplevel(self.mainRoot)
         self.mainRoot.withdraw()

         self.name1 = name1
         self.name2 = name2
         self.mode1 = mode1[0]
         self.mode2 = mode2[0]

         self.gameNum = -1
         self.gameAlreadyInFile = False
         
    def startGame(self):
        self.player1 = player.Player(self.root, 1, self.name1, 150, 550, self.mode1, self.mode2, [], ())
        if self.name2 == "CPU":
            self.player2 = cpu.CPU(self.root2, [])
        else:
            self.player2 = player.Player(self.root2, 2, self.name2, 150, 550, self.mode1, self.mode2, [], ())
        self.player1.otherName = self.name2
        self.player2.otherName = self.name1
        self.playerGoing = 1
    def doTurn(self):
        if self.playerGoing == 1:
            self.root1 = func.Toplevel(self.mainRoot)
            self.player1.reRoot(self.root1)
            self.player1.startTurn(self.player2.name, self.player2.score)
            self.player2.board = self.player1.board
            self.playerGoing = 2
            func.popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player2.name, 500, 500)
        else:
            if self.player2.name == "CPU":
                self.playerGoing = 1
                self.player2.takeTurn()
                self.player2.turnrotation = 0
                self.player1.board = self.player2.board
            else:
                self.root2 = func.Toplevel(self.mainRoot)
                self.player2.reRoot(self.root2)
                self.player2.startTurn(self.player1.name, self.player1.score)
                self.player1.board = self.player2.board
                self.playerGoing = 1
                func.popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player1.name, 500, 500)
        if self.gameAlreadyInFile is False:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = False)
            self.gameAlreadyInFile = True
        else:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = True)
            
    def main(self):
        #self.startGame()
        if self.mode2.lower() == "n":
            if self.player1.distribution:
                while len(self.player1.distribution) > 0 or (len(self.player1.rack) > 0 and len(self.player2.rack) > 0):
                    self.doTurn()
                    #self.updateScores()
            else:
                while len(func.distribution) > 0 or (len(self.player1.rack) > 0 and len(self.player2.rack) > 0):
                    self.doTurn()
                    #self.updateScores()
        else:
            while self.player1.score < 75 and self.player2.score < 75:
                self.doTurn()
                #self.updateScores()
        if self.player1.score > self.player2.score:
            func.popup(func.root, "Player 1 Won", "Player 1 Won", self.player1.screenHeight, self.player1.screenWidth)
        else:
            func.popup(func.root, "Player 2 Won", "Player 2 Won", self.player1.screenHeight, self.player1.screenWidth)
        self.player1.root.destroy()
        self.player2.root.destroy()
        self.mainRoot.destroy()


        
        
class GameWithCPU(Game):
    def __init__(self, name1, mode1, mode2, name2="CPU"):
        super(GameWithCPU, self).__init__(name1, name2, mode1, mode2)
        
    def startGame(self):
        self.player1 = player.Player(self.root, 1, self.name1, 150, 550, self.mode1, self.mode2, [], ())
        self.player2= cpu.CPU(self.root, [], ())
        self.player1.otherName = self.name2
        self.player2.otherName = self.name1
        self.playerGoing = 1

    def doTurn(self):
        if self.playerGoing == 1:
            self.root1 = func.Toplevel(self.mainRoot)
            self.player1.reRoot(self.root1)
            self.player1.startTurn(self.player2.name, self.player2.score)
            self.player2.board = self.player1.board
            self.playerGoing = 2
            #func.popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player2.name, 500, 500)
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
            if self.player1.distribution:
                while len(self.player1.distribution) > 0 or (len(self.player1.rack) > 0 and len(self.player2.rack) > 0):
                    self.doTurn()
                    #self.updateScores()
            else:
                while len(func.distribution) > 0 or (len(self.player1.rack) > 0 and len(self.player2.rack) > 0):
                    self.doTurn()
                    #self.updateScores()
        else:
            while self.player1.score < 75 and self.player2.score < 75:
                self.doTurn()
                #self.updateScores()
        if self.player1.score > self.player2.score:
            func.popup(func.root, "Player 1 Won", "Player 1 Won", self.player1.screenHeight, self.player1.screenWidth)
        else:
            func.popup(func.root, "Player 2 Won", "Player 2 Won", self.player1.screenHeight, self.player1.screenWidth)
        self.player1.root.destroy()
        self.player2.root.destroy()
        self.mainRoot.destroy()
###############End of class definitions.###############
        
###############Start of algorithms for saving games: SavedGame, writeVars, writeAllGames, writeGameToFile, setFileTextToList, playSavedGame.###############


class SavedGame(Game):
    def __init__(self, root, file="savedGame.txt"):
        self.root = func.Toplevel(root)
        self.root.withdraw()
        self.gameWindow = func.Toplevel(self.root, height = root.winfo_screenheight(), width = root.winfo_screenwidth())
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
                    gameLabel = func.Label(self.gameWindow, text=text, height=4, width=20, relief=func.RAISED) #Definetly changeable
                    gameLabels.append(gameLabel)
                    gameLabels[-1].place(x=0, y=column * 100)
                    
                    gameButton = func.Button(self.gameWindow, text="Play!", height=1, width=5, \
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
        distribution = getDist()
        #distribution = gameVars[10]#.split(",")
        self.distribution = distribution
        print(self.distribution)
        #print(distribution)
        func.popup(func.root, "Pass Device", "Pass Device to %s\n\n" % [gameVars[0], gameVars[2]][gameVars[9]-1], 500, 500)
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
        print(type(self.distribution))
        self.player1 = player.Player(self.root, 1, self.name1, 150, 550, self.mode1, self.mode2, rack1, self.distribution)
        if self.name2 == "CPU":
            self.player2 = cpu.CPU(self.root2, rack2, self.distribution)
        else:
            self.player2 = player.Player(self.root2, 2, self.name2, 150, 550, self.mode1, self.mode2, rack2, self.distribution)
        self.playerGoing = 1
        
    def updateScores(self):
        super(SavedGame, self).updateScores()
        
    def doTurn(self):
        if self.playerGoing == 1:
            self.root1 = func.Toplevel(self.mainRoot)
            self.player1.reRoot(self.root1)
            self.player1.startTurn(self.player2.name, self.player2.score)
            self.player2.board = self.player1.board
            self.playerGoing = 2
            func.popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player2.name, 500, 500)
            self.player2.distribution = self.player1.distribution
        else:
            if self.player2.name == "CPU":
                self.playerGoing = 1
                self.player2.takeTurn()
                self.player2.turnrotation = 0
                self.player1.board = self.player2.board
            else:
                self.root2 = func.Toplevel(self.mainRoot)
                self.player2.reRoot(self.root2)
                self.player2.startTurn(self.player1.name, self.player1.score)
                self.player1.board = self.player2.board
                self.playerGoing = 1
                func.popup(self.mainRoot, "Pass Device", "Pass Device to %s\n\n" % self.player1.name, 500, 500)
            self.player1.distribution = self.player2.distribution
        if self.gameAlreadyInFile is False:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = False)
            self.gameAlreadyInFile = True
        else:
            writeGameToFile(self, gameNum = self.gameNum, gameAlreadyInFile = True)

    def main(self):
        super(SavedGame, self).main()   
        
def getDist(file="savedGame.txt"):
    h = open(file).read().split("\n")
    dist = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l",    "l", "l", "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r", "r", "r","s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", "v", "v", "w", "w", "x", "y", "y", "z"]
    q = open(file).read().split()
    r1, r2 = q[10], q[11]
    print(dist)
    h = h[14:]
    g = []
    for i in h:
        g.append(i.split("|"))
    #print("" in func.ascii_uppercase)
    for j in g:
        for k in j:
            #print(k)
            if k in func.ascii_uppercase and k != "":
                #print(func.ascii_uppercase)
                #print(k)
                dist.remove(k.lower())
    for r in [r1, r2]:
        for l in r:
            dist.remove(l.lower())
        
    #print(g)
    print(dist, len(dist))
    return dist
def playSavedGame(file="savedGame.txt"):
    
    if len(open(file).read()) > 0:
        playing = 1
        global scrabble
        scrabble = SavedGame(func.root)
        playing = 0
    else:
        func.popup(func.root, "No saved games", "No saved games\n\n\n", root.winfo_screenheight(), root.winfo_screenwidth())
        
def writeVars(game, file):
    file.write("New Game\n")
    
    file.write("%s %d\n" % (game.player1.name, game.player1.score))
    #file.write("%s %d\n" % (game.player2.name, game.player2.score))
    file.write("%s %d\n" % (game.player2.name, game.player2.score))
    if game.player1.distribution:
        for letter in game.player1.distribution:
            file.write(letter)
            file.write(",")
    else:
        for letter in func.distribution:
            file.write(letter)
            file.write(",")
    file.write("\n")
    file.write("%s %s %d\n" % (game.mode1, game.mode2, game.playerGoing))
    #print(len(distribution))
    game.player1.drawTiles()
    game.player2.drawTiles()
    #print(len(distribution))
    for letter in game.player1.rack:
        file.write(letter)
    file.write("\n")
    for letter in game.player2.rack:
        file.write(letter)
    file.write("\n")
    for row in [game.player1.board, game.player2.board][game.playerGoing-1]:
            for column in row:
                    file.write(column + "|")
            file.write("\n")
            
def setFileTextToList(newTextList, file="savedGame.txt"):
    with open(file, "w"):
        pass
    file = open(file, "w")
    for text in newTextList:
        file.write(text)
        file.write("\n")
        
def writeAllGames(games, file="savedGame.txt"):
    for game in games:
        writeGameToFile(game, gameNum = game.gameNum, gameAlreadyInFile = game.gameAlreadyInFile, file = file)
        
def writeGameToFile(game, gameNum = -1, gameAlreadyInFile = False, file="savedGame.txt"):
    if not gameAlreadyInFile:
        file = open(file, "w")
        writeVars(game, file)
    else:
        file = open(file, "r+")
        fileText = file.read().split("New Game\n")
        #print(fileText)
        text = "New Game\n"
        text += "%s %d\n%s %d\n" % (game.player1.name, game.player1.score, game.player2.name, game.player2.score)
        #print(len(distribution))
        if game.player1.distribution:
            for letter in game.player1.distribution:
                text += letter
                text += ","
        else:
            for letter in func.distribution:
                text += letter
                text += ","
        #print(len(distribution))
        text += "\n"
        text += "%s %s %d\n" % (game.mode1, game.mode2, game.playerGoing)
        game.player1.drawTiles()
        game.player2.drawTiles()
        for letter in game.player1.rack:
            text += letter
        text += "\n"
        for letter in game.player2.rack:
            text += letter
        text += "\n"
        for row in [game.player1.board, game.player2.board][game.playerGoing-1]:
            for column in row:
                text += column
                text += "|"
            text += "\n"
        #print(fileText, gameNum)
        fileText[gameNum] = text
        setFileTextToList(fileText)
if __name__ == "__main__":
    getDist()
