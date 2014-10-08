# -*- coding: utf-8 -*-

from __future__ import division   
import matplotlib.pyplot as plt 
import random 
import numpy as np 

class Player:
    
    def __init__(self, state, gain_matrix):
        self.state = state
        self.gain_matrix = gain_matrix   

    def play(self, circle):

        position = circle.players.index(self)

        act_dist = circle.action_distribution(N, m)[position]

        payoff_vec = np.dot(self.gain_matrix, act_dist)

        if payoff_vec[0] > payoff_vec[1] and payoff_vec[0] > payoff_vec[2]:
            action = 0
        elif payoff_vec[1] >= payoff_vec[0] and payoff_vec[1] > payoff_vec[2]:
            action = 1
        else:
            action = 2

        return action


class Local_Interaction:

    def __init__(self, N, positions_1, positions_2):
        self.players = [Player(0, gain_matrix) for i in range(N)]
        for i in positions_1:
            self.players[i] = Player(1, gain_matrix)
        for i in positions_2:
            self.players[i] = Player(2, gain_matrix)
        self.current_state()

    def current_state(self):
        self.state_1 = []
        self.state_2 = [] 
        for player in self.players:
            self.state_1.append(1 if player.state == 1 else 0)
            self.state_2.append(1 if player.state == 2 else 0)
        
        return np.array([self.state_1, self.state_2])

    def action_distribution(self, N, m):

        adj_matrix = np.zeros((N, N))             #両隣と対戦する様にしました。
        adj_matrix[N-1,0], adj_matrix[N-1,N-2] = 1, 1
        for i in range(N-1):
            adj_matrix[i, i-1], adj_matrix[i, i+1] = 1, 1

        current_state = self.current_state().T
    
        num_ops_1_2 = np.dot(adj_matrix, current_state)

        act_dists = []
        for num_op_1, num_op_2 in num_ops_1_2:
            act_dists.append([(m-num_op_1-num_op_2)/m, num_op_1/m, num_op_2/m])
            
        return act_dists

    def update(self):
        actions = []
        for player in self.players:
            actions.append(player.play(circle))
        for i, player in enumerate(self.players):
            player.state = actions[i]


N = 15 
m = 2 #num_opponent 
q = 1/7
p = 2/7
gain_matrix = np.array([[q, 0, 0], [0, p, 0], [0, 0, 1-q-p]])
T = 20 
positions_1 = [3]
positions_2 = [7]

circle = Local_Interaction(N, positions_1, positions_2) 
transition_1 = []
transition_2 = []

for i in range(T): 
    count_1 = circle.state_1.count(1)
    count_2 = circle.state_2.count(1)
    transition_1.append(count_1)
    transition_2.append(count_2)
    circle.update()

plt.plot(transition_1, label="action transition_1")
plt.plot(transition_2, label="action transition_2")
plt.legend() 
plt.show() 
