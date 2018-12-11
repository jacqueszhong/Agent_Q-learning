

from environment import *


class Simulator:

	#Useful paths for file manipulation
	save_path = "NN_save/"
	map_path="maps/"
	train_map_path = map_path+"training/"
	test_map_path = map_path+"testing/"

	def __init__(self):
		print("Initializing Simulator")
		self.env = Environment()


	def experiment_run(self):
		save_path = self.save_path + "experimentrun/"
		try :
			self.env.load_nn(save_path + "quicksave.h5")
		except :
			print("Couldn't load last quicksave. Create new")

		step=0
		while (step<nbrun):
			self.env.run_simulation(nomap = False, delay = 0.15)

			#Save neural networks (in case of crash)
			name = "exp_step"+str(step)+"_"
			self.env.save_nn(save_path, name)


			self.env.reset()
			step += 1		



	def test_run(self, nbrun):
		save_path = self.save_path + "testrun/"
		try : #delete quicksave.h5 if you want to start from scratch
			self.env.load_nn(save_path + "quicksave.h5")
		except :
			print("Couldn't load last quicksave. Create new")

		step = 0
		while (step<nbrun):
			self.env.run_simulation(nomap = False, delay = 0.15)

			#Save neural networks (in case of crash)
			name = "testrun_step"+str(step)+"_"
			self.env.save_nn(save_path, name)


			self.env.reset()
			step += 1

	def manual_run(self):
		env.run_manual()
		env.reset()

	def generate_maps(self,nb_train,nb_test):
		"""

		:param: map_file, file containing default map values
		:param: nb_train, number of training maps
		:param: nb_test, number of testing maps
		"""

		for i in range(0,nb_train):
			self.env.food_counter = 0
			print("Generating training map "+str(i))
			self.env.init_map()
			self.env.save_map(self.train_map_path+str(i)+".txt")

		for i in range(0,nb_test):
			print("Generating testing map "+str(i))
			self.env.food_counter = 0
			self.env.init_map()
			self.env.save_map(self.test_map_path+str(i)+".txt")
			


