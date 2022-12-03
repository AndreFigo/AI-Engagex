from simple_dqn_keras import Agent
from game_state import GameState
import numpy as np

num_players = 10

if __name__ == "__main__":
    env = GameState(num_players)
    obs = env.observation_tensor(0)
    print("Observation tensor shape: ", obs.shape)
    print("Observation values: ", obs.shape[0])
    n_games = 1000

    agents = [
        Agent(
            gamma=0.99,
            epsilon=1,
            alpha=0.0001,
            input_dims=(obs.shape),
            n_actions=env.num_actions,
            mem_size=1000000,
            batch_size=64,
            epsilon_end=0.01,
        )
        for _ in range(env.num_players)
    ]
    scores = []
    eps_history = []

    for i in range(n_games):
        done = False
        score = 0
        env = GameState(num_players)
        observation = env.observation_tensor(0)
        obs = obs_after = []
        while not done:
            for j in range(env.num_players):  # agent in agents:
                agent = agents[j]

                legal_actions = env.legal_actions(env.players[j])
                if len(legal_actions) == 0:
                    continue
                # print("Legal actions in main:", legal_actions)
                obs = env.observation_tensor(j)
                action = agent.choose_action(obs, legal_actions)

                observation_, reward, done = env.step(j, action)
                score += reward
                # obs_after = env.observation_tensor(i)
                agent.remember(obs, action, reward, observation_, int(done))
                obs = observation_
                agent.learn()

        scores.append(score)
        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])
        print(
            "episode ",
            i,
            "score %.2f" % score,
            " average score %.2f" % avg_score,
            "epsilon %.2f" % agent.epsilon,
        )
