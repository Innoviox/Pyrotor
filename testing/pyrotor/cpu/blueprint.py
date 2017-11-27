from time import time

class BlueprintBase():
    def __init__(self, moves, rack):
        self.setMoves(moves)
        self.rack = rack
       
    def setMoves(self, moves):
        self.moves = filter(bool, moves)
		
    def pick(self):
        bestMove = None
        #a=0
        #t_=0
        for move in self.moves:
            #t=time()
            if bestMove is None or self.score(move) > self.score(bestMove):
                bestMove = move
            #t_+=time()-t
            #a+=1
        #t_/=a
        #print(t_, a, t_*a)
        if self.score(bestMove) > 0: #lol
            return bestMove
        return None
    
    def assureAttrs(self, move):
        try:
            move.score
        except AttributeError:
            move.getScore()
            
        try:
            move.valuation
        except AttributeError:
            move.getEvaluation(self.rack)
            
        return move
		
    def score(self, move):
        #function to be overriden
        move = self.assureAttrs(move)
        return move.score * 1 + move.valuation * 1

class WeightedScorer(BlueprintBase):
    def __init__(self, moves, rack, score_weight, val_weight):
        super().__init__(moves, rack)
        self.score_weight, self.val_weight = score_weight, val_weight

    def score(self, move):
        move = self.assureAttrs(move)
        return move.score * self.score_weight + move.valuation * self.val_weight


class LookAhead(BlueprintBase):
    def __init__(self, moves, rack, bag):
        super().__init__(moves)
        self.rack = rack
        self.bag = bag

    def score(move):
        #function to be overriden
        player = CPU(real=(False, rack), distribution=bag)
        opponent = CPU(real=(False, rack), distribution=bag)
        for person in [player, opponent]:
            person.board = move.board
        
        scene = []
        move = player._run()
        
        opponent.distributon = player.distribution
        
        return move.score * 3 + move.valuation * 2    
