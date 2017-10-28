class BlueprintBase():
    def __init__(self, moves, rack):
        self.setMoves(moves)
        self.rack = rack
       
    def setMoves(self, moves):
        self.moves = filter(lambda move: move is not False, moves)
		
    def pick(self):
        bestMove = None
        for move in self.moves:
            if bestMove is None or self.score(move) > self.score(bestMove):
                bestMove = move
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
