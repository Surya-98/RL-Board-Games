import chess
import numpy as np



class chessutils():
	
	def __init__(self):
		self.plane_b = {'r': 0, 'n': 1, 'b': 2, 'k': 3, 'q': 4, 'p': 5,
			'R': 6, 'N': 7, 'B': 8, 'K': 9, 'Q': 10, 'P': 11}

		self.plane_w = {'R': 0, 'N': 1, 'B': 2, 'K': 3, 'Q': 4, 'P': 5,
			'r': 6, 'n': 7, 'b': 8, 'k': 9, 'q': 10, 'p': 11}

		self.states = {}	


	def getInitialBoard(self): 
		board = chess.Board()
		self.states = {}
		return board

	def getAllactions(self):
		return 73*8*8

	def move(self,board,val,current_player) :
		# decoder to map action index to uci format
		# make move
		# val is 0 -> 8*8*73
		# 73 -> 56 (queen moves): 7 squares* 8 directions, 8 knight moves,
		# 9 underpromotions: 3 ways* 3 pieces
		# print("Action number : " + str(val))
		move_from_row = int(val/8)%8+1
		move_from_col = val % 8
		pick = move_from_col + (move_from_row-1)*8
		# print(move_from_col, move_from_row)
		move_from = chess.FILE_NAMES[move_from_col]+str(move_from_row)
		move_to_e = int(val/64)
		# print(move_to_e)

		if(board.turn):
			i = 1  
		else:
			i = -1 # depends on black or white
		if move_to_e < 56:
			# start from left and go clockwise
			direction = int(move_to_e/7)
			num = move_to_e%7 +1
			# print(direction, num)
			if(direction == 0):
				move_to_row = move_from_row
				move_to_col = move_from_col-num*i
			elif(direction == 1):
				move_to_row = move_from_row+num*i
				move_to_col = move_from_col-num*i
			elif(direction == 2):
				move_to_row = move_from_row+num*i
				move_to_col = move_from_col
			elif(direction == 3):
				move_to_row = move_from_row+num*i
				move_to_col = move_from_col+num*i
			elif(direction == 4):
				move_to_row = move_from_row
				move_to_col = move_from_col+num*i
			elif(direction == 5):
				move_to_row = move_from_row-num*i
				move_to_col = move_from_col+num*i
			elif(direction == 6):
				move_to_row = move_from_row-num*i
				move_to_col = move_from_col
			elif(direction == 7):
				move_to_row = move_from_row-num*i
				move_to_col = move_from_col-num*i

			if ((move_from_row == 7) and str(board.piece_at(pick)) == 'P'):
				move_to = chess.FILE_NAMES[move_to_col]+str(move_to_row)+'q'
			elif ((move_from_row == 2) and str(board.piece_at(pick)) == 'p'):
				move_to = chess.FILE_NAMES[move_to_col]+str(move_to_row)+'q'
			else:
				move_to = chess.FILE_NAMES[move_to_col]+str(move_to_row)
		elif move_to_e >= 56 and move_to_e < 64:
			# start from left and go clockwise knight moves
			if(move_to_e == 56):
				move_to_row = move_from_row+1*i
				move_to_col = move_from_col-2*i
			elif(move_to_e == 57):
				move_to_row = move_from_row+2*i
				move_to_col = move_from_col-1*i
			elif(move_to_e == 58):
				move_to_row = move_from_row+2*i
				move_to_col = move_from_col+1*i
			elif(move_to_e == 59):
				move_to_row = move_from_row+1*i
				move_to_col = move_from_col+2*i
			elif(move_to_e == 60):
				move_to_row = move_from_row-1*i
				move_to_col = move_from_col+2*i
			elif(move_to_e == 61):
				move_to_row = move_from_row-2*i
				move_to_col = move_from_col+1*i
			elif(move_to_e == 62):
				move_to_row = move_from_row-2*i
				move_to_col = move_from_col-1*i
			elif(move_to_e == 63):
				move_to_row = move_from_row-1*i
				move_to_col = move_from_col-2*i
			move_to = chess.FILE_NAMES[move_to_col]+str(move_to_row)
		else:
			# start from left
			dec = move_to_e - 64
			choice = int(dec/3)
			direction = dec % 3
			if (choice == 0):
				choice = 'r'
			elif (choice == 1):
				choice = 'n'
			elif (choice == 2):
				choice = 'b'
			# board.push_san('a1=Q') Move.from_uci('b2a1n')
			if(direction == 0):
				move_to_row = move_from_row+1*i
				move_to_col = move_from_col-1*i
			elif(direction == 1):
				move_to_row = move_from_row+1*i
				move_to_col = move_from_col
			elif(direction == 2):
				move_to_row = move_from_row+1*i
				move_to_col = move_from_col+1*i
			# print(move_to_col)
			move_to = chess.FILE_NAMES[move_to_col]+str(move_to_row)+choice
		move = move_from + move_to  # uci format
		# print("Corresponding move : " + str(move))
		board.push(chess.Move.from_uci(move))
		k = board.turn
		if k ==0:
			k = -1
		return board, k

	def encoder(self, board, move):

		move_from = move[:2]
		move_from_c = chess.FILE_NAMES.index(move_from[0])+1
		move_from_r = int(move_from[1])
		move_from_i = chess.SQUARE_NAMES.index(move_from)
		move_to = move[2:4]
		move_to_c = chess.FILE_NAMES.index(move_to[0])+1
		move_to_r = int(move_to[1])
		move_to_i = chess.SQUARE_NAMES.index(move_to)
		z=0
		if(len(move)==5):
			pp = move[4]
			if pp=='r' or pp=='n' or pp=='b' :
				if(pp=='r'):
					p1 = 0
				elif(pp=='n'):
					p1 = 1
				elif(pp=='b'):
					p1 = 2
				
				z = 1
				if((move_to_c-move_from_c)==-1):
					p2 = 0
				elif((move_to_c-move_from_c)==0):
					p2 = 1
				elif((move_to_c-move_from_c)==1):
					p2 = 2
				if(board.turn):
					index_to = 64 + 3*p1+ p2
				else:
					index_to = 64 + 3*p1 +(2-p2)

		if((str(board.piece_at(move_from_i)) == 'n' or str(board.piece_at(move_from_i)) == 'N')and z==0):
			index_to = 0
			if(move_to_c-move_from_c)==-2 and (move_to_r-move_from_r)==1:
				index_to = 0
			elif(move_to_c-move_from_c)==-1 and (move_to_r-move_from_r)==2:
				index_to = 1
			elif(move_to_c-move_from_c)==1 and (move_to_r-move_from_r)==2:
				index_to = 2
			elif(move_to_c-move_from_c)==2 and (move_to_r-move_from_r)==1:
				index_to = 3
			elif(move_to_c-move_from_c)==2 and (move_to_r-move_from_r)==-1:
				index_to = 4
			elif(move_to_c-move_from_c)==1 and (move_to_r-move_from_r)==-2:
				index_to = 5
			elif(move_to_c-move_from_c)==-1 and (move_to_r-move_from_r)==-2:
				index_to = 6
			elif(move_to_c-move_from_c)==-2 and (move_to_r-move_from_r)==-1:
				index_to = 7
			if(board.turn):
				index_to = 56 + index_to
			else:
				index_to = 56 + (index_to+4)%8

		elif z==0:
			step_r = move_to_r-move_from_r
			step_c = move_to_c-move_from_c

			if((step_c<0) and (step_r==0)):
				direction = 0
				step = -step_c
			elif((step_c>0) and (step_r==0)):
				direction = 4
				step = step_c
			elif((step_r>0) and(step_c==0)):
				direction = 2
				step = step_r
			elif((step_r<0) and (step_c==0)):
				direction = 6
				step = -step_r
			elif(step_r>0 and step_c>0):
				direction = 3
				step = step_r
			elif(step_r>0 and step_c<0):
				direction = 1
				step = step_r
			elif(step_r<0 and step_c<0):
				direction = 7
				step = -step_r
			elif(step_r<0 and step_c>0):
				direction = 5
				step = -step_r

			# print(step, direction)
			if(board.turn):
				index_to = step-1 + 7*direction
			else:
				index_to = step-1 + 7*((direction+4)%8)

		index = []
		index.append(move_from_c-1)
		index.append(move_from_r-1)
		index.append(index_to)		
		return index


	def getValidMoves(self, board) :
		valid = np.zeros([73,8,8])
		for i in board.legal_moves:
			a = self.encoder(board,str(i))
			# print(str(i))
			# print(a)
			valid[a[2]][a[1]][a[0]] = 1
		valid = valid.reshape(-1)
		# print(np.where(valid==1))
		return valid

	def isStateTerminal(self,board,current_player) : 
		
		if(board.is_game_over()):
			res = board.result()
			if(res == '1/2-1/2'):
				k = -1e-4
			elif(res == '1-0' and current_player==1):
				k = 1
			elif(res == '0-1' and current_player==1):
				k = -1
			elif(res == '0-1' and current_player==-1):
				k = 1
			elif(res == '1-0' and current_player==-1):
				k = -1
		else :
			k = 0
		return k

	def getUniversalboard(self, board_list, current_player):

		# black = 0, white = 1
    	# current player is P1
		# need to add repetitions
		pos = np.zeros([8*(12+1)+7, 8, 8])
		state_val = np.zeros([7, 8, 8])
		count = 0
		for i1 in range(8):
			# 0-colour, 1-move_count, 2,3,(k,q) -black castling, 4,5,(K,Q) - white castling, 6- no progress count
			board = board_list[i1]

			if(board.epd() in self.states):
				self.states[board.epd()] +=1
				count = self.states[board.epd()]
			else:
				self.states[board.epd()] =1
				count = 1

			pos[8*i1+12] = np.ones([8,8])*count

			for i in range(64):
				x = i%8
				y = int(i/8)
				if(str(board.piece_at(i))!='None'):
					if(board.turn):
						pos[8*i1 + self.plane_w[str(board.piece_at(i))]][7-y][x] = 1
					else:
						pos[8*i1 + self.plane_b[str(board.piece_at(i))]][y][7-x] = 1
		
		

		board = board_list[-1]

		if (board.turn):
			state_val[0] = np.ones([8, 8])
		else:
			state_val[0] = np.zeros([8, 8])

		for i in range(8):
			for j in range(8):
				state_val[1][i][j] = board.fullmove_number

		for i in range(8):
			for j in range(8):
				state_val[6][i][j] = board.halfmove_clock

		if (board.has_kingside_castling_rights(0)):
			state_val[2] = np.ones([8, 8])

		if (board.has_queenside_castling_rights(0)):
			state_val[3] = np.ones([8, 8])

		if (board.has_kingside_castling_rights(1)):
			state_val[4] = np.ones([8, 8])

		if (board.has_queenside_castling_rights(1)):
			state_val[5] = np.ones([8, 8])			
		pos[-7:] = state_val
		return pos
		
	def getStringboard(self,board) :
		return board.epd(hmvc=board.halfmove_clock, fmvc=board.fullmove_number)


