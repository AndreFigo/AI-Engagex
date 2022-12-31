from simple_dqn_keras import Agent
from game_state import GameState, EngagexPlayer
from train_keras import learn_from_games, record_agents
import numpy as np
import sys
import os

num_players = 4

if __name__ == "__main__":
    game = GameState(num_players = 4, no_moves = 500)
    game.players[1] = EngagexPlayer(1,0,0,game)
    game.players[1].xp = 5
    game.players[1].hp = 90
    p0_obs =game.observation_tensor(0)
    p1_obs = game.observation_tensor(1)
    print(np.sum(p0_obs != p1_obs ))

    print(p0_obs.shape)
    print(p1_obs.shape)
    print(p0_obs[35:39])
    print(p1_obs[35:39])
    
