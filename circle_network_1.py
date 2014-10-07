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

        if payoff_vec[0] > payoff_vec[1]:
            action = 0
        elif payoff_vec[0] == payoff_vec[1]:
            action = random.choice([0, 1])
        else:
            action = 1

        return action


class Local_Interaction:

    def __init__(self, N, positions_1):
        self.players = [Player(0, gain_matrix) for i in range(N)]
        for i in positions_1:
            self.players[i] = Player(1, gain_matrix)

    def current_state(self):

        return [player.state for player in self.players]

    def action_distribution(self, N, m):

        adj_matrix = np.zeros((N, N))             #両隣と対戦する様にしました。
        adj_matrix[N-1,0], adj_matrix[N-1,N-2] = 1, 1
        for i in range(N-1):
            adj_matrix[i, i-1], adj_matrix[i, i+1] = 1, 1

        cur_state = self.current_state()
    
        num_ops_state_1 = np.dot(adj_matrix, cur_state)

        act_dists = []
        for num_op_state_1 in num_ops_state_1:
            act_dists.append([(m-num_op_state_1)/m, num_op_state_1/m])
            
        return act_dists

    def update(self):
        actions = []
        for player in self.players:
            actions.append(player.play(self))
        for i, player in enumerate(self.players):
            player.state = actions[i]


N = 15 
m = 2 #num_opponent 
q = 1/3
gain_matrix = np.array([[q, 0], [0, 1-q]])
T = 20 
positions_1 = [3]

circle = Local_Interaction(N, positions_1) 
transition = []

for i in range(T): 
    counts = circle.current_state().count(1) 
    transition.append(counts) 
    circle.update()

plt.plot(transition, label="action transition") 
plt.legend() 
plt.show() 

