# -*- coding: utf-8 -*

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
import numpy as np

from constant import *

import gym #pip install gym
import time

class AgentBrain :

	#Number of neurons
	nbInput = 5
	nbHidden = 10
	nbOutput = 2

	#Tunable parameters
	T_inv = 20 # Inverse of temperature
	T_inv_max = 60 # Max value of the inverse of temperature
	discount = 0.9 
	momentum = 0.9 # Momentum factor of the backpropagation algorithm
	lr = 0.3 # Learning rate of the backpropagation algorithm
	r_w = 0.1 # Range of the initial weights


	def __init__(self):
		print("Initialization of AgentBrain")

		#Model of utility network
		self.model = tf.keras.Sequential()
		#self.model.add(layers.InputLayer(batch_input_shape=(1,self.nbInput)) )
		self.model.add(layers.Dense(self.nbInput, input_dim=self.nbInput, activation='linear'))
		self.model.add(layers.Dense(self.nbHidden, activation='sigmoid') ) 
		self.model.add(layers.Dense(self.nbOutput,activation='linear') )

		sgd = optimizers.SGD(lr = self.lr, momentum = self.momentum)

		self.model.compile(loss='mae', optimizer='sgd', metrics=['mae'])


	""" NN save/load functions """
	def save(self, name):
		start = time.time()
		self.model.save(name)
		print("Save time : " + str(time.time() - start))

	def load(self, name):
		start = time.time()
		#self.model = models.load_model(name)
		print("Load time : " + str(time.time() - start))


	def savew(self, name):
		start = time.time()
		self.model.save_weights(name)
		print("Save time : " + str(time.time() - start))

	def loadw(self, name):
		start = time.time()
		self.model.load_weights(name)
		print("Load time : " + str(time.time() - start))


	def predict(self,vec):
		print("predicted")
		return 0.1

	def rotate_sensors(self,sensor_arr_type, sensor_arr_vec, angle):
		""" 
		Rotates the input representation of the sensor array
		(algo général mais un peu lourd)
		
		:param sensor_arr_type: Type of sensor. 0 = food, 1 = enemy, 2 = obstacle
		:param sensor_arr_ vec: Input representation of the sensor array
		:param angle: Rotation angle of the sensor array, counterclockwise. Possible values : 90,180,270
		:return: Rotated input representation of the sensor array
		
		"""

		if sensor_arr_type == 0 :
			ref_array = SENSOR_X + SENSOR_O + sensor_Y 
		elif sensor_arr_type == 1 :
			ref_array = SENSOR_X + SENSOR_O
		elif sensor_arr_type == 2 :
			ref_array = SENSOR_o
		else :
			print("ERROR : unknown sensor_arr_type n°" + str(sensor_arr_type))

		if angle == 90:
			rot_mat = [[0,-1],[1,0]]
		elif angle == 180:
			rot_mat = [[-1,0],[0,-1]]
		elif angle == 270:
			rot_mat = [[0,1],[-1,0]]
		else :
			print("ERROR : unknown angle value = " + str(angle))

		rot_array = np.dot(ref_array,rot_mat)

		rot_vec = []
		for pos in rot_array :
			ind = ref_array.index(list(pos))
			rot_vec.append(sensor_arr_vec[ind])

		return rot_vec

	def compute_input_vectors(self, input_vec):
		"""
		Gives the input representation in the four directions (N,E,S,W)

		:param input_vec: input representation, current state of the agent 
		:return: a list of the input representation in each direction 
		"""

		input_vectors = []
		input_vectors.append(input_vec)

		angle = 0
		for i in range(1,4):
			angle += 90
			vec = []
			vec.append(rotate_sensors(0,input_vec[:53],angle)) #Food sensors
			vec.append(rotate_sensors(1,input_vec[53:85],angle)) #Enemy sensors
			vec.append(rotate_sensors(2,input_vec[85:125],angle)) #Obstacle sensors
			vec.append(input_vec[125:]) #Energy, previous choice, collision

			input_vectors.append(vec)

		return input_vectors



	def select_action(self, input_vec):
		"""
		Chooses the action to perform.

		This is the first step of the Q learning process. It evaluates the utility of each possible action. 
		Then, a stochastic selector computes the probability of each action to be elected, based on its utility and the temperature. 
		
		:param input_vec: input representation, current state of the agent
		:return: selected action

		"""

		# Compute utilities
		merits = []
		self.input_vectors = compute_input_vectors(input_vec) #surement redondant 
		for vec in self.input_vectors :
			merits.append(self.predict(vec))

		# Choose action with a stochastic selector
		sum = 0.0
		for m in merits :
			sum += np.exp(m*T_inv)

		proba = []
		for m in merits :
			proba.append( np.exp(m*T_inv)/sum )

		self.action = int( np.random.choice(4, 1, p=proba) )
		return self.action


	def adjust_network(self, new_input_vec, reward):
		"""
		Adjusts the utility network of the agent after one simulation step.

		This is the second step of the Q learning process.

		:param new_input_vec:
		:param reward:

		"""

		prev_input_vec = self.input_vectors[self.action] #save for now the input representation of the previous state and action

		merits = []
		self.input_vectors = compute_input_vectors(new_input_vec)
		for vec in self.input_vectors :
			merits.append(self.predict(vec))

		target = reward + self.discount * np.max(merits)

		# try to fit the utilities before and after performing the action.
		self.model.fit(prev_input_vec,target, epochs=1, verbose=0)





	def test_tuto(self):
		# now execute the q learning
		y = 0.95 # discount
		eps = 0.5
		decay_factor = 0.999 #Taux de diminution du epsilon
		r_avg_list = []
		nb_simu = 10

		env = gym.make('NChain-v0')
		env.reset()


		for i in range(nb_simu):
			s = env.reset() # Reset de l'environnement, donne l'état s initial
			eps *= decay_factor #s Sélecteur d'action epsilon-greedy. Joue le même rôle que la température, cad gère la préférence entre exploration/exploitation
			if i % 1 == 0:
				print("Episode {} of {}".format(i + 1, nb_simu))
			done = False
			r_sum = 0
			while not done:
				if np.random.random() < eps: 
					#Au départ, l'agent choisit une action au hasard avec une proba de 0.5. 
					#A chaque tour, on diminue de 0.001 cette proba. L'agent explorera moins avec le nombre de simulations effectuées.
					a = np.random.randint(0, 2)
				else:
					# Le réseau peut avoir plusieurs sorties, une par action. On prend l'action ayant la plus forte activation.
					# 'predict' mange un vecteur (taille = nbInput) et renvoie un vecteur (taille = nbOutput)
					a = np.argmax(self.model.predict(np.identity(5)[s:s + 1])) 

				new_s, r, done, _ = env.step(a)

				# Calcul de récompense du nouvel état
				target = r + y * np.max(self.model.predict(np.identity(5)[new_s:new_s + 1]))
				
				# On construit le vecteur de sortie attendu target_vec
				target_vec = self.model.predict(np.identity(5)[s:s + 1])[0]
				target_vec[a] = target
				# On lance un tour d'apprentissage, avec en entrée l'état s, de label target_vec.
				# model.fit devrait calculer l'erreur entre la sortie du NN (utilité estimée avant action) et l'utilité après action (target_vec)
				#, puis faire la backpropagation de cette erreur.
				self.model.fit(np.identity(5)[s:s + 1], target_vec.reshape(-1, 2), epochs=1, verbose=0)
				
				s = new_s
				r_sum += r
			r_avg_list.append(r_sum / 1000.0) #L'environnement NChain se termine après 1000 tours.

		print(r_avg_list)




brain = AgentBrain()
#brain.load('test_tuto.h5')
brain.test_tuto()
brain.save('test_tuto.h5')


