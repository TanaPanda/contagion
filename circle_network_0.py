# -*- coding: utf-8 -*-
 
from __future__ import division   
import matplotlib.pyplot as plt 
import random 
import numpy as np 

class Player:

    def __init__(self, state, q):
        self.state = state
        self.gain_matrix = np.array([[q, 0], [0, 1-q]])   
      
    def action_distribution(self, N, m, players):
      
        adj_matrix = np.zeros((N, N))             #両隣と対戦する様にしました。
        adj_matrix[N-1,0], adj_matrix[N-1,N-2] = 1, 1
        for i in range(N-1):
            adj_matrix[i, i-1], adj_matrix[i, i+1] = 1, 1
        
        current_state = [player.state for player in players]
        
        num_op_state_1 = np.dot(adj_matrix, current_state)
        
        position = players.index(self)
        
        act_dist = [(m-num_op_state_1[position])/m, num_op_state_1[position]/m]
        
        return act_dist

    def play(self):

        act_dist = self.action_distribution(N, m, players)
                                
        payoff_vec = np.dot(self.gain_matrix, act_dist)
                                
        if payoff_vec[0] > payoff_vec[1]:
            action = 0
        elif payoff_vec[0] == payoff_vec[1]:
            action = random.choice([0, 1])
        else:
            action = 1

        return action

    def update_player(self):
        
        action = self.play()

        self.state = action


def count_action(players):
   
    actions = []
   
    for player in players:
        actions.append(player.state)

    return actions.count(1)

num_state_0 = 15
num_state_1 = 1
N = num_state_0 + num_state_1
m = 2    #num_opponent
q = 1/3
T = 200

players = [Player(0, q) for i in range(num_type_0)]
players_1 = [Player(1, q) for i in range(num_type_1)]
for player_1 in players_1:
   players.insert(randint(0, num_type_0), player_1)

transition = []

for t in range(T):
    transition.append(count_action(players))
    #print [player.action_distribution(N, m, players) for player in players]
    i = randint(0, N-1)
    players[i].update_player()


plt.plot(transition, label="action transition")
plt.legend()
plt.show()
