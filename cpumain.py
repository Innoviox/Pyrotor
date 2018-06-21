import cpu.cpu as cpu
from cpu import WeightedScorer
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
    s += c.displayBoard(c.board)
    f = open(file,'w',encoding='utf-8')
    f.write(s)
    f.close()
def main(w1, w2, f):
    c = cpu.CPU(strategy=WeightedScorer, bl_args=[w1, w2])
    ms=[]
    rs=[]
    ts=[]
    ss=[]
    while c.distribution:
        rs.append(''.join(c.rack))
        t=time.time()
        ms.append(c.run())
        ts.append(round(time.time()-t, 2))
        ss.append(c.score)
        write_state_to_file(c, ms, rs, ts, ss, file=f)
# main(1, 1, "run.txt")
import os
def testweights():
    from random import random

    #args = [[random() * 4, random() * 4] for i in range(100)]
    args = [[1, i / 10] for i in range(16, 51)]
    for w1, w2 in args:
        d = "cpu-testing {} {}".format(round(w1, 4), round(w2, 4))
        os.mkdir(d)
        os.chdir(d)
        for i in range(100):
            print(i)
            main(w1, w2, "run{}.txt".format(i))
        os.chdir("..")
main(1, 1, "run.txt")
# testweights()
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
