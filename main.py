"""Run to play the simulation of an agent in a maze full of obstacles, enemies and food"""

import time
from simulator import *
import cProfile


sim = Simulator()

print("\nTo use the simulator in manual mode enter 'M' or 'm'.")
print("To run the simulator with the good network enter '*'.")
print("To run the experiment described in [Lin1992] as QCON enter 'Q' or 'q'.")
print("To run the experiment described in [Lin1992] as QCON-R enter 'R' or 'r'.")
c_input = input()
while c_input not in ['m', 'M', 'q', 'Q', 'R', 'r', '*']:
	print("Can't understand "+str(c_input)+". Please try again.")
	print("\nTo use the simulator in manual mode enter 'M' or 'm'.")
	print("To run the simulator with the good network enter '*'.")
	print("To run the experiment described in [Lin1992] as QCON enter 'Q' or 'q'.")
	print("To run the experiment described in [Lin1992] as QCON-R enter 'R' or 'r'.")
	c_input = input()

if c_input == "M" or c_input == "m":
	sim.manual_run()

elif c_input == '*':
	sim.saved_experiment_run()

elif c_input == 'Q' or c_input == 'q':
	# change value to adjust the number of independent experiments to run
	nb_exp = 1
	i = 0
	while i < nb_exp:
		sim.experiment_run()
		i += 1

elif c_input == 'R' or c_input == 'r':
	nb_exp = 1
	i = 0
	while i < nb_exp:
		sim.experiment_run(replay=True)
		i += 1
