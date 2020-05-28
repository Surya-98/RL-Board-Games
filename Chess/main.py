from training import train_class
from chessutils import chessutils
from net import NetworkWrapper as netw
from search import mcts
num_sim = 30
epochs = 500
self_play = 6
compete = 4
def main() :
	print("Loading chess engine")
	chess_utils = chessutils()
	print("Initializing network")
	network = netw(epochs)
	network.loadweights("wt_best.pth.tar")
	print("loading trainer")
	tr = train_class(network, self_play, epochs, chess_utils, compete, num_sim)
	tr.nnet_learning()

if __name__=="__main__" :
	main()
