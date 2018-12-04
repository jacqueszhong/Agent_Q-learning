# -*- coding: utf-8 -*

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, backend
from keras.utils.generic_utils import get_custom_objects
import numpy as np

from constant import *

import gym #pip install gym
import time

DEBUG = 0

def centered_sigmoid(x):
	""" Customized activation function """
	return (backend.sigmoid(x)) - 0.5

class AgentBrain :

	#Number of neurons
	_nbInput = 145
	_nbHidden = 10
	_nbOutput = 1

	_reward_sum = 0

	#Tunable parameters
	_T_inv = 20 # Inverse of temperature
	_T_inv_max = 60 # Max value of the inverse of temperature
	_discount = 0.9 
	_momentum = 0.9 # Momentum factor of the backpropagation algorithm
	_lr = 0.3 # Learning rate of the backpropagation algorithm
	_r_w = 0.1 # Range of the initial weights

	_no_learning = False

	_input_vectors = []


	def __init__(self):
		print("Initialization of AgentBrain")
		if DEBUG:	
			self._nbInput = 5
			self._nbHidden = 10
			self._nbOutput = 2


		#Model of utility network
		self.model = tf.keras.Sequential()

		get_custom_objects().update({'centered_sigmoid': layers.Activation(centered_sigmoid)})
		self.model.add(layers.Activation(centered_sigmoid))

		#self.model.add(layers.InputLayer(batch_input_shape=(1,self.nbInput)) )
		self.model.add(layers.Dense(self._nbInput, input_dim=self._nbInput, activation='linear'))
		self.model.add(layers.Dense(self._nbHidden, activation=centered_sigmoid) ) 
		self.model.add(layers.Dense(self._nbOutput,activation='linear') )

		sgd = optimizers.SGD(lr = self._lr, momentum = self._momentum)

		self.model.compile(loss='mae', optimizer='sgd', metrics=['mae'])


	""" NN save/load functions """
	def save(self, name):
		start = time.time()
		self.model.save(name)
		print("Save time : " + str(time.time() - start))

	def load(self, name):
		start = time.time()
		self.model = models.load_model(name)
		print("Load time : " + str(time.time() - start))


	def savew(self, name):
		start = time.time()
		self.model.save_weights(name)
		print("Save time : " + str(time.time() - start))

	def loadw(self, name):
		start = time.time()
		self.model.load_weights(name)
		print("Load time : " + str(time.time() - start))

	def reset(self):
		self._no_learning = False
		self._T_inv = 20
		self._input_vectors = []
		self._reward_sum = 0

	def reset_no_learning(self):
		self._no_learning = True
		self._T_inv = 20
		self._input_vectors = []
		self._reward_sum = 0


	def predict(self,vec):
		"""
		Wrapper for the model.predict
		"""
		vec = np.array([vec])
		print("Predicting : {0} \n {1}".format(len(vec),vec))

		return self.model.predict(vec)
		#return 0.1

	def add_reward(self,reward):
		self._reward_sum += reward

	""" Functions for input representation processing """
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
			ref_array = SENSOR_X + SENSOR_O + SENSOR_Y 
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
			vec = (self.rotate_sensors(0,input_vec[:53],angle)) #Food sensors
			vec += (self.rotate_sensors(1,input_vec[53:85],angle)) #Enemy sensors
			vec += (self.rotate_sensors(2,input_vec[85:125],angle)) #Obstacle sensors
			vec += list(input_vec[125:]) #Energy, previous choice, collision

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
		if not self._input_vectors : #Input vectors have already been computed in adjust_network of the previous step
			self._input_vectors = self.compute_input_vectors(input_vec)
		#print("vectors : {0} ".format(self._input_vectors))
		for vec in self._input_vectors :
			merits.append(self.predict(vec))

		if self._no_learning :
			# Choose action with maximum merit
			self._action = np.argmax(merits)

		else : 
			# Choose action with a stochastic selector
			sum = 0.0
			for m in merits :
				sum += np.exp(m*T_inv)

			proba = []
			for m in merits :
				proba.append( np.exp(m*T_inv)/sum )

			print("merits proba : {0}".format(proba))
			self._action = int( np.random.choice(4, 1, p=proba) )
		return self._action


	def adjust_network(self, new_input_vec, reward):
		"""
		Adjusts the utility network of the agent after one simulation step.

		This is the second step of the Q learning process.

		:param new_input_vec:
		:param reward:

		"""

		prev_input_vec = self._input_vectors[self.action] #save for now the input representation of the previous state and action

		merits = []
		self._input_vectors = compute_input_vectors(new_input_vec)
		for vec in self._input_vectors :
			merits.append(self.predict(vec))

		target = reward + self._discount * np.max(merits)
		self._reward_sum += reward

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
				input_vec = np.identity(5)[s:s + 1]
				print(input_vec)
				print(type(input_vec))
				target_vec = self.model.predict(input_vec)[0]
				target_vec[a] = target
				# On lance un tour d'apprentissage, avec en entrée l'état s, de label target_vec.
				# model.fit devrait calculer l'erreur entre la sortie du NN (utilité estimée avant action) et l'utilité après action (target_vec)
				#, puis faire la backpropagation de cette erreur.
				self.model.fit(np.identity(5)[s:s + 1], target_vec.reshape(-1, 2), epochs=1, verbose=0)
				
				s = new_s
				r_sum += r
			r_avg_list.append(r_sum / 1000.0) #L'environnement NChain se termine après 1000 tours.

		print(r_avg_list)

if DEBUG:
	brain = AgentBrain()
	#brain.loadw('test_tuto.h5')
	brain.test_tuto()
	brain.savew('test_tuto_w.h5')


"""
#Piste intégration d'AgentBrain

#Init
brain = AgentBrain()
nb_simu = 300

if do_load : 
	brain.load("simu.h5")

#Tour du simulateur
for i in range(nb_simu):
	brain.reset()
	x = env.reset()
	
	while( not dead):
		a = brain.select_action(x)
		(y,r,dead) = env.step(a)
		brain.adjust_network(y,r)

	brain.save("simu.h5")

	#Test de l'agent sur les 50 environnements de test
	if(nb_simu % 20):
		for j in range(50):
			brain.reset_no_learning()
			x = env.reset()

			while( not dead ):
				a = brain.select_action()
				(y,r,dead) = env.step(a)

			

"""