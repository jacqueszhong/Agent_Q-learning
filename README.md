# Agent_Q-learning
Self-learning agent based on Q-learning

This project is based on the article "Self-Improving Reactive Agent Based on Reinforcement Learning" by Long-Ji Lin (1992).
Coded in Python.

We developed this project as part of our master's degree in AI in 2018.

## Packages required
keras
tensorFlow
numpy
gym

## Getting Started

You are playing an agent in a closed environment with obstacles 'O', 4 enemies 'E' and food '$'.
Your goal is to live as long as you can, avoiding enemies and eating food in order to get energy.

Your initial energy level is 40 and you earn 15 every time you eat.

Once the game is running no more food can appear on the map.
If one ennemy is on the same place than you or if you run out of energy you die.

To start the simulator run the main.py file
```
python main.py
```

You have to choose between 4 modes:
- Manual mode -> you control the agent
- Smart mode -> using Q-learning, the agent use its policy to move itself in the environment and learn from its experiences
- Learning mode 
- Learning mode + action replay

## Manual Mode

To move the agent use:
'z' to move north
's' to move south
'q' to move west
'd' to move east

To exit use:
'x' 

## Authors

* **Maëva A.** - [BarbeBleue](https://github.com/barbebleue)

* **Jacques Z.** - [Jaquapi](https://github.com/jacqueszhong)