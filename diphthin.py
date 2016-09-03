ospd = open("newDict.txt").read().split("\n") #taken from https://raw.githubusercontent.com/xjtian/PyScrabble/master/wordlists/OSPD4_stripped.txt
nospd = []
for word in ospd:
    nospd.append(word.strip())
print(len(ospd))
from itertools import permutations as p
from string import ascii_uppercase as a_u
diphths = ["".join(i) for i in p(list(a_u), 2)]
for i in a_u:
    diphths.append(i*2)
for i in diphths:
    with open(i+".txt", "w"):
        pass
    dfile = open(i+".txt", "w")
    for word in nospd:
        #print(word[:2])
        if word[:2] == i:
            pass
            dfile.write(word)
            dfile.write("\n")
    dfile.close()




