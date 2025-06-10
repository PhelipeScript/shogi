from classes.shogi import Shogi
from classes.shogi_mdp_v2 import ShogiMDP_v2
from classes.q_learning_v2 import QLearning

shogi = Shogi()
mdp = ShogiMDP_v2(shogi)
qlearn = QLearning(problem=mdp, discount=0.9, alpha=0.1)
initial_state = ''.join(mdp.game.board.board_str) + ("W" if mdp.game.who_plays_now.color == "WHITE" else "B")
Q, PI = qlearn.calculate_table_q(initial_state=initial_state,max_step=5000)



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
