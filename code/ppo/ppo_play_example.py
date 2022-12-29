import numpy as np
from game_state import GameState
from ppo.ppo_agent import Agent


def play_example():
    env = GameState(num_players=4)
    obs = env.observation_tensor(0)
    N = 20
    batch_size = 5
    alpha = 1e-6
    agents = [
        Agent(
            n_actions=env.num_actions,
            input_dims=obs.shape,
            alpha=alpha,
            batch_size=batch_size,
            chkpt_dir=f"models/player_{i}/",
        )
        for i in range(env.num_players)
    ]
    n_games = 300

    best_score = 0
    score_history = []

    learn_iters = 0
    avg_score = 0
    n_steps = [0 for _ in range(env.num_players)]

    for i in range(n_games):
        env = GameState(num_players=4)
        observation = env.observation_tensor(0)
        done = False
        score = 0
        while not done:
            for j in range(env.num_players):
                legal_actions = env.legal_actions(env.players[j])
                if len(legal_actions) == 0:
                    print("Player",j,"i dead with score", env.players[j].xp)
                    continue # will continue, the agent will not choose an action
                action, prob, val = agents[j].choose_action(observation, legal_actions)
                observation_, reward, done = env.step(j, action)
                n_steps[j] += 1
                score += reward
                agents[j].store_transition(observation, action, prob, val, reward, done)
                if n_steps[j] % N == 0:
                    agents[j].learn()
                    learn_iters += 1
                observation = observation_
            done = all([p.xp <= 0 for p in env.players])
            score_history.append(score)
            avg_score = np.mean(score_history[-100:])
        if avg_score > best_score:
            best_score = avg_score
            agents[j].save_models()

        print(
            "episode: ",
            i,
            "score: %.1f" % score,
            "avg score %.1f" % avg_score,
            "time_steps",
            n_steps,
            "learning_steps",
            learn_iters,
        )
