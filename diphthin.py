class AlreadyRunError(BaseException):
    pass
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path += "/resources/"
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
else:
    raise AlreadyRunError
ospd = open("newDict.txt").read().split("\n")
nospd = []
for word in ospd:
    nospd.append(word.strip())
from itertools import permutations as p
from string import ascii_uppercase as a_u
diphths = ["".join(i) for i in p(list(a_u), 2)]
for i in a_u:
    diphths.append(i*2)
for i in diphths:
    with open("resources/"+i+".txt", "w"):
        pass
    dfile = open("resources/"+i+".txt", "w")
    for word in nospd:
        if word[:2] == i:
            pass
            dfile.write(word)
            dfile.write("\n")
    dfile.close()
    




