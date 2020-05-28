import numpy as np
import math
import random
import net
from compete import Compete
from search import mcts
import os
import time
from pickle import Pickler, Unpickler
import pickle

class train_class :
	def __init__(self,network,num_selfplay,epochs,c4_utils,num_competitions, num_sim_) :
		self.num_sim = num_sim_
		self.network = network
		self.c4_utils = c4_utils
		self.network_old = self.network.__class__(epochs)
		self.mcts = mcts(self.c4_utils,self.network,1.5,self.num_sim)
		self.num_selfplay = num_selfplay
		self.epochs = epochs
		self.num_competitions = num_competitions
		self.training_examples_all = []
		self.update_threshold = 0.5
		self.example_num = 0

	def selfplay(self):
		board = self.c4_utils.getInitialBoard()
		player = 1
		turns = 0
		game_progress = []
		
		
		while True : 
			turns += 1
			board_universal = self.c4_utils.getUniversalboard(board,player)
			mcts_policy = self.mcts.get_policy(board, player)
			action = np.random.choice(7,p=mcts_policy)		# randomly chosen proportional to a probability for exploration/exploitation
			game_progress.append([board_universal,mcts_policy,player,action])

			board, player = self.c4_utils.move(board, action, player)
			time.sleep(2)
			result = self.c4_utils.isStateTerminal(board,player)


			if result !=0 :
				print("      Total moves : " , turns, " Result : ", result)
				return [(a[0],a[1],result*((-1)**(player!=a[2]))) for a in game_progress]

	def nnet_learning(self) :
		memory_size = 2000
		self.network.eval()
		for e in range(self.epochs) :
			print("Epoch : " + str(e))

			self.num_sim = self.num_sim + e*5
			if self.num_sim > 300 : 
				self.num_sim = 300

			for s in range(self.num_selfplay) :
				print("    Game number : "+str(s))
				self.training_examples_all.extend(self.selfplay())
				self.save_examples(self.example_num)
				self.example_num += 1
				self.training_examples_all = []
				self.mcts = mcts(self.c4_utils, self.network, 1.5,self.num_sim)
				self.c4_utils.turn = 0

			print("    End of self play")
			
			self.network.train()

			self.network.saveweights(filename = 'wt_temp.pth.tar')
			self.network_old.loadweights(filename = 'wt_temp.pth.tar')

			net_old_mcts = mcts(self.c4_utils, self.network_old, 1.5,self.num_sim)
			
			training_examples = self.load_examples(self.example_num)
			self.network.train_net(training_examples)

			training_examples = []

			net_mcts = mcts(self.c4_utils, self.network, 1.5,self.num_sim)
			self.network.eval()
			self.network_old.eval()
			
			c = Compete(net_old_mcts, net_mcts, self.c4_utils)
			print("    Competition")
			net_old_win, net_win, draw = c.play(self.num_competitions)
			print("    New network wins : %d, Old network wins : %d, Draw : %d "%(net_win, net_old_win, draw))
			if(net_old_win>net_win): 
				print("    Rejecting new model")
				self.network.loadweights(filename='wt_temp.pth.tar')
			else : 
				self.network.saveweights(filename='wt_best.pth.tar')



	def save_examples(self,iterat) : 
		print("Saving examples. Iter : " + str(iterat))
		folder = './examples/'
		if not os.path.exists(folder) : 
			os.mkdir(folder)

		filename = os.path.join(folder,'checkpoint_'+str(iterat)+'.examples')
		with open(filename,"wb+") as f :
			Pickler(f).dump(self.training_examples_all)
		f.closed

	def load_examples(self,iterat) :
		folder = './examples/'
		example_list = []
		if iterat > 50 : 
			starting_example = iterat - 50
		else : 
			starting_example = 0
		for i in range(starting_example,iterat) :
			infile = open(folder+'checkpoint_'+str(i)+'.examples','rb')
			example = pickle.load(infile)
			example_list.extend(example)

		infile.close()
		return example_list


