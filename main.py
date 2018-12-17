"""Run to play the simulation of an agent in a maze full of obstacles, ennemies and food"""
"""Virtual environnement :
virtualenv --system-site-packages -p python3 ./venv
source ./venv/bin/activate  # sh, bash, ksh, or zsh   
"""

import time
from simulator import *


sim = Simulator()

#sim.test_run(10)
i=0
while(i<20):
	sim.experiment_run()
	i+=1
#sim.generate_maps(301,50)

