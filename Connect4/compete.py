import numpy as np
import copy
import time
class Compete() :

	def __init__(self, player_1, player_2, c4_utils) :	# player1 - old network ; player2 - new network
		self.player_1 = player_1
		self.player_2 = player_2
		self.c4_utils = c4_utils

	def play(self, num) :
		switch_count = int(num/2)

		players = [self.player_2, None, self.player_1]
		p1_won = 0
		p2_won = 0
		draw = 0

		for i in range(switch_count) :
			current_player = 1
			state = self.c4_utils.getInitialBoard()
			iteration = 0
			self.player_1.reset_tree()
			self.player_2.reset_tree()

			while (self.c4_utils.isStateTerminal(state,current_player) == 0) :
				iteration += 1
				state_copy = copy.deepcopy(state)
				board_universal = self.c4_utils.getUniversalboard(state_copy,current_player)
				policy_player = players[current_player+1].get_policy(state_copy, current_player)
				action = np.argmax(policy_player)

				valid_moves = self.c4_utils.getValidMoves(state_copy)

				if valid_moves[action] == 0 : 
					print("Invalid move while competing")
					break 	######## ?
				else : 
					state, current_player = self.c4_utils.move(state_copy,action,current_player)

			result = self.c4_utils.isStateTerminal(state,current_player)
			if(result!=-1 and result!=1): 
				draw += 1
			elif(current_player==1):
				if result == 1: 
					p1_won += 1
					print("Old network won")
				elif result == -1 : 
					p2_won += 1
					print("New network won")
			elif(current_player==-1):
				if result == 1: 
					p2_won += 1
					print("New network won")
				elif result == -1 : 
					p1_won += 1
					print("Old network won")

		players = [self.player_1,None, self.player_2]

		for i in range(switch_count) :
			current_player = 1
			state = self.c4_utils.getInitialBoard()
			iteration = 0
			self.player_1.reset_tree()
			self.player_2.reset_tree()

			while (self.c4_utils.isStateTerminal(state,current_player) == 0) :
				iteration += 1

				state_copy = copy.deepcopy(state)
				board_universal = self.c4_utils.getUniversalboard(state_copy,current_player)
				policy_player = players[current_player+1].get_policy(state_copy, current_player)
				action = np.argmax(policy_player)

				valid_moves = self.c4_utils.getValidMoves(state)

				if valid_moves[action] == 0 : 
					print("Invalid move while competing")
					break 	######## ?
				else : 
					state, current_player = self.c4_utils.move(state_copy,action,current_player)

			result = self.c4_utils.isStateTerminal(state,current_player)
			if(result!=-1 and result!=1): 
				draw += 1
			elif(current_player==1):
				if result == 1: 
					p2_won += 1
					print("New network won")
				elif result == -1 : 
					p1_won += 1
					print("Old network won")
			elif(current_player==-1):
				if result == 1: 
					p1_won += 1
					print("Old network won")
				elif result == -1 : 
					p2_won += 1
					print("New network won")

		return p1_won, p2_won, draw		