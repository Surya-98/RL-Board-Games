# Python Final Project
# Connect Four
#
# Erik Ackermann
# Charlene Wang
#
# Play connect four
# February 27, 2012

from connect4_minimax import *
from c4utils import c4utils
from net import NetworkWrapper as netw

num_games = 100
def main():
	""" Play a game!
	"""
	count = 0
	c4_utils = c4utils()
	network = netw(500)
	network.loadweights("wt_best.pth.tar")
	network.eval()
	
	print("Should Player 1 be a Minimax(Benchmark) or Monte-Carlo(Our program)?")
	choice = 'x'

	win_counts = [0, 0, 0] # [p1 wins, p2 wins, ties]
	g = Game(c4_utils, network, 1500, choice)
	
	for i in range(num_games) :
		print("Game number : ",i)
		g.newGame()
		g.printState()
		player1 = g.players[0]
		player2 = g.players[1]
		exit = False
		while not exit:
			while not g.finished:
				g.nextMove()
			
			g.findFours()
			g.printState()
			
			if g.winner == None:
				win_counts[2] += 1
			
			elif g.winner == player1:
				win_counts[0] += 1
				
			elif g.winner == player2:
				win_counts[1] += 1
			exit = True
			printStats(player1, player2, win_counts)
			# time.sleep(0.5)
			while True:
				if count < num_games : 
					play_again = 'y'
					count += 1
				else : 
					play_again = 'n'

				
				if play_again.lower() == 'y' or play_again.lower() == 'yes': 
					g.newGame()
					g.printState()
					break
				elif play_again.lower() == 'n' or play_again.lower() == 'no':
					print("Thanks for playing!")
					exit = True
					break
				else:
					print("I don't understand... "),
		
def printStats(player1, player2, win_counts):
	print("{0}: {1} wins, {2}: {3} wins, {4} ties".format(player1.name,
		win_counts[0], player2.name, win_counts[1], win_counts[2]))
		
if __name__ == "__main__": # Default "main method" idiom.
	main()
