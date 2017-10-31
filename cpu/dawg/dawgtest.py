import sys
sys.path.append("../..")
from utils import subdicts
def itersubs():
    for subd in subdicts.values():
        yield from subd

from dawg import *

d = Dawg()
words = ["AAHED", "AAHING", "AALII"]
lex = list(sorted(subdicts["AB"]))[:100]
for w in lex:
    #print("adding {}".format(w))
    d.add(w)
print('min')
d.pathgen()
d.minimize()
print(d)
#print(d.replacements)
for w in lex:
    if not d.acceptable(w):
        print(w)
        for i in range(len(w)+1):
            j=d.parse(w[:i])
            print("\t {}:".format(w[:i]), j.coolstr() if j else False)
 #   print(w, d.acceptable(w))
#print(d)
#print(d.acceptable("AAHII"))
#print(d.acceptable("AC"))
from timeit import timeit

def check():
    return d.acceptable("ABCDEFG")

print(timeit(check, number=1))
