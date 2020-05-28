import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import os
from pickle import Pickler, Unpickler


batch_size = 100

class Network_arch(nn.Module) :
	def __init__(self, channel_size=2,board_row=6,board_col=7):
		super(Network_arch,self).__init__()
		self.fc10 = nn.Linear(84,42)
		self.fc11 = nn.Linear(42,21)
		
		self.bnorm11 = nn.BatchNorm1d(42)
		self.bnorm12 = nn.BatchNorm1d(21)

		self.fc3 = nn.Linear(21,board_col)

		self.fc4 = nn.Linear(21,1)

	def forward(self,t) :
		t = t.reshape(t.shape[0],-1)
		t = self.bnorm11(self.fc10(t))
		t = self.bnorm12(self.fc11(t))

		p = self.fc3(t)
		v = self.fc4(t)

		p = F.softmax(p,dim=1)
		v = torch.tanh(v)

		return p,v

class NetworkWrapper(Network_arch) : 
	def __init__(self,total_epochs) :
		super(NetworkWrapper,self).__init__()
		self.network = Network_arch()
		if torch.cuda.is_available() :
			print("Using CUDA")
			self.network.cuda()
		self.total_epochs = total_epochs

	def train_net(self,examples) :
		print("Training network")
		optimizer = optim.Adam(self.network.parameters())
		for epoch in range(self.total_epochs) :
			batch_count = int(len(examples)/batch_size)
			for bt in range(batch_count) :
				samples = np.random.randint(len(examples), size = batch_size) 
				state_list, pi_list, v_list = list(zip(*[examples[i] for i in samples]))
				state_array = torch.FloatTensor(np.array(state_list).astype(np.float64))
				pi_array = torch.FloatTensor(np.array(pi_list))
				v_array = torch.FloatTensor(np.array(v_list))

				if torch.cuda.is_available() : 
					state_array, pi_array, v_array = state_array.contiguous().cuda(), pi_array.contiguous().cuda(), v_array.contiguous().cuda()

				actual_pi, actual_v = self.network.forward(state_array)
				loss_pi = self.pi_loss(actual_pi, pi_array)
				loss_v = self.v_loss(actual_v, v_array)
				total_loss = loss_pi + loss_v

				optimizer.zero_grad()
				total_loss.backward()
				optimizer.step()

	def pi_loss(self,actual, target) :
		return -torch.sum(actual * target) / target.size()[0]

	def v_loss(self,actual, target) :
		return torch.sum((actual.view(-1)-target)**2) / target.size()[0]

	def saveweights(self,filename) :
		folder =  './weights/'
		if not os.path.exists(folder) : 
			os.mkdir(folder)
		torch.save(self.network.state_dict(), folder+filename)

	def loadweights(self,filename) :
		folder =  './weights/'
		self.network.load_state_dict(torch.load(folder+filename, map_location=torch.device('cpu')))

a = NetworkWrapper(10)
print(a.network)