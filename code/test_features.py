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
    p0_obs =game.observation_tensor(0)[:-num_players]
    p1_obs = game.observation_tensor(1)[:-num_players]
    print(np.sum(p0_obs != p1_obs ))
    p0_obs=p0_obs.reshape((5,7,5))
    p1_obs=p1_obs.reshape((5,7,5))
    print(p0_obs.shape)
    print(p1_obs.shape)
    print(p0_obs[2,3,:])
    print(p1_obs[2,3,:])
    
