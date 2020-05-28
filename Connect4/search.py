import numpy as np
import math
import torch
import time
import copy

class mcts : 
	def __init__(self, c4_utils, network, exp, total_sims) : 
		self.policy = {}
		self.value = {}
		self.state_count = {}
		self.stateAction_count = {}
		self.valid_moves = {}
		self.Q = {}
		self.terminal_states = {}
		self.c4_utils = c4_utils
		self.network = network
		self.exploration_param = exp
		self.total_sims = total_sims

	def reset_tree(self) : 
		self.policy = {}
		self.value = {}
		self.state_count = {}
		self.stateAction_count = {}
		self.valid_moves = {}
		self.Q = {}
		self.terminal_states = {}
		

	def get_policy(self, state, player) : 

		for i in range(self.total_sims) : 
			state_copy = copy.deepcopy(state)
			self.search(state_copy,player)
		
		max_actions = self.c4_utils.getAllactions()
		state_string = self.c4_utils.getStringBoard(state)
		

		policy = [self.stateAction_count[(state_string,action)] if (state_string,action) in self.stateAction_count else 0 for action in range(max_actions)]

		policy = np.asarray(policy) / np.sum(policy)
		
		return policy

	def search(self, state, player) : # state must be a string
		
		board_universal = self.c4_utils.getUniversalboard(state,player)
		
		state_string = self.c4_utils.getStringBoard(state)

		if state_string not in self.terminal_states : 
			self.terminal_states[state_string] = self.c4_utils.isStateTerminal(state,player)
		if self.terminal_states[state_string] != 0 : 
			return -self.terminal_states[state_string]

		if state_string not in self.policy :
			p, v = self.network.forward(torch.FloatTensor((np.expand_dims(board_universal, axis=0)).astype(np.float64)))
			valid_moves = self.c4_utils.getValidMoves(state)
		
			p_valid = p.detach().numpy()*valid_moves
			p_sum = np.sum(p_valid)

			if p_sum > 0 : 
				p_valid /= p_sum
			else : 
				p_valid += valid_moves
				p_sum = np.sum(p_valid)
				p_valid /= p_sum

			self.policy[state_string] = p_valid
			self.valid_moves[state_string] = valid_moves

			self.value[state_string] = v
			self.state_count[state_string] = 0

			return -v

		best_utility = -float('inf')
		best_action = 0

		for action in range(len(self.valid_moves[state_string])) :	# iterate over all moves
			if self.valid_moves[state_string][action] == 1 : 
				if (state_string,action) in self.Q : 
					utility = self.Q[(state_string,action)] + self.exploration_param * self.policy[state_string][0][action] * \
													math.sqrt(self.state_count[state_string]) / (1 + self.stateAction_count[(state_string,action)])
				else : 
					utility = self.exploration_param * self.policy[state_string][0][action] * math.sqrt(self.state_count[state_string] + 1e-6) # small positive value

				if utility > best_utility :
					best_action = action
					best_utility = utility

		next_state, player = self.c4_utils.move(state,best_action,player)
		state_copy = copy.deepcopy(next_state)
		v = self.search(state_copy,player)

		if (state_string,best_action) in self.Q : 
			self.Q[(state_string,best_action)] = (v + self.stateAction_count[(state_string,best_action)]*self.Q[(state_string,best_action)])/(1 + self.stateAction_count[(state_string,best_action)]) # average
			self.stateAction_count[(state_string,best_action)] += 1
		else : 
			self.Q[(state_string,best_action)] = v
			self.stateAction_count[(state_string,best_action)] = 1

		self.state_count[state_string] += 1
		return -v

	def get_move(self,state,player) : 
		board = np.zeros((6,7))
		for i in range(6) : 
			for j in range(7) :
				if state[i][j]==' ' :
					board[5-i][j] = 0
				elif state[i][j] == 'x' : 
					board[5-i][j] = 1
				elif state[i][j] == 'o' :
					board[5-i][j] = -1
		if player == 'x' : 
			player = 1
		else :
			player = -1

		policy = self.get_policy(board,player)
		move = np.argmax(policy)
		return move

