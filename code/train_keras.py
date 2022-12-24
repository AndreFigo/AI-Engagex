from simple_dqn_keras import Agent
from game_state import GameState
import numpy as np
import sys
import os


def random_agent(obs: np.ndarray, num_actions: int) -> Agent:
    # returns an agent that performs random actions all the time
    agent_random = Agent(
        alpha=0.001,
        gamma=1,
        epsilon=1,
        batch_size=64,
        input_dims=(obs.shape),
        epsilon_dec=1,
        epsilon_end=1,
        mem_size=100000,
        n_actions=num_actions,
        fname="",
    )
    return agent_random


def rational_agent(obs: np.ndarray, num_actions: int) -> Agent:
    # returns an agent with the ability to learn
    return Agent(
        gamma=1,  # gamma = 1 means no discounting
        epsilon_dec=0.996,  # after 2300 moves in each agent, epsilon is 0.1
        epsilon=1,
        alpha=0.001,
        input_dims=(obs.shape),
        n_actions=num_actions,
        mem_size=64,
        batch_size=64,
        epsilon_end=0.01,
    )


def get_agents(
    obs: np.ndarray, num_actions: int, num_agents: int, random=False
) -> list:
    # retuns a list of agents for training
    if random:
        # one ratoinal agent and the rest random
        all_agents = [rational_agent(obs, num_actions)] + [
            random_agent(obs, num_actions) for _ in range(num_agents - 1)
        ]
        return all_agents
    else:
        # all rational agents
        all_agents = [rational_agent(obs, num_actions) for _ in range(num_agents)]
        return all_agents


def learn_from_games(
    n_games,
    num_players,
    random_play=False,
    model_folder="models/model_default",
    record=True,
):
    # trains agents for learning games and records metrics on the results
    env = GameState(num_players)
    agents = get_agents(
        env.observation_tensor(0), env.num_actions, num_players, random_play
    )
    file_id = 2
    if record:
        file_output = "%s/output.csv" % model_folder
        file_id = open(file_output, "a")
        record_agents(agents, model_folder)
    env = GameState(num_players)
    for i in range(n_games):
        done = False
        scores = [0 for _ in range(env.num_players)]
        env = GameState(num_players)
        while not done:
            for j in range(env.num_players):  # agent in agents:
                agent: Agent = agents[j]

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
                agent.learn()
        if record:
            player_xps: list = [env.players[i].xp for i in range(env.num_players)]
            print("player_xps:", player_xps)
            str_init = ",".join([str(xp) for xp in player_xps])
            str_init += "," + ",".join([str(i) for i in env.total_actions])
            file_id.write("%s\n" % str_init)
            file_id.flush()

        # eps_history.append(agent.epsilon)
        print(
            "episode ",
            i,
            "scores",
            scores,
            "epsilon %.2f" % agents[0].epsilon,
        )

        if (i + 1) % 10 == 0:
            j = 0
            for agent in agents:
                agent.model_file = "%s/model_agent_%d_epoch_%d.h5" % (
                    model_folder,
                    j,
                    i + 1,
                )
                agent.save_model()
                j += 1
    if record:
        file_id.close()


def record_agents(agents, model_folder):
    # records the agents' properties
    file_path = "%s/agent_record.csv" % model_folder
    with open(file_path, "a") as f:
        for agent in agents:
            f.write("%s\n" % agent)