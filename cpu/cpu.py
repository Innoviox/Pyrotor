#def print(*args, **kwargs):pass #print-suppresser
def call(func):
    def inner(*args, **kwargs):
        print("calling {}".format(func.__name__))
        return func(*args, **kwargs)
    return inner



from .blueprint import BlueprintBase
from .utils import Move, Board, distribution, skips_formatted, insert
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

    def generate_checked(self):
        self.strategy = strategy = self.BlueprintCreator(self.generate(), self.rack, *self.bl_args)
        best = None
        bestScore = 0
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
            neighbors.append((r + 1, c))
            neighbors.append((r - 1, c))
            neighbors.append((r, c + 1))
            neighbors.append((r, c - 1))
        neighbors = self.board.removeDuplicates(neighbors)
        for word in words:
            for neighbor in neighbors:
                rIndex, cIndex = neighbor
                for direc in ['A', 'D']:
                    newBoard = self.board.clone()
                    if self.playWord(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard, self.rack)
                        play.getScore()
                        play.getEvaluation(self.rack)
                        s = strategy.score(play)
                        if bestScore < s:
                            best = play
                            bestScore = s
                        #yield play
                        continue

                    newBoard = self.board.clone()
                    if self.playWordOpp(word, rIndex, cIndex, direc, newBoard):
                        play = Move(word, newBoard, rIndex, cIndex, direc, prevBoard, self.rack,
                                    revWordWhenScoring=False)
                        play.getScore()
                        play.getEvaluation(self.rack)
                        s = strategy.score(play)
                        if bestScore < s:
                            best = play
                            bestScore = s
                        #yield play

        words = self.board.removeDuplicates(self.gac(self.rack, 7))
        for (d, row) in enumerate(self.board.board[1:]):
            for move in self.complete(self.slotify(row[1:]), 'A', d + 1, words):
                s = strategy.score(play)
                if bestScore < s:
                    best = play
                    bestScore = s

        for (d, col) in enumerate([[row[i] for row in self.board.board[1:]] for i in range(len(self.board.board))]):
            for move in self.complete(self.slotify(col), 'D', d, words):
                s = strategy.score(play)
                if bestScore < s:
                    best = play
                    bestScore = s
        return best

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

    def insert(self, s, pos, word):
        slot, reps = s
        idx = w_pos = 0
        for p in range(pos, 15):
            if slot[p] == '.':
                slot = slot[:p] + word[w_pos] + slot[p + 1:]
                w_pos += 1
                if not idx:
                    idx = p + 1
                if w_pos == len(word):
                    return slot, reps, idx
        return False

    def place(self, slot, pos, word, direc, depth):
        i = self.insert(slot, pos, word)
        if i:
            slot, reps, wordPos = i
        else:
            return False

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
            edgeFinder = [i for i, j in enumerate(slotForLen) if j != '.']
            for word in words:
                l = len(word)
                for pos in range(edgeFinder[0], edgeFinder[-1]+l+2):
                    if pos-l in range(15):
                        if slotForLen[pos-l] == '.':
                            yield self.place(slot, pos-l, word, direc, depth)

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

    def pick_n(self, n):
        self.strategy = strategy = self.BlueprintCreator(self.generate(), self.rack, *self.bl_args)
        return strategy.pick_n(n)

    def pick_iter(self):
        self.strategy = strategy = self.BlueprintCreator(self.generate(), self.rack, *self.bl_args)
        return strategy.pick_iter()

    def run(self, file=sys.stdout):
        if file is not sys.stdout:
            file = open(file, "w")
        self.strategy = strategy = self.BlueprintCreator(self.generate(), self.rack, *self.bl_args)
        b = strategy.pick()
        #b = self.generate_checked()
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