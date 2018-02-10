from cpu.cpu import CPU
import cProfile
import pstats
import time as _time
def time(f, n):
    print(cpu.timeit.timeit(f, number=n))
    #for i in range(n):
        #print(cpu.timeit.timeit(f, number=1))
def fight():
    c = CPU()
    m=[]
    while c.distribution:
        m.append(c._run())
        print(m)
        c.displayBoard(c.board.board)  
##    c = CPU()
##    c2 = CPU()
##    m=[]
##    while distribution: #(c.rack and c2.rack) or 
##        m.append(c._run())
##        print(m)ca
##        c2.board = c.board
##        m.append(c2._run())
##        print(m)
##        c.board = c2.board
##        print(c.score, c2.score)
    
##    def a():
##        c.board.getWords(c.board.board)
##    def d():
##        c.board.checkBoard(c.board.board)
##    def e():
##        for i in c.generate():pass
##    def f():
##        b.getScore()
##    def g():
##        pass
##        #b.getEvaluation(c.rack)
def test():
    q=[]
    for i in range(5):
        c = CPU()
        m=[]
        while c.distribution:
            m.append(cpu.timeit.timeit(c._run, number=1))
            print(m)
            #c.displayBoard(c.board.board)
        q.extend(m)
    print(q)
        
##        #c.board.s(b)
##        #input()
##        m.append(b)
##        print(m)
        
##        time(a, 1000)
##        time(d, 1000)
##        time(f, 1000)
##        time(g, 1000)
        #time(e, 5)
        
    
if __name__ == "__main__":
##
##    for i in range(10):
##        c = CPU()
##        t=_time.time()
##        c.rack = list("ABCDEFG")
##        c._run()
##        print(_time.time()-t)
##        t=_time.time()
##        c.rack = list("HILMNOP")
##        c._run()
##        print(_time.time()-t)
##    while c.distribution:
##        cProfile.run('c._run()', 'run.profile')
##        stats = pstats.Stats('run.profile')
##        stats.strip_dirs().sort_stats('time').print_stats(15)
##        input()
    import os
    os.environ["PATH"] += ":/Users/chervjay/homebrew/bin"
    c = CPU()
    os.chdir("runs")
    i = 1
    while os.path.exists("test"+str(i)):
        i += 1
    os.makedirs("test"+str(i))
    os.chdir("test"+str(i))
    from pycallgraph import PyCallGraph, Config
    from pycallgraph.output import GraphvizOutput
    run = 0
    while c.distribution:
        #c.run()
        #continue
        direc = "turn{}:{}".format(run, ''.join(sorted(c.rack)))
        os.makedirs(direc)
        os.chdir(direc)
        g = GraphvizOutput(output_file="run.png")
        #with PyCallGraph(output=g):
        cProfile.run('c.run("board.txt")', 'run.profile')
        readable = open("run.txt", "w")
        stats = pstats.Stats('run.profile', stream=readable)
        stats.strip_dirs().sort_stats('time').print_stats()
        readable.close()
        os.chdir('..')
        run += 1
    #while c.distribution:
    #    c._run()