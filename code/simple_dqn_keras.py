from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import numpy as np


class ReplayBuffer(object):
    def __init__(self, max_size, input_shape, n_actions, discrete=False):
        self.mem_size = max_size
        self.mem_cntr = 0
        self.state_memory = np.zeros((self.mem_size, *input_shape))
        self.new_state_memory = np.zeros((self.mem_size, *input_shape))
        self.discrete = discrete
        dtype = np.int8 if self.discrete else np.float32
        self.action_memory = np.zeros((self.mem_size, n_actions), dtype=dtype)
        self.reward_memory = np.zeros(self.mem_size)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.float32)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - int(done)
        if self.discrete:
            actions = np.zeros(self.action_memory.shape[1])
            actions[action] = 1.0
            self.action_memory[index] = actions
        else:
            self.action_memory[index] = action
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size)
        states = self.state_memory[batch]
        states_ = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]
        return states, actions, rewards, states_, terminal


def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims):
    init = tf.keras.initializers.HeUniform()

    model = Sequential(
        [
            Dense(fc1_dims, input_shape=(*input_dims,), activation = 'relu', kernel_initializer = init),
            Dense(fc2_dims,activation = 'relu', kernel_initializer = init),
            # Dense(fc3_dims,activation = 'relu', kernel_initializer = init),
            # Dense(fc4_dims, activation = 'relu', kernel_initializer = init),
            Dense(n_actions, kernel_initializer = init)
        ]
    )
    model.compile(optimizer=Adam(lr=lr), loss=tf.keras.losses.Huber())
    return model


class Agent(object):
    def __init__(
        self,
        alpha,
        gamma,
        n_actions,
        epsilon,
        batch_size,
        input_dims,
        epsilon_dec=0.996,
        epsilon_end=0.01,
        mem_size=1000000,
        fname="dqn_model.h5",
    ):
        self.action_space = np.array([i for i in range(n_actions)])
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_end
        self.epsilon_dec = epsilon_dec
        self.batch_size = batch_size
        self.model_file = fname
        self.memory = ReplayBuffer(mem_size, input_dims, n_actions, discrete=True)
        self.q_eval = build_dqn(alpha, n_actions, input_dims, 256,256)

    def remember(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    def choose_action(self, state, legal_actions, print_q_vector = False):
        state = state[np.newaxis, :]
        rand = np.random.random()
        # print("legal_actions", legal_actions)

        if rand < self.epsilon:
            action = np.random.choice(self.action_space[legal_actions])

        else:
            # print("not random")
            actions = self.q_eval.predict(state, verbose=0)
            actions = actions[0, legal_actions]
            if print_q_vector:
                print("yielded actions: ", actions)
            action = legal_actions[np.argmax(actions)]
        return action

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return
        state, action, reward, new_state, done = self.memory.sample_buffer(
            self.batch_size
        )
        action_values = np.array(self.action_space, dtype=np.int8)
        action_indices = np.dot(action, action_values)
        q_eval = self.q_eval.predict(state, verbose=0)
        q_next = self.q_eval.predict(new_state, verbose=0)

        q_target = q_eval.copy()
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        q_target[batch_index, action_indices] = (
            reward + self.gamma * np.max(q_next, axis=1) * done
        )

        _ = self.q_eval.fit(state, q_target, verbose=0)

        self.epsilon = (
            self.epsilon * self.epsilon_dec
            if self.epsilon > self.epsilon_min
            else self.epsilon_min
        )

    def save_model(self):
        self.q_eval.save(self.model_file)

    def load_model(self):
        self.q_eval = load_model(self.model_file)

    def __str__(self):
        return f"Agent: gamma: {self.gamma}, epsilon: {self.epsilon}, epsilon_dec:{self.epsilon_dec}, epsilon_end:{self.epsilon_min}, batch_size: {self.batch_size}, mem_size: {self.memory.mem_size}"
