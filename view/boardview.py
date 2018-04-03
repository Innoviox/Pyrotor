from cpu import Board, CPU, Move, distribution, random, skips_formatted
import tkinter as tk

extraList = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15",
             "TWS", "DWS", "TLS", "DLS",
             "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "I ", "J ", "K ", "L ", "M ", "N ", "O ",
             "*", " "]

colors = {"TWS": "red", "DWS": "pink", "TLS": "light green", "DLS": "light blue", "*": "pink"}

scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
          "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
          "x": 8, "z": 10, "?": 0}

_codes = {0: "\u2080", 1: "\u2081", 2: "\u2082", 3: "\u2083", 4: "\u2084", 5: "\u2085",
          6: "\u2086", 7: "\u2087", 8: "\u2088", 9: "\u2089", 10: "\u2081\u2080"}


def get_subscript(number):
    return _codes[number]


left_arrow = chr(int('2192', 16))
down_arrow = chr(int('2193', 16))
ACROSS, DOWN = 1, 2


class TileLabel:
    def __init__(self, master, label, col, row, new):
        self.text = label
        self.ptext = label
        self.extra = label in extraList
        self.typing = False
        self.master = master
        self.row = row
        self.col = col
        self.frame = tk.Frame(master, bd=1, relief=tk.RAISED, width=1, height=1)
        self.frame.grid(row=row, column=col, columnspan=1)
        self.extra = label in extraList
        self._init_as_standard()
        self.new = new
        if label not in extraList:
            self._init_as_letter(self.text, new=new)
        self.dir = DOWN

    def _init_as_standard(self):
        self.entry = None
        self.label = tk.Label(self.frame, text=self.text.strip(), height=2, width=3)
        if self.text in colors.keys():
            self.label.config(bg=colors[self.text])
        self.label.pack()
        if self.extra:
            self.label.bind("<Button-1>", self.onclick)
        self.new = False

    def _init_as_letter(self, letter, new=False):
        self.text = letter.upper()
        self.entry = tk.Frame(self.master, bd=1, relief=tk.SUNKEN)
        self.entry.grid(row=self.row, column=self.col, columnspan=1)
        self.label.config(text=self.text.upper() + get_subscript(scores[self.text.lower()]), relief=tk.RAISED)

        if new:
            self.label.config(bg="yellow")
        # if self.new:
        #     self.label.config(bg="red")
        self.entry.lift()
        if self.extra:
            self.label.bind("<Button-1>", self.onclick)
        self.new = new and not self.new

    def onclick(self, event):
        if self.row != 0 and self.col != 0:
            if self.dir == ACROSS:
                self.dir = DOWN
                self.label.config(text=down_arrow)
            else:
                self.dir = ACROSS
                self.label.config(text=left_arrow)
            self.master.master.erase_new(self)
            self.typing = True
            self.master.master.typing = self

    def setdir(self, direction):
        self.dir = direction
        self.regress()
        self.typing = True
        self.label.config(text=[left_arrow, down_arrow][direction - 1])

    def regress(self):
        self.text = self.ptext
        if self.entry:
            self.entry.pack_forget()
        self.label.pack_forget()
        self._init_as_standard()
        self.typing = False

    def type(self, event, first_last=False):
        if self.typing:
            char = event.char
            if char == '\x7f':
                self.regress()
                return self.pass_backwards()
            elif char:
                self.typing = False
                if self.entry:
                    self.entry.pack_forget()
                self._init_as_letter(char, new=True)
                return self.pass_forwards()
        else:
            return 0

    def pass_forwards(self):
        return self.dir

    def pass_backwards(self):
        return -self.dir


class RackTile(TileLabel):
    def __init__(self, master, letter, idx):
        super().__init__(master, letter, idx, 1, False)

    def onclick(self, event):
        self.master.master.rack_focus(self)

    def setdir(self, direction): pass

    def type(self, event, first_last=False):
        if self.col == 6 and first_last:
            self.label.config(bg="white")
            return 0
        elif event.char == '\x7f':
            return self.pass_backwards()
        else:
            self._init_as_letter(event.char)
            return self.pass_forwards()

    def pass_forwards(self):
        return 1

    def pass_backwards(self):
        return -1


class Handler:
    def __init__(self):
        self.rack1 = []
        self.rack2 = []
        self.current = 0
        self.racks = [self.rack1, self.rack2]
        self.distribution = distribution
        for rack in self.racks:
            self.draw_tiles(rack)

    def draw_tiles(self, rack):
        while len(rack) < 7 and len(self.distribution) > 0:
            letter = random.choice(self.distribution)
            rack.append(letter.upper())
            self.distribution.remove(letter)

    def switch_player(self):
        self.current += 1
        self.current %= 2

    def current_rack(self):
        return self.racks[self.current]

    def draw_current_rack(self):
        self.draw_tiles(self.current_rack())


class BoardView(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.board = Board()
        self.old_board = self.board.clone()
        self.cpu = CPU()

        self.bind("<KeyPress>", self.type)
        self.typing, self.rTyping = None, None
        self.first_last = False

        self.handler = Handler()

        self._init_gui()

    def _init_gui(self):
        self._init_frame()
        self._init_board()
        self._init_rack()
        self._init_moves()

    def _init_frame(self):
        self.boardFrame = tk.Frame(self, bd=1, relief=tk.SUNKEN,  width=497, height=497)

        self.boardFrame.place(x=0, y=0)
        self.boardFrame.grid(columnspan=16, rowspan=16, column=0, row=0)

    def _init_moves(self):
        self.moves = []
        self.text = tk.Label(self, text="Current Move: ")
        self.text.grid(row=0, column=18)
        self.cbtn = tk.Button(self, text="Commit", command=self._commit)
        self.cbtn.grid(row=1, column=18)
        self.data = tk.Listbox(self, bg='white')
        self.scrollbar = tk.Scrollbar(self.data, orient=tk.VERTICAL)
        self.data.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.data.yview)
        self.moves = []
        self.data.grid(row=2, column=18, rowspan=5)
        self.data.bind('<<ListboxSelect>>', self._onselect)
        self.pbtn = tk.Button(self, text="Play", command=self._play)
        self.pbtn.grid(row=7, column=18)

    def _onselect(self, evt):
        move = self.moves[evt.widget.curselection()[0]]
        self.old_board = self.board.clone()
        self.board = move.board
        self._update_board()

    def _play(self):
        move = self.moves[self.data.curselection()[0]]
        self.board = move.board.clone()
        self.old_board = self.board.clone()
        self.cpu.board = self.board
        self._update_rack(move)
        self.handler.draw_current_rack()
        self.handler.switch_player()
        self._init_rack()
        self._init_board()

    def _update_rack(self, move):
        for i in move.word:
            if i in self.get_rack_text():
                idx = self.get_rack_text().index(i)
                rem = self.rack[idx]
                rem.regress()
                self.handler.current_rack().remove(i)
                self.update()

    def _update_moves(self):
        self.data.delete(0, tk.END)
        for move in self.moves:
            self.data.insert(tk.END, self._fstr(move))

    def _commit(self):
        move = self.get_current_move()
        if move:
            self.moves.append(move)
            self._update_moves()

    def _commit_move(self, move):
        self.moves.append(move)
        self._update_moves()

    def _init_board(self):
        self.tiles = []
        for i in range(16):
            self.grid_rowconfigure(i, minsize=31)
            self.tiles.append([])
            for j in range(16):
                self.grid_columnconfigure(j, minsize=31)
                label = self.board[j][i]
                new = label != self.old_board[j][i]
                self.tiles[-1].append(TileLabel(self.boardFrame, label, i, j, new=new))

        self.solveButton = tk.Button(self, text="Solve!", command=self.solve)
        self.solveButton.grid(column=8, row=18)

    def _update_board(self):
        for i in range(16):
            for j in range(16):
                label = self.board[j][i]
                new = label != self.old_board[j][i]
                if new:
                    self.tiles[i][j] = TileLabel(self.boardFrame, label, i, j, new=new)

    def _init_rack(self):
        self.rackFrame = tk.Frame(self, bd=1, relief=tk.SUNKEN)
        self.rackFrame.grid(columnspan=7, row=17, column=5)
        self.first_last = False
        self.rack = []
        for i, letter in zip(range(7), self.handler.current_rack()):
            self.rack.append(RackTile(self.rackFrame, letter, i))

    def get_rack_text(self):
        return [i.text for i in self.rack]

    def solve(self):
        self.moves.clear()
        self._update_moves()
        self.place(force=True)
        self.cpu.rack = self.get_rack_text()
        # self.cpu.run()
        # self.old_board = self.board.clone()
        # self.board = self.cpu.board
        # self._update_board()
        for move in self.cpu.pick_n(20):
            self._commit_move(move)

    def erase_new(self, ignore):
        for r in self.tiles:
            for tile in r:
                if tile is not ignore:
                    if tile.new or tile.typing:
                        tile.regress()
                        if tile is self.typing:
                            self.typing = None

    def rack_focus(self, rack_tile):
        self.rTyping = rack_tile
        rack_tile.label.config(bg="yellow")
        self.first_last = False
        self.typing = None

    def type(self, event):
        if self.typing:
            direction = self.typing.type(event)
            c, r = self.typing.row, self.typing.col
            first = True
            while first or self.board[c][r] not in extraList:
                if direction == ACROSS:
                    r += 1
                elif direction == -ACROSS:
                    r -= 1
                elif direction == DOWN:
                    c += 1
                else:
                    c -= 1
                first = False
                if c > 15 or r > 15:
                    return
            if 0 < r < 16 and 0 < c < 16:
                self.typing = self.tiles[r][c]
                self.typing.typing = True
                self.typing.setdir(abs(direction))
            else:
                self.typing = None
            self._update_current_move()
        elif self.rTyping:
            d = self.rTyping.type(event)
            e = (d / 2) + 0.5
            if d == -1:
                self.rTyping.regress()
                self.rTyping.label.config(bg="yellow")
            elif d == 1:
                self.rTyping.label.config(bg="white")
            if [1, 0][int(e)] <= self.rTyping.col <= [6, 5][int(e)]:
                self.rTyping.label.config(bg="white")
                self.rTyping = self.rack[self.rTyping.col + d]
                if self.rTyping.col != 6 or (self.rTyping.col == 6 and not self.first_last):
                    self.rTyping.label.config(bg="yellow")
                    if self.rTyping.col == 6:
                        self.first_last = True

    def get_current_move(self):
        move = []
        word = ''
        for r in self.tiles:
            for tile in r:
                if tile.new:
                    move.append(tile)
                    word += tile.text
        if move:
            row        = move[0].row
            col        = move[0].col
            board      = self.place()
            prev_board = self.board.clone()
            direction  = move[0].dir
            rack       = self.get_rack_text()

            m = Move(word, board, row, col, direction, prev_board, rack)
            return m
        return False

    def place(self, force=False):
        if force:
            new_board = self.board
        else:
            new_board = self.board.clone()
        for r in self.tiles:
            for tile in r:
                if tile.new:
                    new_board.board[tile.row][tile.col] = tile.text
                    if force:
                        tile.new = False

        return new_board

    @staticmethod
    def _str(move):
        position = (lambda r, c: "ABCDEFGHIJKLMNO"[c - 1] + str(r))(move.row, move.col)
        word = skips_formatted(move)
        sc = move.getScore()
        return f"\n{position} {word} +{sc}"

    def _fstr(self, move):
        try:
            ev = move.getEvaluation(move.rack)
        except KeyError:
            ev = "NR"
        return f"\n{self._str(move)} {ev}"

    def _update_current_move(self):
        move = self.get_current_move()
        if move and move.board.checkBoard(move.board.board):
            # move.board.display()
            # move.prevBoard.display()
            self.text.config(text="Current move: "+self._str(move))
