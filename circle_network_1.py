# -*- coding: utf-8 -*-
 
from __future__ import division   
import matplotlib.pyplot as plt 
import random 
import numpy as np 

class Player:

    def __init__(self, state, q):
        self.state = state
        self.gain_matrix = np.array([[q, 0], [0, 1-q]])   
      
    def action_distribution(self, N, m, circle):
      
        adj_matrix = np.zeros((N, N))             #両隣と対戦する様にしました。
        adj_matrix[N-1,0], adj_matrix[N-1,N-2] = 1, 1
        for i in range(N-1):
            adj_matrix[i, i-1], adj_matrix[i, i+1] = 1, 1
        
        current_state = [player.state for player in circle.players]
        
        num_op_state_1 = np.dot(adj_matrix, current_state)
        
        position = circle.players.index(self)
        
        act_dist = [(m-num_op_state_1[position])/m, num_op_state_1[position]/m]
        
        return act_dist

    def play(self):

        act_dist = self.action_distribution(N, m, circle)
                                
        payoff_vec = np.dot(self.gain_matrix, act_dist)
                                
        if payoff_vec[0] > payoff_vec[1]:
            action = 0
        elif payoff_vec[0] == payoff_vec[1]:
            action = random.choice([0, 1])
        else:
            action = 1

        return action
    
class Local_Interaction:
    
    def __init__(self, N, num_1):
        self.players = [Player(0, q) for i in range(N)]
        self.first_action(num_1)
        
    def first_action(self, num_1):
        position_1 = np.random.randint(0, len(self.players), num_1) 
        for i in position_1:
            self.players[i] = Player(1, q)
            
        return self.players
            
    def current_state(self):
        actions = []
        for player in self.players:
            actions.append(player.play())
            
        return actions
    
    def update(self):
        actions = self.current_state()
        for i, player in enumerate(self.players):
            player.state = actions[i]

num_0 = 14
num_1 = 1
N = num_0 + num_1
m = 2    #num_opponent
q = 1/3

circle = Local_Interaction(N, num_1) 
transition = [1]

while 1:
    no_one_moved = True
    old_location = circle.current_state()
    counts = old_location.count(1)
    transition.append(counts)
    circle.update()
    if circle.current_state() != old_location:
        no_one_moved = False
    if no_one_moved:
        break
        
plt.plot(transition, label="action transition")
plt.legend()
plt.show()         
