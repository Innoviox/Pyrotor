import cpu.cpu as cpu
from cpu import WeightedScorer, Board, readBoard
import tabulate as tb
import time
pos = lambda r, c: "ABCDEFGHIJKLMNO"[c - 1] + str(r)
score = lambda m, c: '+{:>3}/{:>3}'.format(m.score, c)
val = lambda m, c: '{:0>3.2f}'.format(c.strategy.score(m))
def write_state_to_file(c, moves, racks, times, scores, file='run.txt'):
    s=''
    h = ['Word', 'Score', 'Eval', 'Pos', 'Rack', 'Time']
    t=[]
    for i,m in enumerate(moves,start=1):
        t.append([cpu.skips_formatted(m), score(m, scores[i-1]), val(m,c), pos(m.row, m.col), racks[i-1], times[i-1]])
    s += tb.tabulate(t,headers=h,showindex=range(1,len(t)+1))#,tablefmt="fancy_grid")
    s+='\n'
    s += c.displayBoard(c.board, out=False)
    f = open(file,'w',encoding='utf-8')
    f.write(s)
    f.close()

def main(w1, w2, f, racks=None):
    readBoard()
    c = cpu.CPU(strategy=WeightedScorer, bl_args=[w1, w2])
    c.displayBoard(c.board)
    ms=[]
    rs=[]
    ts=[]
    ss=[]
    while (not racks) or c.distribution:
        if racks is not None:
            try:
              c.rack = next(racks)
            except StopIteration:
                return

        rs.append(''.join(c.rack))
        t=time.time()
        for move in c.pick_n(5):
            print(move)
        ts.append(round(time.time()-t, 2))
        ss.append(c.score)
        write_state_to_file(c, ms, rs, ts, ss, file=f)

def two_player_game(w1, w2, f):
    b = Board()
    p1 = cpu.CPU(strategy=WeightedScorer, bl_args=[w1, w2], board=b)
    p2 = cpu.CPU(strategy=WeightedScorer, bl_args=[w1, w2], board=b)
    ms = []
    rs = []
    ts = []
    ss = []
    while True:
        for p in [p1, p2]:
            rs.append(''.join(p.rack))
            t = time.time()
            ms.append(p.run())
            ts.append(round(time.time() - t, 2))
            ss.append(p.score)
            write_state_to_file(p, ms, rs, ts, ss, file=f)

            p1.board = ms[-1].board
            p2.board = ms[-1].board

            p1.distribution = p.distribution
            p2.distribution = p.distribution

            if not p.distribution:
                if not (p1.rack and p2.rack):
                    return
# racks = map(list, [input("Rack: ").upper()])
# main(1, 1, "game.txt", racks=iter(racks))
# input()

def playGame():
    readBoard()
    c = cpu.CPU(strategy=WeightedScorer, bl_args=[1, 1])
    while True:
        rack = list(input("Rack: ").upper())
        c.rack = rack
        print(c.board)
        moves = list(c.pick_n(5))
        for i, suggest in enumerate(moves, start=1):
            print(f"Move {i}:", suggest)
        choice = input("Choose move: ")
        if choice == "other":
            readBoard(b=c.board)
        else:
            move = moves[int(choice) - 1]
            c.board = move.board.clone()
        readBoard(b=c.board)
# playGame()
c = cpu.CPU()
c.rack = list(["RIEMEDO"])
c.run()
import sys
sys.exit()
import os
def testweights():
    from random import random

    args = [[random() * 4, random() * 4] for i in range(1000)]
    # args = [[1, i / 10] for i in range(16, 510)]
    for w1, w2 in [[1, 1]]:#args:
        d = "cpu-testing-two-players {} {}".format(round(w1, 4), round(w2, 4))
        os.mkdir(d)
        os.chdir(d)
        for i in range(100):
            print(i)
            try:
                two_player_game(w1, w2, "run{}.txt".format(i))
            except Exception as e:
                print(e)
        os.chdir("..")
# main(1, 1, "run2.txt")
testweights()
def results():
    for i in os.listdir():
        if len(i.split())==2:
            os.chdir(i)
            sum = 0
            a = []
            j = 0
            while os.path.exists(f"run{j}.txt"):
                f = open("run" + str(j) + ".txt")
                l = f.read().split("------------------------------------------------------------------")[0]
                l = l.split("\n")[-2]
                l = l.split("/")[1].split()[0]
                sum += int(l)
                a.append(l)
                f.close()
            sum /= 5
            print(i, sum, a)
            os.chdir('..')
