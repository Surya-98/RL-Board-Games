import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import os
# from torchvision import transforms
# from torch.autograd import Variable
from pickle import Pickler, Unpickler


batch_size = 100

class Network_arch(nn.Module) :
	def __init__(self):
		super(Network_arch,self).__init__()
		self.conv1 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv2 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv3 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv4 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv5 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv6 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv7 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv8 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv9 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv10 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv11 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv12 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv13 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv14 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv15 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv16 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv17 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv18 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.conv19 = nn.Conv2d(111, 111, 3, stride=1, padding=1)
		self.conv20 = nn.Conv2d(111, 111, 3, stride=1, padding=1)

		self.bnorm1 = nn.BatchNorm2d(111)
		self.bnorm2 = nn.BatchNorm2d(111)
		self.bnorm3 = nn.BatchNorm2d(111)
		self.bnorm4 = nn.BatchNorm2d(111)
		self.bnorm5 = nn.BatchNorm2d(111)
		self.bnorm6 = nn.BatchNorm2d(111)
		self.bnorm7 = nn.BatchNorm2d(111)
		self.bnorm8 = nn.BatchNorm2d(111)
		self.bnorm9 = nn.BatchNorm2d(111)
		self.bnorm10 = nn.BatchNorm2d(111)

		self.fc1 = nn.Linear(111*8*8,1024)
		self.bnorm11 = nn.BatchNorm1d(1024)

		self.fc2 = nn.Linear(1024,1024)
		self.bnorm12 = nn.BatchNorm1d(1024)

		self.fc3 = nn.Linear(1024,8*8*73)

		self.fc4 = nn.Linear(1024,1)

	def forward(self,t) :
		
		t1 = F.relu(self.bnorm1(self.conv2(self.conv1(t))))
		t = t1 + t
		t1 = F.relu(self.bnorm2(self.conv4(self.conv3(t))))
		t = t1 + t
		t1 = F.relu(self.bnorm3(self.conv6(self.conv5(t))))
		t = t1 + t 
		t1 = F.relu(self.bnorm4(self.conv8(self.conv7(t))))
		t = t1 + t 
		t1 = F.relu(self.bnorm5(self.conv10(self.conv9(t))))
		t = t1 + t 
		t1 = F.relu(self.bnorm6(self.conv12(self.conv11(t))))
		t = t1 + t 
		t1 = F.relu(self.bnorm7(self.conv14(self.conv13(t))))
		t = t1 + t 
		t1 = F.relu(self.bnorm8(self.conv16(self.conv15(t))))
		t = t1 + t 
		t1 = F.relu(self.bnorm9(self.conv18(self.conv17(t))))
		t = t1 + t 
		t1 = F.relu(self.bnorm10(self.conv20(self.conv19(t))))
		t = t1 + t
		t = t.reshape(t.shape[0],-1)
		t = self.bnorm11(self.fc1(t))
		t = self.bnorm12(self.fc2(t))

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
			if self.total_epochs%100 == 0:
				print("Training epoch number : "+str(epoch))
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
