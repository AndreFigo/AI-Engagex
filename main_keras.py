from simple_dqn_keras import Agent
from game_state import GameState
import numpy as np
import sys
import os


num_players = 4

if __name__ == "__main__":
    model_folder = sys.argv[1]
    if not os.path.isdir(model_folder):
        os.mkdir(model_folder)
    file_output = "%s/output.csv" % sys.argv[1]
    file_id = open(file_output, "a")
    env = GameState(num_players, no_moves=10000)
    obs = env.observation_tensor(0)
    print("Observation tensor shape: ", obs.shape)
    print("Observation values: ", obs.shape[0])
    n_games = 500

    agents = [
        Agent(
            gamma=0.99,
            epsilon_dec=0.996,  # after 2300 moves in each agent, epsilon is 0.1
            epsilon=1,
            alpha=0.0001,
            input_dims=(obs.shape),
            n_actions=env.num_actions,
            mem_size=100000,
            batch_size=64,
            epsilon_end=0.01,
        )
        for _ in range(env.num_players)
    ]
    scores = []
    eps_history = []

    for i in range(n_games):
        done = False
        scores = [0 for _ in range(env.num_players)]
        env = GameState(num_players)
        observation = env.observation_tensor(0)
        obs = obs_after = []
        while not done:
            for j in range(env.num_players):  # agent in agents:
                agent = agents[j]

                legal_actions = env.legal_actions(env.players[j])
                if len(legal_actions) == 0:
                    if env.players[j].hp <= 0:
                        print("Player ", j, " is dead with score ", env.players[j].xp)
                    continue
                # print("Legal actions in main:", legal_actions)
                obs = env.observation_tensor(j)
                action = agent.choose_action(obs, legal_actions)

                observation_, reward, done = env.step(j, action)
                scores[j] += reward
                # obs_after = env.observation_tensor(i)
                agent.remember(obs, action, reward, observation_, int(done))
                obs = observation_
                agent.learn()
        str_init = ",".join([str(i) for i in scores])
        str_init += "," + ",".join([str(i) for i in env.total_actions])
        file_id.write("%s\n" % str_init)
        file_id.flush()

        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])
        print(
            "episode ",
            i,
            "scores",
            scores,
            "epsilon %.2f" % agent.epsilon,
        )

        if i % 10 == 0 and i > 0:
            j = 0
            for agent in agents:
                agent.model_file = "%s/model_agent_%d_epoch_%d.h5" % (
                    model_folder,
                    j,
                    i,
                )
                agent.save_model()
                j += 1
    file_id.close()
