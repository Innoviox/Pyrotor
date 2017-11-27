import utils as u
import itertools as it

SPACE = " "

class Board:
    def __init__(self, board=None):
        if board is None:
            self.board = u.regBoard
        else:
            self.board = board
            
    def squareRight(self, square):
        return self.board[square.row][square.col + 1]

    def adjacents(self, square):
        r, c = square.row, square.col
        return [board[i][j] for i, j in [r+1, c],
                                        [r-1, c],
                                        [r, c+1],
                                        [r, c-1]]
    
    def generateAnchorSquares(self):
        for row in self.board:
            for sq in row:
                if not sq.isEmpty():
                    yield from filter(Square.possibleAnchor, self.adjacents(sq))

    def cross_checks(self, square):
        ...
        
class Square:
    def __init__(self, letter, row, col):
        self.letter = letter
        self.sentinel = self.letter in u.extraList
        self.space = letter == SPACE
        self.row = row
        self.col = col
        
    def isEmpty(self):
        return self.space

    def possibleAnchor(self):
        return self.space and not self.sentinel
                                      
    def get(self):
        ...
        
class Rack: #probably shouldn't class, just make a list
    def remove(self, letter):
        ...

    def append(self, letter):
        ...
        
def leftPart(partialWord, node, limit):
    extendRight(partialWord, node, anchorSquare)
    if limit > 0:
        for action, nodeTo in node.actions.items():
            if action in rack:
                rack.remove(action)
                leftPart(partialWord + action, nodeTo, limit - 1)

def extendRight(partialWord, node, square):
    if square.isEmpty():
        if node.isEnd():
            storeMove(partialWord)
        for action, nodeTo in node.actions.items():
            if action in rack and n in square.cross_checks():
                rack.remove(action)
                next_square = board.squareRight(square)
                extendRight(partialWord + action, nodeTo, next_square)
                rack.append(action)
    else:
        letter = square.get()
        if letter in node.actions:
            next_square = board.squareRight(square)
            extendRight(partialWord + letter, node.actions[letter])
            
def storeMove(move):
    ...
