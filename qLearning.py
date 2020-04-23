import numpy as np
import keras.backend.tensorflow_backend as backend
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.optimizers import Adam
import tensorflow as tf
from tensorflow import keras
from keras.callbacks import TensorBoard
from collections import deque
import time
import random
from tqdm import tqdm
import os
import matplotlib.pyplot as plt

from Connect4Env import Connect4Env
from ModifiedTB import ModifiedTensorBoard

DISCOUNT = 0.8
REPLAY_MEMORY_SIZE = 50000  # How many last steps to keep for model training
MIN_REPLAY_MEMORY_SIZE = 1000  # Minimum number of steps in a memory to start training
MINIBATCH_SIZE = 64  # How many steps (samples) to use for training
UPDATE_TARGET_EVERY = 5  # Terminal states (end of episodes)
MODEL_NAME = '4x4'
MEMORY_FRACTION = 0.20
MIN_REWARD = 100

# Environment settings
EPISODES = 4000000

# Exploration settings
epsilon = 5  # not a constant, going to be decayed
EPSILON_DECAY = 0.99
MIN_EPSILON = 0.15

#  Stats settings
AGGREGATE_STATS_EVERY = 50  # episodes
SHOW_PREVIEW = False

env = Connect4Env()

# For stats
ep_rewards = [-200]

# For more repetitive results
random.seed(1)
np.random.seed(1)
tf.compat.v2.random.set_seed(1)
# # tf.random.set_seet(1)
# tf.set_random_seed(1)

# Memory fraction, used mostly when trai8ning multiple agents
# gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=MEMORY_FRACTION)
# backend.set_session(tf.Session(config=tf.ConfigProto(gpu_options=gpu_options)))

# Create models folder
if not os.path.isdir('models'):
    os.makedirs('models')


# Agent class
class DQNAgent:
    def __init__(self):

        # Main model
        self.model = self.create_model()

        # Target network
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        # An array with last n steps for training
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        # Custom tensorboard object
        self.tensorboard = TensorBoard(log_dir="logs/{}-{}".format(MODEL_NAME, int(time.time())))
        self.tensorboard.step = 1
        self.tensorboard.writer = tf.summary.create_file_writer(self.tensorboard.log_dir)


        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0

    def create_model(self):
        model = Sequential()

        model.add(Dense(MINIBATCH_SIZE, input_dim=env.observation_space.n))  # OBSERVATION_SPACE_VALUES = (10, 10, 3) a 10x10 RGB image.
        model.add(Activation('relu'))

        model.add(Dense(128))
        model.add(Activation('relu'))

        model.add(Dense(128))
        model.add(Activation('relu'))

        model.add(Dense(128))
        model.add(Activation('relu'))


        # model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors

        model.add(Dense(env.action_space.n, activation='linear'))  # ACTION_SPACE_SIZE = how many choices (9)
        model.compile(loss="mse", optimizer=Adam(lr=0.001), metrics=['accuracy'])
        return model

    # Adds step's data to a memory replay array
    # (observation space, action, reward, new observation space, done)
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    # Trains main network every step during episode
    #

    def train(self, terminal_state, step):

        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        # Get a minibatch of random samples from memory replay table
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # Get current states from minibatch, then query NN model for Q values
        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_list = self.model.predict(current_states)

        # Get future states from minibatch, then query NN model for Q values
        # When using target network, query it, otherwise main network should be queried
        new_current_states = np.array([transition[4] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        # Now we need to enumerate our batches
        for index, (current_state, current_player, action, reward, new_current_state, done) in enumerate(minibatch):

            # If not a terminal state, get new q from future states, otherwise set it to 0
            # almost like with Q Learning, but we use just part of equation here
            if not done:
                if current_player == 1:
                    future_q = np.max(future_qs_list[index])
                else:
                    future_q = np.min(future_qs_list[index])
                new_q = reward + DISCOUNT * future_q
            else:
                new_q = reward

            # Update Q value for given state
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            # And append to our training data
            X.append(current_state)
            y.append(current_qs)

        # Fit on all samples as one batch, log only on terminal state
        history = self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False if terminal_state else None)

        for i in range(int(abs(new_q) / 40)):
            history = self.model.fit(np.array(X), np.array(y), batch_size=MINIBATCH_SIZE, verbose=0, shuffle=False if terminal_state else None)

        # print(history.history.keys())
        err = history.history['accuracy'][0]

        # if err > 0.98:
        #     agent.model.save("models/Connect4_{}_err_{}".format(MODEL_NAME, str(err)), overwrite = True)

        # Update target network counter every episode
        if terminal_state:
            self.target_update_counter += 1

        # If counter reaches set value, update target network with weights of main network
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def train2(self, terminal_state, step):
        if not terminal_state or len(self.replay_memory) == 0:
            return

        currStates = []
        actions = []
        rewards = []

        recurses = []
        recurseDiscount = 0.1

        firstTransition = self.replay_memory.pop()
        currStates.append(firstTransition[0])
        actions.append(firstTransition[2])

        currReward = firstTransition[3]
        rewards.append(currReward)
        currReward = currReward * DISCOUNT

        recurse = 500
        recurses.append(recurse)
        recurse = np.ceil(recurse * recurseDiscount)

        while len(self.replay_memory) > 0:
            transition = self.replay_memory.pop()
            currStates.append(transition[0])
            actions.append(transition[2])

            rewards.append(currReward)
            recurses.append(recurse)

            currReward = currReward * DISCOUNT
            recurse = np.ceil(recurse * recurseDiscount)

        current_qs_list = self.model.predict(np.array(currStates))

        X = []
        y = []

        for i in range(len(currStates)):
            current_qs = current_qs_list[i]
            current_qs[actions[i]] = rewards[i]

            recurse = int(recurses[i])
            X.extend([currStates[i]] * recurse)
            y.extend([current_qs] * recurse)

        history = self.model.fit(np.array(X), np.array(y),
                                 verbose=0, shuffle=True)

        # print(history.history.keys())
        err = history.history['accuracy'][0]
        # plt.plot(err, '-bo')
        # plt.show()

        if err == 1:
            agent.model.save("models/Connect4_{}_err_{}"
                             .format(MODEL_NAME, str(err)), overwrite=True)

        # Update target network counter every episode
        self.target_update_counter += 1

        # If counter reaches set value, update target network with
        # weights of main network
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    # Queries main network for Q values given current observation space
    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape))[0]


agent = DQNAgent()
agent.model = keras.models.load_model("models/Connect4_4x4_17000")

# Iterate over episodes
for episode in tqdm(range(17001, EPISODES + 1), ascii=True, unit='episodes'):
    if episode % 1000 == 0:
        agent.model.save("models/Connect4_{}_{}".
                         format(MODEL_NAME, str(episode)), overwrite=True)

    # Update tensorboard step every episode
    agent.tensorboard.step = episode

    # Restarting episode - reset episode reward and step number
    episode_reward = 0
    step = 1

    # Reset environment and get initial state
    current_state = env.reset()
    current_player = 1

    # Reset flag and start iterating until episode ends
    done = False
    while not done:
        # This part stays mostly the same,
        # the change is to query a model for Q values
        if np.random.random() > epsilon:
            # Get action from Q table
            if current_player == 1:
                action = np.argmax(agent.get_qs(current_state))
            else:
                action = np.argmin(agent.get_qs(current_state))
        else:
            # Get random action
            action = np.random.randint(0, env.action_space.n)

        current_player = current_player * -1

        [new_state, reward, done, info] = env.step(action)

        # Transform new continous state to new discrete state and count reward
        episode_reward += reward

        # Every step we update replay memory and train main network
        agent.update_replay_memory((current_state, current_player, action,
                                    reward, new_state, done))
        agent.train(done, step)

        current_state = new_state
        step += 1

    # Append episode reward to a list and log stats
    # (every given number of episodes)
    ep_rewards.append(episode_reward)
    if not episode % AGGREGATE_STATS_EVERY or episode == 1:
        average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:]) / \
            len(ep_rewards[-AGGREGATE_STATS_EVERY:])
        min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
        max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
        # agent.tensorboard.update_stats(reward_avg=average_reward,
        # reward_min=min_reward, reward_max=max_reward, epsilon=epsilon)

        # Save model, but only when min reward is greater or equal a set value
        # if min_reward >= MIN_REWARD:
        #     agent.model.save("models/Connect4_{}_reward{}"
        #     .format(MODEL_NAME, str(min_reward)))

    # Decay epsilon
    if epsilon > MIN_EPSILON:
        epsilon *= EPSILON_DECAY
        epsilon = max(MIN_EPSILON, epsilon)

agent.model.save("models/Connect4{}".format(MODEL_NAME))
