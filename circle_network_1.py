# -*- coding: utf-8 -*-

from __future__ import division   
import matplotlib.pyplot as plt 
import random 
import numpy as np 
import networkx as nx

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
        else:
            action = 1

        return action


class Local_Interaction:

    def __init__(self, N, positions_1):
        self.players = [Player(0, gain_matrix) for i in range(N)]
        for i in positions_1:
            self.players[i] = Player(1, gain_matrix)
        self.current_state()

    def current_state(self):
        self.state_1 = []
        for player in self.players:
            self.state_1.append(1 if player.state == 1 else 0)
        
        return self.state_1

    def action_distribution(self, N, m):

        adj_matrix = np.zeros((N, N))             #両隣と対戦する様にしました。
        adj_matrix[N-1,0], adj_matrix[N-1,N-2] = 1, 1
        for i in range(N-1):
            adj_matrix[i, i-1], adj_matrix[i, i+1] = 1, 1

        current_state = self.current_state()
    
        num_ops_1 = np.dot(adj_matrix, current_state)

        act_dists = []
        for num_op_1 in num_ops_1:
            act_dists.append([(m-num_op_1)/m, num_op_1/m])
            
        return act_dists

    def update(self):
        actions = []
        for player in self.players:
            actions.append(player.play(self))
        for i, player in enumerate(self.players):
            player.state = actions[i]


N = 15 
m = 2 #num_opponent 
p = 1/3
gain_matrix = np.array([[p, 0], [0, 1-p]])
T = 20 
positions_1 = [3]

circle = Local_Interaction(N, positions_1) 
transition_1 = []

for i in range(T): 
    count_1 = circle.state_1.count(1)
    transition_1.append(count_1)
    circle.update()

plt.plot(transition_1, label="action transition_1")
plt.legend()
plt.show()


G = nx.Graph()
for i in range(N-1):
    G.add_edge(i, i+1, {"weight":10})
G.add_edge(0, N-1, {"weight":10})

pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, node_size=300, node_color="w")
nx.draw_networkx_edges(G, pos, width=1)
nx.draw_networkx_labels(G, pos ,font_size=13, font_color="r")

plt.xticks([])
plt.yticks([])
plt.show() 
