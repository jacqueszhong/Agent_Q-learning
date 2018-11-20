# -*- coding: utf-8 -*

import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

import gym #pip install gym
import time

class AgentBrain :

	#Number of neurons
	nbInput = 5
	nbHidden = 10
	nbOutput = 2

	def __init__(self):
		print("Initiating UtilityNetwork")
		#Model of utility network
		self.model = tf.keras.Sequential()
		#self.model.add(layers.InputLayer(batch_input_shape=(1,self.nbInput)) )
		self.model.add(layers.Dense(self.nbInput, input_dim=self.nbInput, activation='linear'))
		self.model.add(layers.Dense(self.nbHidden, activation='sigmoid') ) 
		self.model.add(layers.Dense(self.nbOutput,activation='linear') )
		self.model.compile(loss='mse', optimizer='adam', metrics=['mae'])


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


	def test_tuto(self):
		# now execute the q learning
		y = 0.95 #
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




net = UtilityNetwork()
net.loadw('test_tuto_w.h5')
net.test_tuto()
net.savew('test_tuto_w.h5')


