
from environment import *
import csv

class Simulator:

	#Useful paths for file manipulation
	save_path = "NN_save/"
	map_path="maps/"
	csv_path="csv/"
	train_map_path = map_path+"training/"
	test_map_path = map_path+"testing/"

	delay = 0.01

	def __init__(self):
		print("Initializing Simulator")
		self.env = Environment()


	def run_simulation(self, nomap = False, delay = delay):
		"""
		Run one simulation of the game
		"""
		game_state = 0
		while game_state == 0:
			if nomap == False :
				self.env.show()

			game_state = self.env.update_q()
			time.sleep(delay)


	def experiment_run(self,nb_train=300,nb_test=50,period_test=20, replay=False):
		save_path = self.save_path + "experimentrun/"
		mean_food = []
		std_food = []

		no_map = False

		try :
			self.env.load_nn(save_path + "quicksave.h5")
		except :
			print("Couldn't load last quicksave. Create new")
		time.sleep(1)

		step=0
		while (step<=nb_train):
			#Load corresponding map
			m = self.train_map_path+str(step)+".txt"
			self.env.load_map(m)
			print("Loaded : "+m)

			#Run one simulation turn
			if not replay:
				self.run_simulation(delay=0.0,nomap=no_map)

			#Save and reset
			name = "exp_step"+str(step)+"_"
			self.env.save_nn(save_path, name)
			self.env.reset()
			

			#Run tests every 'period_test' steps
			if (step % period_test == 0):
				food_array = np.zeros(nb_test)
				
				self.env.desactivate_learning()
				for i in range(0,nb_test):
					print("##Test "+str(i)+" of step "+str(step)+"##")
					
					#Load corresponding map
					m = self.test_map_path+str(i)+".txt"
					self.env.load_map(m)
					print("Loaded : "+m)
					#time.sleep(1)

					#Run one simulation turn
					self.run_simulation(delay=0.0,nomap=no_map)

					#Save and reset
					food_array[i] = (15-self.env.food_counter)
					self.env.reset()

					
				#Retrieve mean food
				self.env.activate_learning()
				print("Step="+str(step)+"Foods = "+str(food_array))
				mean_food.append(np.mean(food_array))
				std_food.append(np.std(food_array))
				time.sleep(2)

			step += 1


		self.toCSV2("exp",mean_food,std_food)

	def toCSV(self,name,mean_food):

		s = str(time.time())
		s = s.replace(".","")
		s = s[4:12]
		filename = self.csv_path+s+"_"+name+".csv"

		np.savetxt(filename,mean_food,fmt='%1.5f',delimiter=',')
		"""
		csvfile = open(filename, 'wb')

		csvwriter = csv.writer(csvfile,delimiter=',')
		print(str(type(mean_food)) + " and "+str(mean_food))
		csvwriter.writerow(mean_food)

		csvfile.close()
		"""

	def toCSV2(self,name,mean_food,std_food):

		s = str(time.time())
		s = s.replace(".","")
		s = s[4:12]
		filename = self.csv_path+s+"_"+name+".csv"

		arr = np.stack((mean_food,std_food))

		np.savetxt(filename,arr,fmt='%1.5f',delimiter=',')
		"""
		csvfile = open(filename, 'wb')

		csvwriter = csv.writer(csvfile,delimiter=',')
		print(str(type(mean_food)) + " and "+str(mean_food))
		csvwriter.writerow(mean_food)

		csvfile.close()
		"""


	def test_run(self, nbrun):
		save_path = self.save_path + "testrun/"
		try : #delete quicksave.h5 if you want to start from scratch
			self.env.load_nn(save_path + "quicksave.h5")
		except :
			print("Couldn't load last quicksave. Create new")

		step = 0
		while (step<nbrun):
			self.run_simulation(delay = 0.15)

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
			


