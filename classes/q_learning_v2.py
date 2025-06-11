import random
import pickle
import os
import time

class QLearning:
    def __init__(
        self,
        problem,
        discount = 0.90,
        tetha = 1e-6,
        alpha = 0.1, 
        e = 0.4
    ):
        self.problem = problem
        self.theta = tetha
        self.alpha = alpha
        self.discount = discount
        self.e = e
        
        self.load_tables()
    
    def load_tables(self):
        if os.path.exists("data/q_table.pkl") and os.path.exists("data/policy.pkl"):
            print("\033[33mArquivos existentes encontrados. \nCarregando tabelas...")
            with open("data/q_table.pkl", "rb") as f:
                self.Q_TABLE = pickle.load(f)
            with open("data/policy.pkl", "rb") as f:
                self.PI = pickle.load(f)
            print("Tabelas carregadas com sucesso. \nIniciando treinamento...\n\033[0m")
        else:
            print("\033[33mNenhum arquivo encontrado. \nIniciando tabelas do zero...")
            self.Q_TABLE = {}   
            self.PI = {}  
            print("Iniciando treinamento....\n\033[0m")

    def save_tables(self):
        print("\n\033[33mSalvando tabelas...\033[0m")
        
        with open("data/q_table.pkl", "wb") as file:
            pickle.dump(self.Q_TABLE, file)

        with open("data/policy.pkl", "wb") as file:
            pickle.dump(self.PI, file)
        print("\033[33mTabelas salvas com sucesso!\n\033[0m")

    def calculate_table_q(self, initial_state, max_step=1, max_limit=10000):
        step = 0
        start_time = time.time()

        while step < max_step:
            step+=1
            state = initial_state
            limit = 0
            print(f"\n\033[37mIniciando novo jogo ({step}/{max_step})...\033[0m")   
            if self.problem.game_over:
                self.problem.restart()

            while self.problem.game_over == False and limit < max_limit:
                limit+=1

                self.problem.process_states()
                action = self.choose_next_action(state)

                if state not in self.Q_TABLE:
                    self.Q_TABLE[state] = {}

                if action not in self.Q_TABLE[state]:
                    self.Q_TABLE[state][action] = 0.0  

                old_q = self.Q_TABLE[state][action]
                next_q = 0

                for next_state, prob in self.problem.T(state, action):
                    next_q += self.new_q(state, action, next_state, prob)
                
                self.Q_TABLE[state][action] = self.alpha * old_q + (1 - self.alpha) * next_q

                self.PI[state] = max(self.Q_TABLE[state], key=self.Q_TABLE[state].get)

                state = self.choose_next_state(state, action)
                self.problem.next_state(action)
            if step % 100 == 0:
                self.save_tables()

        self.save_tables()
        end_time = time.time()
        elapsed = end_time - start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        print(f"\033[32mTempo de execução: {hours}h{minutes}m{seconds}s.")
        return self.Q_TABLE, self.PI
    
    def choose_next_action(self, state):
        random_action = random.choice(self.problem.actions)
        if state not in self.PI:
            return random_action
        policy_action = self.PI[state]
        next_action = random.choices([random_action, policy_action], weights=[self.e, (1-self.e)])[0]
        return next_action
    
    def choose_next_state(self, state, action):
        next_states = self.problem.T(state, action)
        states = []
        probs = []
        for next_state, prob in next_states:
            states.append(next_state)
            probs.append(prob)
            
        if sum(probs) <= 0:
            return random.choice(states)
        chosen_state = random.choices(states, weights=probs)[0]
        return chosen_state

    def new_q(self, state, action, next_state, prob):
        max_q = max(self.Q_TABLE[state].values())
        return prob * (self.problem.R(state, action, next_state) + self.discount * max_q)
