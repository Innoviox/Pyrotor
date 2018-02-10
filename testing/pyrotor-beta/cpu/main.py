import cpu
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
c = cpu.CPU()
ms=[]
rs=[]
ts=[]
ss=[]
while c.distribution:
    rs.append(''.join(c.rack))
    t=time.time()
    ms.append(c._run())
    ts.append(round(time.time()-t, 2))
    ss.append(c.score)
    write_state_to_file(c, ms, rs, ts, ss)