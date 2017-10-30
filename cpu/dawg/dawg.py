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

    def process(self, action):
        if action not in self.actions:
            return False
        return self.actions[action]

    def __repr__(self):
        return str(self.id) + " " + str(self.actions)
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
                return Node(None, False)
        return node
    
    def acceptable(self, actions):
        return '!' in self.parse(actions).actions
    
    def __str__(self):
        return str(self.nodes)
        
class Trie:
    def __init__(self):
        self.nodes = Automata()

    def add(self, word):
        w = word + "!"
        node = self.nodes.start
        for to in w:
            end = to == "!"
            node = self.nodes.add(node, to, end=end)

t = Trie()
t.add("HI")
t.add("HELLO")
print(t.nodes)
print(t.nodes.acceptable("HE"))
"""
add(_, c)
add(c, a)
add(a, r)
add(r, !, end=True)

add(_, c)
add(c, a)
add(a, r)
add(r, s)




_1: c:_2, e:_2, d:_6
_2: a:_3
_3: r:_4, t:_4
_4:es:_5
_5:e
_6: o:_7
_7:eg:_4,n:_8
_8: e:_5
"""
