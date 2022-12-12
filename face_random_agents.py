from simple_dqn_keras import Agent
from game_state import GameState
import sys

num_players = 4


def get_agents_and_game(file_str: str):
    model_player_file = file_str
    env = GameState(num_players, no_moves=10000)
    obs = env.observation_tensor(0)
    agent_trained = Agent(
        alpha=0,
        gamma=1,
        epsilon=0,
        batch_size=64,
        input_dims=(obs.shape),
        epsilon_dec=0,
        epsilon_end=0,
        mem_size=100000,
        n_actions=env.num_actions,
        fname=model_player_file,
    )
    agent_trained.load_model()
    all_agents = [agent_trained]
    for _ in range(1, env.num_players):
        # using a random agent for comparison
        agent = Agent(
            alpha=0,
            gamma=1,
            epsilon=1,
            batch_size=64,
            input_dims=(obs.shape),
            epsilon_dec=0,
            epsilon_end=1,
            mem_size=100000,
            n_actions=env.num_actions,
            fname="",
        )
        all_agents.append(agent)
    return all_agents, env


def play_game(env: GameState, agents: list) -> list:
    done = False
    scores = [0 for _ in range(env.num_players)]
    obs = []
    while not done:
        for j in range(env.num_players):  # agent in agents:
            agent = agents[j]

            legal_actions = env.legal_actions(env.players[j])
            print("legal actions are", len(legal_actions), ":", legal_actions, end="; ")
            if len(legal_actions) == 0:
                if env.players[j].hp <= 0:
                    print("Player ", j, " is dead with score ", env.players[j].xp)
                continue
            # print("Legal actions in main:", legal_actions)
            obs = env.observation_tensor(j)
            action = agent.choose_action(obs, legal_actions)

            observation_, reward, done = env.step(j, action)
            scores[j] += reward
            obs = observation_
    return scores


if __name__ == "__main__":
    agents, env = get_agents_and_game(sys.argv[1])
    scores = play_game(env, agents)
    print("Scores: ", scores)
