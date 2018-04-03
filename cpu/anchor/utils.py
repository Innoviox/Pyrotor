import collections
import itertools
import string
leaves = open("cpu/resources/leaves.txt").read().split()
leavesDict = {leaves[i]:float(leaves[i+1]) for i in range(0, len(leaves), 2)}
leavesDict[''] = 0
diphths = [["".join(i) for i in itertools.permutations(list(string.ascii_uppercase), 2)] + \
                                        [j*2 for j in string.ascii_uppercase]][0]
subdicts = {diphth: set(open("cpu/resources/" + diphth + ".txt").read().split()) \
                         for diphth in diphths}

regBoard=[[" ", "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O "],
            ['01', 'TWS', ' ',   ' ',   'DLS', ' ',   ' ',   ' ',   'TWS', ' ',   ' ',   ' ',   'DLS', ' ',   ' ',   'TWS'],
            ['02', ' ',   'DWS', ' ',   ' ',   ' ',   'TLS', ' ',   ' ',   ' ',   'TLS', ' ',   ' ',   ' ',   'DWS', ' '],
            ['03', ' ',   ' ',   'DWS', ' ',   ' ',   ' ',   'DLS', ' ',   'DLS', ' ',   ' ',   ' ',   'DWS', ' ',   ' '],
            ['04', 'DLS', ' ',   ' ',   'DWS', ' ',   ' ',   ' ',   'DLS', ' ',   ' ',   ' ',   'DWS', ' ',   ' ',   'DLS'],
            ['05', ' ',   ' ',   ' ',   ' ',   'DWS', ' ',   ' ',   ' ',   ' ',   ' ',   'DWS', ' ',   ' ',   ' ',   ' '],
            ['06', ' ',   'TLS', ' ',   ' ',   ' ',   'TLS', ' ',   ' ',   ' ',   'TLS', ' ',   ' ',   ' ',   'TLS', ' '],
            ['07', ' ',   ' ',   'DLS', ' ',   ' ',   ' ',   'DLS', ' ',   'DLS', ' ',   ' ',   ' ',   'DLS', ' ',   ' '],
            ['08', 'TWS', ' ',   ' ',   'DLS', ' ',   ' ',   ' ',   'A',   'B',   ' ',   ' ',   'DLS', ' ',   ' ',   'TWS'],
            ['09', ' ',   ' ',   'DLS', ' ',   ' ',   ' ',   'DLS', ' ',   'DLS', ' ',   ' ',   ' ',   'DLS', ' ',   ' '],
            ['10', ' ',   'TLS', ' ',   ' ',   ' ',   'TLS', ' ',   ' ',   ' ',   'TLS', ' ',   ' ',   ' ',   'TLS', ' '],
            ['11', ' ',   ' ',   ' ',   ' ',   'DWS'  , ' ', ' ',   ' ',   ' ',   ' ',   'DWS', ' ',   ' ',   ' ',   ' '],
            ['12', 'DLS', ' ',   ' ',   'DWS', ' ',   ' ',   ' ',   'DLS', ' ',   ' ',   ' ',   'DWS', ' ',   ' ',   'DLS'],
            ['13', ' ',   ' ',   'DWS', ' ',   ' ',   ' ',   'DLS', ' ',   'DLS', ' ',   ' ',   ' ',   'DWS', ' ',   ' '],
            ['14', ' ',   'DWS', ' ',   ' ',   ' ',   'TLS', ' ',   ' ',   ' ',   'TLS', ' ',   ' ',   ' ',   'DWS', ' '],
            ['15', 'TWS', ' ',   ' ',   'DLS', ' ',   ' ',   ' ',   'TWS', ' ',   ' ',   ' ',   'DLS', ' ',   ' ',   'TWS']]
regCC = [[string.ascii_uppercase for i in range(16)] for j in range(16)]

extraList=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15",
           "TWS", "DWS", "TLS", "DLS",
           "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ",
           "*", " "]
distribution = ["a", "a", "a", "a", "a", "a", "a", "a", "a", "b", "b", "c", "c", "d", "d", "d", "d", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "e", "f", "f", "g", "g", "g", "h", "h", "i", "i", "i", "i", "i", "i", "i", "i", "i", "j", "k", "l",    "l", "l", "l", "m", "m", "n", "n", "n", "n", "n", "n", "o", "o", "o", "o", "o", "o", "o", "o", "p", "p", "q", "r", "r", "r", "r", "r", "r","s", "s", "s", "s", "t", "t", "t", "t", "t", "t", "u", "u", "u", "u", "v", "v", "w", "w", "x", "y", "y", "z"]
scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
           "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
           "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
           "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
           "x": 8, "z": 10}

def skips(move):
    sk=[]
    r, c = move.row, move.col
    i=0
    while move.board.board[r][c] not in extraList:
        if move.board.board[r][c] == move.prevBoard.board[r][c]:
            sk.append({move.board.board[r][c]: i})
        else:
            i += 1
        if not move.rwws:
            im = 1
        else:
            im = -1

        if move.direction == 'D':
            r -= im
        else:
            c -= im

        if r > 15 or c > 15:
            if move.rwws:
                return reversed(sk)
            return sk
    if move.rwws:
        return reversed(sk)
    return sk
def skips_formatted(move):
    word = list(move.word)
    for i in skips(move):
        for k, v in i.items():
            word.insert(v, '({})'.format(k))#f'({k})')
    return ''.join(i for i in word).replace(')(', '')

class Move():
    def __init__(self, word, board, row, column, direction, prevBoard, rack, \
                 doNotScoreWord=False, revWordWhenScoring=True, evaluate=True, _type='P'):
        self.word = word
        self.board = board
        self.row = row
        self.col = column
        self.direction = direction
        self.prevBoard = prevBoard
        self.dnsw = doNotScoreWord
        self.rwws = revWordWhenScoring
        self.rack = rack

        
    def comp(self, other):
        return self.score+self.valuation>other.score+other.valuation

    def getScore(self):
        self.score = self.prevBoard.score(self)
        return self.score
    
    def getEvaluation(self, rack):
        nR = rack[:]
        for letter in self.word:
            if letter in nR:
                nR.remove(letter)

        self.valuation = leavesDict[''.join(i for i in sorted(nR))]
        return self.valuation
    def __repr__(self):
        return ", ".join(str(i) for i in (skips_formatted(self), self.score, self.valuation, self.row, self.col)) + "\n"
    
class Board():
    def __init__(self, board=None, crosschecks=None):
        if board is None:
            self.board = regBoard
        else:
            self.board = board
        if crosschecks is None:
            self.crosschecks = regCC
        else:
            self.crosschecks = crosschecks
            
        self.subdicts = subdicts
        self.extraList = extraList

    def checkWord(self, word):
        return len(word) > 1 and word.upper() in subdicts[word[:2]]


    def getWords(self, board):
        words = []
        uai = []  # used across indexes
        udi = []  # used down indexes
        # Iterate through; find a letter -> follow right/down
        c = 0
        
        def _getWord(rIndex, row, cIndex, col, direc, _c):
            nR, nC = rIndex, cIndex
            word=collections.OrderedDict()
            l = uai if direc=='A' else udi
            while l.count((nR, nC))<1 and \
                  nR < len(board) and nC < len(board[nR]) and \
                  board[nR][nC] not in self.extraList:
                letter = board[nR][nC]
                if word.get(letter):
                    letter += str(_c) #differentiate
                    _c += 1
                word[letter] = (nR, nC)
                l.append((nR, nC))
                if direc=='A':
                    nC += 1
                else:
                    nR += 1
            if len(word)>1:
                words.append(word) 
            return _c

        for (rIndex, row) in enumerate(board):
            for (cIndex, col) in enumerate(row):
                if col not in self.extraList:
                    for direc in 'AD':
                        c = _getWord(rIndex, row, cIndex, col, direc, c)
        
        return list(map(self.minimize, words))
    
    def minimize(self, wordDict):
        word = ''.join(i[0] for i in wordDict.keys())
        newDict = collections.OrderedDict()
        currentPositions = {letter: 0 for letter in word}
        for (letter, place) in wordDict.items():
            if len(letter) == 0:
                newDict[letter] = place
            else:
                addStr = ''
                if currentPositions[letter[0]] != 0:
                    addStr = str(currentPositions[letter[0]])
                newDict[letter[0] + addStr] = place
                currentPositions[letter[0]] += 1
        return newDict
    
    def expandFrom(self, point, places, extendedFrom, ):
        assert point not in extendedFrom
        
        usedPlaces = [point]
        
        rT, cT = point
        cT += 1
        while (rT, cT) in places:
            usedPlaces.append((rT, cT))
            cT += 1
            
        cT = point[1]
        cT -= 1
        while (rT, cT) in places:
            usedPlaces.append((rT, cT))
            cT -= 1

        cT = point[1]
        rT += 1
        while (rT, cT) in places:
            usedPlaces.append((rT, cT))
            rT += 1

        rT = point[0]
        rT -= 1
        while (rT, cT) in places:
            usedPlaces.append((rT, cT))
            rT -= 1
        return usedPlaces
    
    def removeDuplicates(self, oldList):
        return list(set(oldList))

    def checkBoard(self, board):
        if board[0] != [" ", "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O "]:
            return False
        if [i[0] for i in board] != [' ', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']:
            return False
        if board[8][8] == "*":
            return False
        
        words = self.getWords(board)
        correctWords = [word for word in words if self.checkWord(''.join(letter[0] for letter in word.keys()))]
        if len(correctWords) < len(words):
            return False
        
        places = [value for word in words for value in word.values()]
        if places:
            top = places[0]
        else:
            return False
        extendedFrom = []
        usedPlaces = self.expandFrom(top, places, extendedFrom)
        l = [coord for place in places for coord in place]
        #Extend to the edge of the board
        for j in range(min(l), max(l)+1):
            np = usedPlaces[:]
            for i in np:
                try:
                    usedPlaces.extend(self.expandFrom(i, places, extendedFrom))
                    usedPlaces = self.removeDuplicates(usedPlaces)
                    extendedFrom.append(i)
                  #  if sorted(usedPlaces) == sorted(places):
                        #return True
                except AssertionError:
                    pass
                
        #if any place wasn't used return false
        if len([place for place in places if place not in usedPlaces]) == 0:
            return True
        return False
    
    def getPlaces(self, board):
        words = [word for word in self.getWords(board) if self.checkWord(''.join(letter[0] for letter in word.keys()))]
        places = [value for word in words for value in word.values()]
        return places

    def clone(self):
        return Board(board=[row[:] for row in self.board])

    def slotify(self, slot):
        slot = ''.join(slot)
        slot = slot.replace(' ', '.')
        for i in self.extraList:
            slot = slot.replace(i, '.')
        return slot
    
    def display(self):
        s="{bar}\n{sep}\n".format(bar="|",sep="-"*66)
        text=s+s.join(''.join('|'+c.center(4 if j == 0 else 3) for j, c in enumerate(r)) for r in self.board) + s
        text = text[2:-1]
        print(text)
        return text


    def score(self, move):
        oldWords = self.getWords(self.board)
        allWords = self.getWords(move.board.board)
        newWords = [word for word in allWords if word not in oldWords]
        wordScore = 0
        wordMult = 1
        scored = collections.OrderedDict()
        c=0
        if not move.dnsw:
            if move.rwws:
                sw = reversed(move.word)
                im = 1
            else:
                sw = move.word
                im = -1
            for (index, letter) in enumerate(sw):
                row = move.row
                col = move.col
                
                if move.direction == 'D':
                    row -= index*im
                else:
                    col -= index*im
                
                if row>15 or col>15:
                    return 0
                lettMult = 1
                oldLetter = self.board[row][col]
                if oldLetter in ['TLS', 'DLS']:
                    lettMult *= ['D', 'T'].index(oldLetter[0])+2
                elif oldLetter in ['TWS', 'DWS']:
                    wordMult *= ['D', 'T'].index(oldLetter[0])+2
                elif oldLetter == '*':
                    wordMult *= 2
                wordScore += scores[letter.lower()] * lettMult
                if scored.get(letter):
                    scored[letter+str(c)]=(row, col)
                    c+=1
                else:
                    scored[letter]=(row,col)
            
            wordScore *= wordMult
        if move.rwws:
            scored = collections.OrderedDict(list(scored.items())[::-1])
        for word in newWords:
            if move.dnsw or not set([i for i in scored.values()]).issubset(set([i for i in word.values()])):
                auxWordScore = 0
                auxWordMult = 1
                for (letter, place) in word.items():
                    lettMult = 1
                    letter = letter[0]
                    row, col = place
                    oldLetter = self.board[row][col]
                    if row>15 or col>15:
                        return 0
                    if oldLetter in ['TLS', 'DLS']:
                        lettMult *= ['D', 'T'].index(oldLetter[0])+2
                    elif oldLetter in ['TWS', 'DWS']:
                        auxWordMult *= ['D', 'T'].index(oldLetter[0])+2
                    auxWordScore += scores[letter.lower()] * lettMult
                auxWordScore *= auxWordMult
                wordScore += auxWordScore
        if len(move.word) == 7:
            wordScore += 50 #Bingo!
        return wordScore

    def s(self, move):
        self.scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
                       "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
                       "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
                       "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
                       "x": 8, "z": 10}
        oldWords = self.getWords(self.board)
        allWords = self.getWords(move.board.board)
        newWords = [word for word in allWords if word not in oldWords]
        wordScore = 0
        wordMult = 1
        scored = collections.OrderedDict()
        c = 0

        print("Scoring: ", move)
        if not move.dnsw:
            if move.rwws:
                sw = reversed(move.word)
                im = 1
            else:
                sw = move.word
                im = -1
            for (index, letter) in enumerate(sw):
                row = move.row
                col = move.col

                if move.direction == 'D':
                    row -= index * im
                else:
                    col -= index * im

                if row > 15 or col > 15:
                    print('fa')
                    return 0
                lettMult = 1
                oldLetter = self.board[row][col]
                print(f"Scoring letter {letter} at {row}, {col}")
                print(f"Old letter: {oldLetter}")
                if oldLetter in ['TLS', 'DLS']:
                    lettMult *= ['D', 'T'].index(oldLetter[0]) + 2
                elif oldLetter in ['TWS', 'DWS']:
                    wordMult *= ['D', 'T'].index(oldLetter[0]) + 2
                elif oldLetter == '*':
                    wordMult *= 2
                print(f"Letter multiplier: {lettMult}")
                wordScore += self.scores[letter.lower()] * lettMult
                if scored.get(letter):
                    scored[letter + str(c)] = (row, col)
                    c += 1
                else:
                    scored[letter] = (row, col)
                print(wordScore)

            wordScore *= wordMult
            print(wordScore)
        if move.rwws:
            scored = collections.OrderedDict(list(scored.items())[::-1])
        for word in newWords:
            if move.dnsw or not set([i for i in scored.values()]).issubset(set([i for i in word.values()])):
                print('aux', word)
                auxWordScore = 0
                auxWordMult = 1
                for (letter, place) in word.items():
                    # if place not in scored.values():
                    print('\t scoring', letter, place)
                    lettMult = 1
                    letter = letter[0]
                    row, col = place
                    oldLetter = self.board[row][col]
                    if row > 15 or col > 15:
                        print('fa')
                        return 0
                    if oldLetter in ['TLS', 'DLS']:
                        lettMult *= ['D', 'T'].index(oldLetter[0]) + 2
                    elif oldLetter in ['TWS', 'DWS']:
                        auxWordMult *= ['D', 'T'].index(oldLetter[0]) + 2
                    print(oldLetter)
                    print(lettMult)
                    auxWordScore += self.scores[letter.lower()] * lettMult
                    print(auxWordScore)
                auxWordScore *= auxWordMult
                print(auxWordScore)
                wordScore += auxWordScore
                print(wordScore)
        if len(move.word) == 7:
            wordScore += 50  # Bingo!
        # input()
        return wordScore

    def __getitem__(self, idx):
        return self.board[idx]

    def adjacents(self, r, c):
        if 1 < r:
            yield self[r-1][c]
        if 1 < c:
            yield self[r][c-1]
        if r < 15:
            yield self[r+1][c]
        if c < 15:
            yield self[r][c+1]

    def anchors(self):
        for i, row in enumerate(self.board[1:], start=1):
            r, r_ = self._slotify(row), row
            for j, sq in enumerate(row[1:], start=1):
                c_ =  [i[j] for i in self.board]
                c = self._slotify(c_)
                #print('b1', r, r_)
                #print('c1', c, c_)
                if sq in extraList and any(i not in extraList for i in self.adjacents(i, j)):
                    #print('b', r, r_)
                    #print('c', c, c_)
                    yield Anchor(r[:], r_[:], j, i)
                    yield Anchor(c[:], c_[:], i, j)

    def reinsert(self, anchor):
        slot = anchor.real_slot
        idx = anchor.idx
        if slot[0] in self[0]:
            for i in range(len(self.board)):
                r = self.board[i]
                r[idx] = slot[i]
                self.board[i] = r
        else:
            self.board[idx - 1] = slot

    def direction(self, anchor):
        return not anchor.slot[0] in self[0] # true for row, false for col

    def dstr(self, anchor):
        return 'A' if self.direction(anchor) else 'D'

    def _slotify(self, slot):
        return ''.join('.' if i in extraList else i for i in slot)

def checkWord(word):
        word = word.upper()
        return len(word) > 1 and word in subdicts[word[:2]]

class Anchor:
    def __init__(self, slot, real_slot, idx, board_idx):
        #print(slot)
        self.slot, self.real_slot, self.idx, self.board_idx = slot, real_slot, idx, board_idx
        # assert slot[idx] in extraList

    def expand(self, word, direction):
        slot = self.real_slot[:]
        idx = self.idx
        word_iter = iter(word)
        while 0 < idx < len(slot):
            if slot[idx] in extraList:
                try:
                    slot[idx] = next(word_iter)
                except StopIteration:
                    return slot
            idx += direction
        return slot

