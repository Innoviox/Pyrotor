#def print(*args, **kwargs):pass #print-suppresser
"""
Ok. Here's how it works.
Let's take a sample board and a sample rack:

	----------------------------------------------------------------
	|  | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
	----------------------------------------------------------------
	|01|TWS|   |   |DLS|   |   |   |TWS|   |   |   |DLS|   |   |TWS|
	----------------------------------------------------------------
	|02|   |DWS|   |   |   |TLS|   |   |   |TLS|   |   |   |DWS|   |
	----------------------------------------------------------------
	|03|   |   |DWS|   |   |   |DLS|   |DLS|   |   |   |DWS|   |   |
	----------------------------------------------------------------
	|04|DLS|   |   |DWS|   |   |   |DLS|   |   |   |DWS|   |   |DLS|
	----------------------------------------------------------------
	|05|   |   |   |   |DWS|   |   |   |   |   |DWS|   |   |   |   |
	----------------------------------------------------------------
	|06|   |TLS|   |   |   |TLS|   |   |   |TLS|   |   |   |TLS|   |
	----------------------------------------------------------------
	|07|   |   |DLS|   |   |   |DLS|   |DLS|   |   |   |DLS|   |   |
	----------------------------------------------------------------
	|08|TWS|   |   |DLS|   |   |   | R | A | D | I | C | A | L |TWS|
	----------------------------------------------------------------
	|09|   |   |DLS|   |   |   |DLS|   |DLS|   |   |   |DLS|   |   |
	----------------------------------------------------------------
	|10|   |TLS|   |   |   |TLS|   |   |   |TLS|   |   |   |TLS|   |
	----------------------------------------------------------------
	|11|   |   |   |   |DWS|   |   |   |   |   |DWS|   |   |   |   |
	----------------------------------------------------------------
	|12|DLS|   |   |DWS|   |   |   |DLS|   |   |   |DWS|   |   |DLS|
	----------------------------------------------------------------
	|13|   |   |DWS|   |   |   |DLS|   |DLS|   |   |   |DWS|   |   |
	----------------------------------------------------------------
	|14|   |DWS|   |   |   |TLS|   |   |   |TLS|   |   |   |DWS|   |
	----------------------------------------------------------------
	|15|TWS|   |   |DLS|   |   |   |TWS|   |   |   |DLS|   |   |TWS|
	----------------------------------------------------------------

With a rack:

	['A', 'M', 'A', 'Z', 'I', 'N', 'G']
	
Steps:

1)  Find all words on rack. This is done with cpu.CPU.gacc, which stands for getAllCorrectCombinations, using itertools.permutations. Pretty simple.
2)  Get all the positions to play at. This takes all the places on the board, in utils.board.getPlaces, and uses all of the points adjacent to it.
2a) If there are no tiles on the board, simply add all tiles in the 8th row and 8th column.
3)  Loop through all the points to play at, all of the words, and the directions (Across, 'A', and Down, 'D').  For each play, check if it's a valid play, then yield it.
4) 


How to check if a play is valid:
1) Get the words on the board. This is done in utils.board.getWords.
	Each word is represented as a collections.orderedDict object. 
	Each key-value pair is letter: (row, column).
	For the board this is the list that is returned:

		[OrderedDict([('R', (8, 8)), ('A', (8, 9)), ('D', (8, 10)), ('I', (8, 11)), ('C', (8, 12)), ('A1', (8, 13)), ('L', (8, 14))])]





"""
def call(func):
    def inner(*args, **kwargs):
        print("calling {}".format(func.__name__))
        return func(*args)
    return inner



from .blueprint import *
from utils import *
import sys

class CPU():
    def __init__(self, strategy=BlueprintBase):
        self.board = Board()
        
        self.rack = []
        self.distribution = distribution[:]
        self.drawTiles()
            
        self.checkWord = self.board.checkWord
        self.extraList = self.board.extraList

        self.score = 0

        self.BlueprintCreator = strategy
        
        self.name = "CPU"

    def drawTiles(self):
        while len(self.rack)<7 and len(self.distribution)>0:
            letter = random.choice(self.distribution)
            self.rack.append(letter.upper())
            self.distribution.remove(letter)
    
    def gacc(self, iterable, maxDepth):
        for word in self.gac(iterable, maxDepth):
            if self.checkWord(word):
                yield word
    
    def displayBoard(self, board):
        s="{bar}\n{sep}\n".format(bar="|",sep="-"*66)
        text=s+s.join(''.join('|'+c.center(4 if j == 0 else 3) for j, c in enumerate(r)) for r in board) + s
        text = text[2:-1]
        print(text)
        return text

    def generate(self):
        prevBoard = self.rNab()
        words = self.board.removeDuplicates(self.gacc(self.rack, len(self.rack)))
        places = self.board.getPlaces(self.board.board)
        plays = []
        neighbors = []

        if places == []:
            for i in range(1, 15):
                places.append((i, 8))
                places.append((8, i))
        across, down = [], []
        for place in places:
            r, c = place
            neighbors.append((r+1,c))
            neighbors.append((r-1,c))
            neighbors.append((r,c+1))
            neighbors.append((r,c-1))
        neighbors = self.board.removeDuplicates(neighbors)
        for word in words:
            for neighbor in neighbors:
                rIndex, cIndex = neighbor
                for direc in ['A', 'D']:
                    newBoard = self.rNab()
                    if self.playWord(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard, self.rack)
                        yield play
                        continue
                        
                    newBoard = self.rNab()
                    if self.playWordOpp(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard, self.rack, revWordWhenScoring=False)
                        yield play

        words = self.board.removeDuplicates(self.gac(self.rack, 7))
        for (d, row) in enumerate(self.board.board[1:]):
            yield from self.complete(self.slotify(row[1:]), 'A', d+1, words)
            
        for (d, col) in enumerate([[row[i] for row in self.board.board[1:]] for i in range(len(self.board.board))]):
            yield from self.complete(self.slotify(col), 'D', d, words)

    def proxyBoard(self):
        return Board(copy.deepcopy(self.board.board))

    def playWord(self, word, row, col, direc, board):
        for letter in reversed(word):
            if row>15 or col>15:
                return False
            if board.board[row][col] in string.ascii_uppercase:
                return False
            board.board[row][col] = letter
            if direc=='A':
                col -= 1
            else:
                row -= 1
        if board.checkBoard(board.board):
            return True
        return False

    def playWordOpp(self, word, row, col, direc, board, skip=False):
        for letter in word:
            if row>15 or col>15:
                return False
            if board.board[row][col] in string.ascii_uppercase:
                return False
            board.board[row][col] = letter
            if direc=='A':
                col += 1
            else:
                row += 1
        if board.checkBoard(board.board):
            return True
        return False
    
    def rNab(self):
        return Board([[col for col in row] for row in self.board.board])

    def gac(self, iterable, maxDepth):
        for depth in range(1, maxDepth + 1): 
            for word in itertools.permutations(iterable, depth):
                yield ''.join(word)
    
    def place(self, slot, pos, word, direc, depth):
        slot, reps = slot
        currPos = pos
        slot = list(slot)

        index = wordPos = 0
        while index < len(word):
            newPos = currPos + index
            if newPos>=len(slot):
                return False
            if slot[newPos] != '.':
                currPos += 1
                index -= 1
            else:
                slot[newPos] = word[index]
                if not wordPos:
                    wordPos = currPos+index
            index += 1
        wordPos += 1
        slot = ''.join(slot)

        if not all(map(self.checkWord, slot.strip('.').split('.'))):
            return False

        newBoardSlot = [reps[index] if newLetter == '.' else newLetter for (index, newLetter) in enumerate(slot)]
        newBoard = self.rNab()
        if direc == 'A':
            newBoard.board[depth][1:] = newBoardSlot[:]
            col = wordPos
            row = depth
        else:
            for (index, row) in enumerate(newBoard.board[1:]):
                row[depth] = newBoardSlot[index]
            col = depth
            row = wordPos
        move = Move(word, newBoard, row, col, direc, self.rNab(), self.rack, doNotScoreWord=True)
        if move.board.checkBoard(newBoard.board):
            move.getScore()
            move.getEvaluation(move.rack)
            return move
        return False
        
    def complete(self, slot, direc, depth, words):
        if depth==0:
            return []
        newSlots = []
        slotForLen = slot[0]
        if slotForLen != '...............':
            edgeFinder = [i[0] for i in enumerate(slotForLen) if i[1] !='.']
            for word in words:
                for pos in range(edgeFinder[0], edgeFinder[-1]+len(word)+2):
                    if pos-len(word) in range(len(slotForLen)):
                        if slotForLen[pos-len(word)] == '.':
                            yield self.place(slot, pos-len(word), word, direc, depth)

        #return newSlots

    def slotify(self, slot):
        slotForReps = slot
        slot = ''.join(i for i in slot)
        slot = slot.replace(' ', '.')
        for i in self.extraList:
            slot = slot.replace(i, '.')
        #print(slot)
        return slot, slotForReps


    def exchange(self):
        if len(distribution)<7:
            return []
        exchs = self.gac(self.rack, len(self.rack))
        for i in exchs:
            exch = Move(i, self.board, 0, 0, 0, self.board, self.rack, _type = 'e')
            exch.score = 0
            exch.getEvaluation(self.rack)
            yield exch

    def _run(self, file=sys.stdout):
        if file is not sys.stdout:
            file = open(file, "w")
        strategy = self.BlueprintCreator(self.generate(), self.rack)
        b = strategy.pick()
        t='p'
        
        if b is None:
            strategy.setMoves(self.exchange())
            b = strategy.pick()
            t='e'
            
        if b is None:
            print('I must pass...')
            return False
        
        if t != 'e':
            s = skips_formatted(b)
            print(s, file=file)
            print(b.row, b.col, file=file)
            print(b.score, b.valuation, file=file)
            
            self.board = b.board
            self.score += b.score
        else:
            print('Exchanging: {}\nValuation: {}'.format(b.word, b.valuation), file=file)

        for i in b.word:
            try:
                self.rack.remove(i)
            except:
                pass
        if file is not sys.stdout:
            print(self.displayBoard(self.board.board), file=file)
        else:
            self.displayBoard(self.board.board)
        self.drawTiles()
        return b

        
#unoptimized 1: [1.265223413996864, 3.3181498589983676, 6.187262326013297, 15.610297638981137, 11.20657178098918, 12.085041426995303, 19.933482533990173, 11.703756713977782, 11.809690213995054, 19.07466845199815, 23.55593549797777, 25.44604094600072]
#unoptimized 2: [2.747440225997707, 8.259836661018198, 10.411048979993211, 4.2886343720019795, 6.342490005976288, 4.577497259015217, 12.975426388991764, 10.519884257984813, 11.847122590988874, 33.74615316497511, 22.835890852991724, 33.31392122301622]
#unoptimized 3: [0.765806123992661, 6.166275091993157, 7.858307157992385, 12.531746090011438, 9.574502478993963, 19.63452962198062, 18.69206987900543, 12.540515913016861, 13.480751961003989, 16.363495366997086, 4.436360361985862, 15.09462254299433]
#12.78334581602313
#optimized1  1: [1.665996327996254, 7.3778611320012715, 11.375762982992455, 2.9555456250091083, 4.974553312000353, 9.928192778024822, 7.631045920017641, 11.769443914003205, 13.565904060000321, 18.685287929023616, 19.486449793999782, 16.662063413998112]
#optimized1  2: [1.74913569400087, 7.473322498000925, 12.628520960977767, 4.9739597710140515, 14.49849371999153, 13.32051673901151, 20.283806324005127, 8.142356403986923, 16.22037523498875, 22.071941621019505, 12.094354822009336, 9.727558161976049]
#optimized1  3: [1.5485639690014068, 3.9073374739964493, 6.62486044500838, 6.343475920992205, 2.6210223180241883, 8.699827930016909, 11.358580372005235, 23.01152083699708, 24.981908791000023, 8.391618594992906, 17.091218812012812, 8.808330937026767]
#optimized1  4: [0.8331756230036262, 3.6176393469795585, 6.975504544010619, 10.809455045004142, 7.3936960870050825, 10.150695773016196, 22.273985980980797, 6.687757364008576, 8.724490929977037, 29.298748324014014, 4.558691303012893, 14.576253092003753]
#10.80314185321125
#optimized2  1: [1.2783712660020683, 4.249000264011556, 4.514386737981113, 4.865409799007466, 9.679090443009045, 6.282409895997262, 3.3017842389817815, 18.261759247019654, 8.83863319599186, 21.465678223001305, 13.255115537001984, 19.390510562021518]
#optimized2  2: [0.9049904700077605, 2.0015377280069515, 4.282056188996648, 5.481174947984982, 6.726537792972522, 7.307185123005183, 14.644356150995009, 9.006248919991776, 17.457672567019472, 26.309426841995446, 8.991929311014246, 23.584705193003174]
#optimized2  3: [1.452723626018269, 3.4530001710227225, 2.5678244750015438, 9.060929650993785, 4.948611400992377, 6.2725813839933835, 14.724158021999756, 13.372502509999322, 9.666142661008053, 5.119453541992698, 7.95828937200713, 16.36855056299828]
#9.36235383397353
#optimized3  1: 
#optimized3  2:
#optimized3  3: 
