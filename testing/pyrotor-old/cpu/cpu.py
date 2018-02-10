#def print(*args, **kwargs):pass #print-suppresser
def call(func):
    def inner(*args, **kwargs):
        print("calling {}".format(func.__name__))
        return func(*args, **kwargs)
    return inner



from .blueprint import BlueprintBase
from .utils import Move, Board, distribution, skips_formatted
import random, string, itertools, sys, copy

class CPU():
    def __init__(self, strategy=BlueprintBase, bl_args=[]):
        self.board = Board()
        
        self.rack = []
        self.distribution = distribution[:]
        self.drawTiles()
            
        self.checkWord = self.board.checkWord
        self.extraList = self.board.extraList

        self.score = 0

        self.BlueprintCreator = strategy
        self.bl_args = bl_args
        self.strategy = None
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
        prevBoard = self.board.clone()
        words = self.board.removeDuplicates(self.gacc(self.rack, len(self.rack)))
        places = self.board.getPlaces(self.board.board)
        neighbors = []

        if not places:
            for i in range(1, 15):
                places.append((i, 8))
                places.append((8, i))
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
                    newBoard = self.board.clone()
                    if self.playWord(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard, self.rack)
                        yield play
                        continue
                        
                    newBoard = self.board.clone()
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
                #cc = (depth, currPos) if direc == 'A' else (currPos, depth)
                #if word[index] not in self.board.crosschecks[cc[0]][cc[1]]: return False
                slot[newPos] = word[index]
                if not wordPos:
                    wordPos = currPos+index
            index += 1
        wordPos += 1
        slot = ''.join(slot)

        if not all(map(self.checkWord, slot.strip('.').split('.'))):
            return False

        newBoardSlot = [reps[index] if newLetter == '.' else newLetter for (index, newLetter) in enumerate(slot)]
        newBoard = self.board.clone()
        if direc == 'A':
            newBoard.board[depth][1:] = newBoardSlot[:]
            col = wordPos
            row = depth
        else:
            for (index, row) in enumerate(newBoard.board[1:]):
                row[depth] = newBoardSlot[index]
            col = depth
            row = wordPos
        move = Move(word, newBoard, row, col, direc, self.board.clone(), self.rack, doNotScoreWord=True)
        if move.board.checkBoard(newBoard.board):
            move.getScore()
            move.getEvaluation(move.rack)
            return move
        return False
        
    def complete(self, slot, direc, depth, words):
        if depth==0:
            return []
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

    def run(self, file=sys.stdout):
        if file is not sys.stdout:
            file = open(file, "w")
        self.strategy = strategy = self.BlueprintCreator(self.generate(), self.rack, *self.bl_args)
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