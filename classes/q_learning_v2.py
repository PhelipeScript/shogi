import random

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
        
        self.Q_TABLE = {}
        self.PI = {}

    def calculate_table_q(self, initial_state, max_step=1, max_limit=2):
        step = 0

        while step < max_step:
            if self.problem.game_over:
                print(f'\n\n\n\n\n CAlaABREZO\n\n\n\n\n\n')
                self.problem.restart()
            step+=1
            state = initial_state
            limit = 0
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

        return self.Q_TABLE, self.PI
    
    def choose_next_action(self, state):
        random_action = random.choice(self.problem.actions)
        if state not in self.PI:
            return random_action
        policy_action = self.PI[state]
        next_action = random.choices([random_action, policy_action], weights=[self.e, (1-self.e)])[0]
        # print("------------------------------")
        # print(f"proxima ação tomada {next_action}")
        return next_action
    
    def choose_next_state(self, state, action):
        next_states = self.problem.T(state, action)
        states = []
        probs = []
        for next_state, prob in next_states:
            states.append(next_state)
            probs.append(prob)
        chosen_state = random.choices(states, weights=probs)[0]
        # print("------------------------------")
        # print(f"estado selecionado {chosen_state}")
        return chosen_state

    def new_q(self, state, action, next_state, prob):
        max_q = max(self.Q_TABLE[state].values())
        # print(f"MAIOR AÇÇÃO{max_q}")
        return prob * (self.problem.R(state, action, next_state) + self.discount * max_q)
