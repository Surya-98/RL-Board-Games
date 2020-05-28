import numpy as np
import copy
import time
class Compete() :

	def __init__(self, player_1, player_2, chess_utils) :	# player1 - old network ; player2 - new network
		self.player_1 = player_1
		self.player_2 = player_2
		self.chess_utils = chess_utils

	def play(self, num) :
		switch_count = int(num/2)

		players = [self.player_2, None, self.player_1]
		p1_won = 0
		p2_won = 0
		draw = 0

		# print(switch_count)
		for i in range(switch_count) :
			# print("Player1 game no",i)
			state_list = []
			current_player = 1
			state = self.chess_utils.getInitialBoard()
			iteration = 0
			self.player_1.reset_tree()
			self.player_2.reset_tree()

			while (self.chess_utils.isStateTerminal(state,current_player) == 0) :
				iteration += 1

				if state_list == [] :
					state_list = [state] * 8

				state_list.append(state)

				if len(state_list) > 8 : 
					state_list.pop(0)
				board_universal = self.chess_utils.getUniversalboard(state_list,current_player)
				policy_player = players[current_player+1].get_policy(state_list, current_player)
				action = np.argmax(policy_player)

				valid_moves = self.chess_utils.getValidMoves(state)

				if valid_moves[action] == 0 : 
					print("Invalid move while competing")
					break 	######## ?
				else : 
					state, current_player = self.chess_utils.move(state,action,current_player)
					print(state)
					print(" ")

			result = self.chess_utils.isStateTerminal(state,current_player)
			# print(result)
			# time.sleep(2)

			if(result!=-1 and result!=1): 
				draw += 1
			elif(current_player==1):
				if result == 1: 
					p1_won += 1
				elif result == -1 : 
					p2_won += 1
			elif(current_player==-1):
				if result == 1: 
					p2_won += 1
				elif result == -1 : 
					p1_won += 1

		players = [self.player_1,None, self.player_2]

		for i in range(switch_count) :
			# print("Player1 game no",i)
			state_list = []
			current_player = 1
			state = self.chess_utils.getInitialBoard()
			iteration = 0
			self.player_1.reset_tree()
			self.player_2.reset_tree()

			while (self.chess_utils.isStateTerminal(state,current_player) == 0) :
				iteration += 1

				if state_list == [] :
					state_list = [state] * 8

				state_list.append(state)

				if len(state_list) > 8 : 
					state_list.pop(0)
				state_list_copy = copy.deepcopy(state_list)
				board_universal = self.chess_utils.getUniversalboard(state_list_copy,current_player)
				policy_player = players[current_player+1].get_policy(state_list_copy, current_player)
				action = np.argmax(policy_player)

				valid_moves = self.chess_utils.getValidMoves(state)

				if valid_moves[action] == 0 : 
					print("Invalid move while competing")
					break 	######## ?
				else : 
					state, current_player = self.chess_utils.move(state,action,current_player)
					print(state)
					print(" ")

			result = self.chess_utils.isStateTerminal(state,current_player)
			# print(result)
			# time.sleep(2)
			if(result!=-1 and result!=1): 
				draw += 1
			elif(current_player==1):
				if result == 1: 
					p2_won += 1
				elif result == -1 : 
					p1_won += 1
			elif(current_player==-1):
				if result == 1: 
					p1_won += 1
				elif result == -1 : 
					p2_won += 1

		return p1_won, p2_won, draw		