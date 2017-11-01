def inDict(item, d):
    return item in d.keys() or item in d.values()
class Node:
    _id = 0
    def __init__(self, prev, end=False):
        self.id = Node._id
        Node._id += 1
        self.prev = prev
        self.end = end
        self.actions = {}
        
    def addAction(self, action, nodeTo, force=False):
        #print(self.coolstr())
        #print("adding action", action)
        #print("\t", nodeTo.coolstr())
        if force or action not in self.actions:
            self.actions[action] = nodeTo

    def getactions(self):
        return list(self.actions.keys())

    def ame(self):
        return list(filter(lambda i: i != "!", self.getactions()))

    def onlyEnd(self):
        return len(self.ame()) == 0
    
    def process(self, action):
        if action not in self.actions:
            return False
        return self.actions[action]

    def __repr__(self):
        return " ".join(map(str, (self.id, self.catalysts(), self.getactions())))

    def backtrace(self):
        node=self
        path=[]
        while node is not None:
            path.append(node)
            node=node.prev
        return path

    def _backtrace(self, nodes):
        b=None
        for node in nodes:
            a=node.backtrace()
            if self in a:
                b = a
        return b
    
    def _reachable(self):
        if self.end:
            return []
        nodes = [self]
        for action, node in self.actions.items():
##            _node = node
##            while not _node.end:
##                nodes.append(_node)
                
            nodes.extend(node._reachable())
        return nodes
        
    def reachable(self):
        n = self._reachable()
        n = list(filter(lambda i: i is not self, n))
        return n

    def path(self, nodes):
        i=self._backtrace(nodes)
        i.extend(self.reachable())
        return i

    def catalysts(self):
        if self.prev is not None:
            return list(self.prev.actionlead(self))
        return [None]

    def actionlead(self, node):
        for action, nodeTo in self.actions.items():
            if nodeTo.id == node.id:
                yield action
                
    def coolstr(self):
        s = ""
        s += "{} <= {}\n".format(str(self), self.prev.id if self.prev is not None else "None")
        for action, nodeTo in self.actions.items():
            s += "\t{} => {} \n".format(action, str(nodeTo))
        return s

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
        nodeTo = Node(nodeFrom, end=end)
        if action not in nodeFrom.actions:
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
        w = word
        node = self.start
        for to in w:
            node = super(Trie, self).add(node, to)
        super(Trie, self).add(node, "!", end=True)
        
    def __str__(self):
        s = ""
        for node in sorted(self.nodes, key=lambda i:i.id):
            s += node.coolstr()
        return s
    
class Dawg(Trie):
    def __init__(self):
        self.deletednodes = []
        self.replacements = {}
        self.nodepaths = {}
        super(Dawg, self).__init__()       

    def pathgen(self):
        for node in self.nodes:
            self.nodepaths[node] = node.path(self.nodes)
    def minimize(self):
        minimized = []
        for node in self.nodes:
            for node2 in self.nodes:
                if node not in minimized and node.id != node2.id and node2 not in self.nodepaths[node] and node not in self.nodepaths[node2]:
                    for action, nodeTo in node.actions.copy().items():
                        if action in node2.actions:# and action != "!":
                            p = node.prev
                            p2 = node2.prev
                            if p is not None and p2 is not None and p.catalysts() == p2.catalysts():
                                for c_action in node2.catalysts():
                                    #if p.id == 2 and c_action in 'EOLR':
                                        #print("adding action {} from\n\t{} \nto \n\t{}".format(c_action, node2.coolstr(), p.coolstr()))
                                        #print("because of", action, node2.coolstr(), p.coolstr(), p2.coolstr(), node.coolstr(), sep="\n\t")
                                    p2.addAction(c_action, node)#, force=True)
                                for n_action, nodeTo in node2.actions.copy().items():
                                    if p.catalysts() == nodeTo.prev.catalysts():
                                        if n_action not in node.actions:
                                            #print("adding action {} from\n\t{} \nto \n\t{}".format(n_action, nodeTo.coolstr(), node.coolstr()))
                                            node.addAction(n_action, nodeTo, force=True)
                                        else:
                                            _node = node.actions[n_action]
                                            for _n_action, _nodeTo in nodeTo.actions.items():
                                                #print("adding action {} from\n\t{} \nto \n\t{}".format(_n_action, _nodeTo.coolstr(), _node.coolstr()))
                                                _node.addAction(_n_action, _nodeTo, force=True)

                    if not node.onlyEnd() and node.ame() == node2.ame():
                        same = True
                        for ((action1, nodet1), (action2, nodet2)) in zip(node.actions.copy().items(), node2.actions.copy().items()):
                            if nodet1.ame() != nodet2.ame():
                                same = False
                        if same:
                            p2=node2.prev
                            for c_action in node2.catalysts():
                                if c_action is not None:
                                    #print("adding action {} from\n\t{} \nto \n\t{}".format(c_action, node.coolstr(), p2.coolstr()))
                                    if c_action in p2.actions:
                                        p2.addAction(c_action, node, force=True)
                            for action, nodeTo in node2.actions.items():
                                if action in node.actions:
                                    nodeTo.prev = node
                                    #print("adding action {} from\n\t{} \nto \n\t{}".format(action, node2.coolstr(), node.coolstr()))
                                    if action in node.actions:
                                        node.addAction(action, nodeTo, force=True)
##                            self.replacements[node2] = node
            minimized.extend((node, node2))
##                    print(self.parse("AAH"))
##                    print(self.parse("AAL"))
##                    print(node.id, node2.id)
##                    input()
            
        for node in self.nodes:
            node.update(self.replacements)

if __name__ == "__main__":
    lex = ["CAR", "CARS", "CAT", "CATS", "DO", "DOG", "DOGS", "DONE", "EAR", "EARS", "EAT", "EATS"]                           
    t = Dawg()
    for w in lex:
        t.add(w)
        #\t.minimize()
        #input(t)
        #print(t)
    #print(t.acceptable("EAT"))
    print(list(filter(lambda i:i.id==47, t.nodes))[0].getactions())
    #for i in range(len(t.nodes)):
    for i in range(1):
        t.pathgen()
        t.minimize()
        #input(t)
    for n in t.deletednodes:
        pass
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
