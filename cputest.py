from cpu import CPU
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
##        print(m)
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
    os.environ["PATH"] = "/Users/chervjay/homebrew/bin"
    c = CPU()
    
    from pycallgraph import PyCallGraph
    from pycallgraph.output import GraphvizOutput

    g = GraphvizOutput()
    g.output_file = "run.png"
    c.rack = list("ABCDEFG")
##    c._run()
    #with PyCallGraph(output=g):
    c._run()
    g2 = GraphvizOutput()
    g2.output_file = "run2.png"
    c.rack = list("HILMNOP")
##    c._run()
##    for i in range(10):
##        c._run()
##    with PyCallGraph(output=g2):
##        c._run()
    cProfile.run('c._run()', 'run.profile')
    stats = pstats.Stats('run.profile')
    stats.strip_dirs().sort_stats('time').print_stats(15)
      #fight()
#[1.7072216619853862, 3.1325161900022067, 1.6216930149821565, 3.268413445999613, 3.705194982991088, 15.889340254012495, 5.688638204999734, 4.1342786839813925, 20.16599447801127, 5.605817347008269, 15.521598959021503, 8.941739761008648, 25.326604697998846, 18.971136287000263, 28.019278490013676, 26.350266034016386, 23.84890027498477, 16.002048529975582, 7.042422533995705, 26.99606496299384, 32.414714958984405, 15.247227340994868, 1.1243990630027838, 3.4754078430123627, 11.673580643022433, 2.6024817819998134, 7.487077052996028, 7.309637408994604, 11.14153193400125, 14.711314640007913, 8.855871091014706, 29.52353919702, 18.273340198997175, 30.2577743739821, 16.94557886000257, 19.052926197997294, 13.73912344200653, 13.845009912998648, 34.1416648819868, 39.3223710609891, 40.41984408602002, 26.62969347499893, 19.51503164198948, 44.1740132959967, 39.12099281800329, 1.2027060329855885, 2.65757844701875, 4.557685183011927, 4.110742001998005, 10.145192698022583, 4.7756191799999215, 4.710683440993307, 13.963426639995305, 13.199134234018857, 26.245197443990037, 33.25656496998272, 22.95353161598905, 30.64343233400723, 16.719950309983687, 30.113948104000883, 17.75676007498987, 13.29482840700075, 27.94027982300031, 11.234770610986743, 19.581611906993203, 15.192255259986268, 49.241733882023254, 0.8161826569994446, 5.454085556004429, 4.969681193004362, 10.928349269001046, 1.5972406709915958, 3.6771177009795792, 5.738978226989275, 6.110980087018106, 12.932388702000026, 10.695273424003972, 21.048558980983216, 32.73511774398503, 13.641970978002064, 13.774489501985954, 14.741290208999999, 13.078035676997388, 29.453492833010387, 57.62879308700212, 11.837178073998075, 11.057494577980833, 27.168097740010126, 0.3975788909883704, 1.4681445810128935, 5.444586767000146, 4.077422722999472, 8.503607852006098, 10.49940709999646, 10.740528668975458, 4.019111391011393, 11.964352468989091, 20.951317258994095, 10.927683763002278, 14.412274879985489, 7.626214646996232, 6.811122585000703, 20.354628455999773, 19.115355746995192, 36.390685473015765, 37.57398434399511, 39.32085073101916, 24.51525673098513, 49.96606025699293, 45.93350953402114, 25.294191809021868]
#16.773275875188578