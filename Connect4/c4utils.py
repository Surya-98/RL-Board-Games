import numpy as np



class c4utils():

	def __init__(self, row=6, column=7):
		self.column = 7
		self.row = 6
		self.states = {}
		self.turn = 0

	def getStringBoard(self, board):
		return str(board)

	def getInitialBoard(self): 
		board = np.zeros([self.row,self.column])
		self.states = {}
		self.turn = 0
		return board

	def getAllactions(self):
		return self.column
	

	def move(self, board, val, current_player):

		for i in range(self.row):
			if(board[self.row-i-1][val]==0):
				# print("HI")
				board[self.row-i-1][val] = current_player
				self.turn += 1
				return board, -current_player

	def getValidMoves(self, board):
		valid = np.zeros([self.column])
		for i in range(self.column):
			if(board[0][i]==0):
				valid[i] = 1
		return valid

	def isStateTerminal(self, board, k):
		for i in range(self.column-3):
			for j in range(self.row):
				if(board[j][i]==-k and board[j][i+1]==-k and board[j][i+2]==-k and board[j][i+3]==-k):
					return -1
		for i in range(self.column):
			for j in range(self.row-3):
				if(board[j][i]==-k and board[j+1][i]==-k and board[j+2][i]==-k and board[j+3][i]==-k):
					return -1
		for i in range(self.column-3):
			for j in range(self.row-3):
				if(board[j][i]==-k and board[j+1][i+1]==-k and board[j+2][i+2]==-k and board[j+3][i+3]==-k):
					return -1
		for i in range(3,self.column):
			for j in range(self.row-3):
				if(board[j][i]==-k and board[j+1][i-1]==-k and board[j+2][i-2]==-k and board[j+3][i-3]==-k):
					return -1 
		
		count = 0
		for i in range(self.column) : 
			if board[0][i] != 0 :
				count += 1
		if count==self.column :
			return -0.0005

		else : 	
			return 0

	def getUniversalboard(self, board, current_player):

		state = np.zeros([2, self.row, self.column])
		# print("Visual Board")
		# print(board)
		for i in range(self.row):
			for j in range(self.column):
				if(board[i][j]==current_player):
					state[0][i][j] = 1
				elif(board[i][j]!=0):
					state[1][i][j] = 1
		# print("State Network input")
		# print(state)
		return state.reshape((84,1))


	def print_board(self,board) : 
		print(board)