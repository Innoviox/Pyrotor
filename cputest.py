from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from cpu.cpu import CPU
import cProfile
import pstats
import os
if __name__ == "__main__":
    os.environ["PATH"] += ":/Users/chervjay/homebrew/bin"
    c = CPU()
    os.chdir("runs")
    i = 1
    while os.path.exists("test"+str(i)):
        i += 1
    os.makedirs("test"+str(i))
    os.chdir("test"+str(i))

    run = 0
    while c.distribution:
        direc = "turn{}:{}".format(run, ''.join(sorted(c.rack)))
        os.makedirs(direc)
        os.chdir(direc)
        g = GraphvizOutput(output_file=f"{direc}/run.png")
        with PyCallGraph(output=g):
            cProfile.run('c.run("board.txt")', 'run.profile')
            readable = open("run.txt", "w")
            stats = pstats.Stats('run.profile', stream=readable)
            stats.strip_dirs().sort_stats('time').print_stats()
            readable.close()
            os.chdir('..')
            run += 1