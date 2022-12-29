from simple_dqn_keras import Agent
from game_state import GameState
from train_keras import learn_from_games, record_agents
import numpy as np
import sys
import os
import datetime
num_players = 4

# i also wanted to log the agents' properties

if __name__ == "__main__":
    execution_time = datetime.datetime.now().strftime("%Y_%m_%d_%X")
    model_folder = f"models/{sys.argv[1]}_{execution_time}"
    print("model folder:", model_folder)
    if not os.path.isdir(model_folder):
        os.makedirs(model_folder, exist_ok = True)

    n_games = 100000
    learn_from_games(
        n_games, num_players, random_play=False, model_folder=model_folder, record=True
    )
