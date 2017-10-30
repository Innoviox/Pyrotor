class Node:
    _id = 0
    def __init__(self, prev, end=False):
        self.id = Node._id
        Node._id += 1
        self.prev = prev
        self.end = end
        self.actions = {}
        
    def addAction(self, action, nodeTo):
        if action not in self.actions:
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
        
    def _reachable(self):
        #print("iterating on", self)
        if self.end:
            return []
        nodes = [self]
        #print(self.actions)
        for action, node in self.actions.items():
            #print("\taccessing", node)
            nodes.extend(node._reachable())
        return nodes
        
    def reachable(self):
        n = self._reachable()
        n = list(filter(lambda i: i is not self, n))
        return n

    def path(self):
        #print("pathing", self)
        i=self.backtrace()
        i.extend(self.reachable())
        return i

    def catalysts(self):
        if self.prev is not None:
            return list(self.prev.actionlead(self))
        return None

    def actionlead(self, node):
        for action, nodeTo in self.actions.items():
            if nodeTo is node:
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
        super(Dawg, self).__init__()
        
        
    def add(self, word):
        print("adding", word)
        super(Dawg, self).add(word)
        self.minimize()
        
        
    def minimize(self):
        deleted = []
        cantdelete=[]
        for node in self.nodes:
            for node2 in self.nodes:
                if node2 not in deleted and node2 not in node.path():
                    #print("Cycling", node, node2, "\n", sep="\n\t")
                
                    for action, nodeTo in node.actions.copy().items():
                        if action in node2.actions and action != "!":
                            p=node.prev
                            #print(p)
                            #print("\tCycling", node, node2, "\n", sep="\n\t")
                            if p.catalysts() == node2.prev.catalysts():
                                for c_action in node2.catalysts():
                                    #print("\tpreadding", c_action)
                                    
                                        p.actions[c_action] = node
                            else:
                                pass
                                #print("\t\tpreadd stopped", p.catalysts(), node2.catalysts())
                            #print(p)
                            for n_action, nodeTo in node2.actions.items():
                                #print("a\t", node, node2, nodeTo, n_action, sep="\n\t")
                                #print("\tpostadding", n_action, nodeTo)
                                if node.prev.catalysts() == nodeTo.prev.catalysts():
                                    if n_action not in node.actions:
                                        #print("\t\tpoa2")
                                        node.addAction(n_action, nodeTo)
                                    else:
                                        _node = node.actions[n_action]
                                        for _n_action, _nodeTo in nodeTo.actions.items():
                                            #print("\t\t\tpoa3", _n_action, _nodeTo)
                                            _node.addAction(_n_action, _nodeTo)
                            if node2 not in cantdelete:
                                deleted.append(node2)
                                cantdelete.extend(node2.path())
                                cantdelete.append(node2)

                    if not node.onlyEnd() and node.ame() == node2.ame():
                        
                        same = True
                        for ((action1, nodet1), (action2, nodet2)) in zip(node.actions.copy().items(), node2.actions.copy().items()):
                            if nodet1.ame() != nodet2.ame():
                                same = False
                        if same:
                            p=node.prev
                            for c_action in node2.catalysts():
                                p.actions[c_action] = node
                            if node not in self.replacements.keys() and node not in self.replacements.values():
                               self.replacements[node2] = node
        for node in self.nodes:
            node.update(self.replacements)
            
        for node in deleted:
            self.nodes.remove(node)
            self.deletednodes.append(node)

lex = ["CAR", "CARS", "CAT", "CATS","DO", "DOG", "DOGS", "DONE", "EAR", "EARS", "EAT", "EATS"]                           
t = Dawg()
for w in lex:
    t.add(w)
    #input(t)
    #print(t)
#print(t.acceptable("EAT"))
for n in t.deletednodes:
    t.nodes.append(n)
print(t)
for w in lex:
    print(t.acceptable(w))
print(t.acceptable("EO"))
print(t.parse("CA"))
print(t.parse("DO"))
print(t.start.actions.keys())
