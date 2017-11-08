import cpu
import tabulate as tb
import time

def write_state_to_file(c, moves, racks, times, file='run.txt'):
    s=''
    h = ['Turn', 'Word', 'Score', 'Eval', 'Pos', 'Rack', 'Time']
    t=[]
    
    for i,m in enumerate(moves,start=1):
        t.append([i,cpu.skips_formatted(m), m.score, m.valuation, (m.row, m.col), racks[i-1], times[i-1]])
    s += tb.tabulate(t,headers=h,tablefmt="fancy_grid")
    s+='\n'
    s += c.displayBoard(c.board)
    f = open(file,'w',encoding='utf-8')
    f.write(s)
    f.close()
    
c = cpu.CPU()
ms=[]
rs=[]
ts=[]
while c.distribution:
    rs.append(''.join(c.rack))
    t=time.time()
    ms.append(c._run())
    ts.append(round(time.time()-t, 2))
    write_state_to_file(c, ms, rs, ts)
    print(open('run.txt').read())