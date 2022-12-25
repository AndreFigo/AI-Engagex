from simple_dqn_keras import Agent
from game_state import GameState
from train_keras import learn_from_games, record_agents
import numpy as np
import sys
import os

num_players = 4

# i also wanted to log the agents' properties

if __name__ == "__main__":
    model_folder = sys.argv[1]
    if not os.path.isdir(model_folder):
        os.mkdir(model_folder)
    file_output = "%s/output.csv" % sys.argv[1]
    file_agent_record = "%s/agent_record.csv" % sys.argv[1]

    n_games = 100000
    learn_from_games(
        n_games, num_players, random_play=False, model_folder=model_folder, record=True
    )
