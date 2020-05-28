from training import train_class
from c4utils import c4utils
from net import NetworkWrapper as netw
from search import mcts
num_sim = 1000
epochs = 4
self_play = 5
compete = 4
def main() :
	print("Loading c4")
	c4_utils = c4utils()
	print("Initializing network")
	network = netw(epochs)
	network.loadweights("wt_best.pth.tar")
	print("loading trainer")
	tr = train_class(network, self_play, epochs, c4_utils, compete, num_sim)
	tr.nnet_learning()

if __name__=="__main__" :
	main()
