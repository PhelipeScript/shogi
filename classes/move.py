class Move:
  def __init__(self, piece, origin, destination):
    self.piece = piece
    self.origin = origin
    self.destination = destination
    
  def execute(self):
    # executa o movimento
    pass
  
  def capture(self):
    # captura uma peça
    pass

  def check_promotion(self):
    # verifica se a peça pode ser promovida
    pass
  
  def promote(self):
    # promove uma peça
    pass
  