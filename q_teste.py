from classes.shogi import Shogi
from classes.shogi_mdp import ShogiMDP
from classes.q_learning import Qlearning

shogi = Shogi()
mdp = ShogiMDP(shogi)
qlearn = Qlearning(problema=mdp, desconto=0.9, alpha=0.1)
Q, PI = qlearn.calcular_tabela_q(estado_inicial=0,n_passos=5000)

#Defina o estado do jogo: Represente o estado atual do jogo de 
# forma que o agente possa utilizá-lo para tomar decisões. 
# Isso pode ser feito através de um vetor ou matriz que codifique a posição das peças, 
# o jogador atual, etc.

#classe que movimenta a peça -> shogi

#Defina as ações: Identifique todas as ações possíveis que o agente pode realizar em cada estado do jogo, 
# como mover peças, capturar peças, etc.

# -> shogi_copy.move_piece(position) 
# -> shogi.promote_piece(piece)
# -> shogi.drop_piece(drop, piece)

# Inicialize a tabela Q: Crie uma tabela Q que armazene os valores Q para cada par estado-ação.
# Os valores Q representam a recompensa esperada de realizar uma determinada ação em um determinado estado.

# -> ???????????????