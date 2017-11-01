class Node:
    _id = 0
    def __init__(self, prev, end=False):
        self.id = Node._id
        Node._id += 1
        self.prev = prev
        self.end = end
        self.actions = {}
        
    def addAction(self, action, nodeTo, force=False):
        if force or action not in self.actions:
            self.actions[action] = nodeTo

    def __repr__(self):
        return self.sstr()

    def __str__(self):
        return self.sstr()

    def sstr(self): #short string: id catalysts actions
        return " ".join(map(str, (self.id, self.catalysts(), self.getactions())))

    def fstr(self): #full  string: s.sstr <= prev
                    #            :     a => s[a].sstr
                    #            :     ...
        s = ""
        s += "{} <= {}\n".format(str(self), self.prev.id if self.prev is not None else "None")
        for action, nodeTo in self.actions.items():
            s += "\t{} => {} \n".format(action, str(nodeTo))
        return s

    def getactions(self):
        return list(self.actions.keys())
    
    def catalysts(self):
        if self.prev is not None:
            return list(self.prev.actionlead(self))
        return [None]

    def actionlead(self, node):
        for action, nodeTo in self.actions.items():
            if nodeTo.id == node.id:
                yield action

    def update(self, replacements):
        for action, node in self.actions.items():
            if node in replacements:
                self.actions[action] = replacements[node]
                
class Automata:
    def __init__(self):
        self.start = Node(None)
        self.nodes = [self.start]
        self.ends = []
        
    def add(self, nodeFrom, action, end=False):
        if action not in nodeFrom.actions:
            nodeTo = Node(nodeFrom, end=end)
            nodeFrom.addAction(action, nodeTo)
        else:
            return nodeFrom.actions[action]
        if end: self.ends.append(nodeTo)
        self.nodes.append(nodeTo)
        return nodeTo

    def parse(self, actions):
        node = self.start
        for action in actions:
            if action in node.actions:
                node = node.actions[action]
            else:
                return False
        return node
    
    def acceptable(self, actions):
        n = self.parse(actions)
        return n and '!' in n.actions
    
    def __str__(self):
        return str(self.nodes)

    
class Trie(Automata):
    def add(self, word):
        nodes = []
        w = word
        node = self.start
        for to in w:
            node = super(Trie, self).add(node, to)
            nodes.append(node)
        nodes.append(super(Trie, self).add(node, "!", end=True))
        return nodes
        
    def __str__(self):
        s = ""
        for node in sorted(self.nodes, key=lambda i:i.id):
            s += node.fstr()
        return s

def cPrefix(w1, w2):
    for i in range(len(w1), 0, -1):
        if w2[:i] == w1[:i]:
            return w1[:i], i
    return None, None

def cSuffix(w1, w2):
    for i in range(0, -len(w1) + 1, -1):
        if w2[i:] == w1[i:]:
            return w1[i:], len(w1) + i, len(w2) + i
    return None, None, None
        
    
class Dawg(Trie):
    def __init__(self):
        super(Dawg, self).__init__()
        self.pWords = ['']
        self.pWordNodeList = [[]]
        self.replacements = {}
    def add(self, word):
        wordNodes = super(Dawg, self).add(word)
        for pWord, pWordNodes in zip(self.pWords, self.pWordNodeList):
            self.minimize(pWord, pWordNodes, word, wordNodes)
        self.pWords.append(word)
        self.pWordNodeList.append(wordNodes)
    
    def minimize(self, pWord, pWordNodes, word, wordNodes):
        pre, preN = cPrefix(word, pWord)
        suf, sufN1, sufN2 = cSuffix(word, pWord)
        if pre is not None and pWordNodes:
            #print("presynthesizing", pWord, word)
            self.synth(wordNodes[preN], pWordNodes[preN])
        if suf is not None and pWordNodes:
            #print("sufsynthesizing", pWord, word)
            self.synth(wordNodes[sufN1], pWordNodes[sufN2])
            
    def synth(self, node1, node2):
        #link node2.prev to node1
        for catalyst in node2.catalysts():
            node2.prev.addAction(catalyst, node1, force=True)
        #add node2's actions to node1
        for node2_action, nodeTo in node2.actions.items():
            nodeTo.prev = node1
            if node2_action in node1.actions:
                node1_subaction = node1.actions[node2_action]
                for node2_subaction, nodeTo_sub in nodeTo.actions.items():
                    node1_subaction.addAction(node2_subaction, nodeTo_sub, force=True)           
            else:
                node1.addAction(node2_action, nodeTo, force=True)
        self.replacements[node2] = node1
        #self.update({node2: node1})

    def update(self, replacements):
        for nodes in self.pWordNodeList:
            for node in nodes:
                node.update(replacements)

    

if __name__ == "__main__":
    lex = ["CAR", "CARS", "CAT", "CATS", "DO", "DOG", "DOGS", "DONE", "EAR", "EARS", "EAT", "EATS"]                           
    t = Dawg()
    for w in lex:
        t.add(w)
        #\t.minimize()
        #input(t)
        #print(t)
    t.update(t.replacements)
    print(t)
    #print(t.acceptable("EAT"))
    #print(list(filter(lambda i:i.id==47, t.nodes))[0].getactions())
    #for i in range(len(t.nodes)):
 #   for i in range(1):
 #       t.pathgen()
 #       t.minimize()
        #input(t)
    #for n in t.deletednodes:
 #       pass
        #t.nodes.append(n)
    #print(t)
    #print(t.replacements)
    for w in lex:
        print(w, t.parse(w), t.acceptable(w))
    #print(list(filter(lambda i:i.id==47, t.nodes))[0].getactions())
    ##print(t.parse("CAR"))
    ##print(t.parse("DOG"))

    ##import random
    ##s = "ACDEGORST"
    ##for i in range(100):
    ##    q=''.join(random.sample(s, random.choice([3, 4])))
    ##    print(q, t.acceptable(q))
