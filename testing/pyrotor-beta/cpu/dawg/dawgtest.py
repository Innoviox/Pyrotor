import sys
sys.path.append("../..")
from utils import subdicts
import os
os.environ["PATH"] += ":/Users/chervjay/homebrew/bin"
def itersubs():
    for subd in subdicts.values():
        yield from subd

from newdawg import *

d = Dawg()
words = ["AAHED", "AAHING", "AALII"]
lex = list(sorted(sorted(subdicts["AB"])))#[:10]
#lex.extend(list(sorted(sorted(subdicts["AC"]))))#[:100])
from pycallgraph import PyCallGraph, Config
from pycallgraph.output import GraphvizOutput
g = GraphvizOutput(output_file="run.png")
#with PyCallGraph(output=g):
for w in lex:
    d.add(w)
#print('min')
#d.pathgen()
#d.minimize()
print(d)
#print(d.replacements)
for w in lex:
    if not d.acceptable(w):
        print(w)
        for i in range(len(w)+1):
            j=d.parse(w[:i])
            #print("\t {}:".format(w[:i]), j.fstr() if j else False)
 #   print(w, d.acceptable(w))
#print(d)
#print(d.acceptable("AAHII"))
#print(d.acceptable("AC"))
from timeit import timeit

def check():
    return d.acceptable("AFPJP")

print(timeit(check, number=1190764))
