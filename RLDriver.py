import pygame
from random import expovariate
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt

from tf_agents.environments import tf_py_environment
from tf_agents.networks import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.utils import common
from tf_agents.trajectories import trajectory
from tf_agents.replay_buffers import tf_uniform_replay_buffer, episodic_replay_buffer
from tf_agents.drivers import dynamic_step_driver, dynamic_episode_driver
from tf_agents.metrics import tf_metrics

from environment.AstracraftEnvironment import AstracraftEnvironment

tf.compat.v1.enable_v2_behavior()
print("Tensorflow version:")
print(tf.version.VERSION)

# ''' HYPERPARAMETERS'''
# q_net_layers = (100,) # fc_layer_params
q_net_layers = (75, 40)
num_iterations = 200 # Number of episodes batches to train on
collection_steps_per_iteration = 100 # Training steps per iteration, random sampling
replay_buffer_max_length = 200 # Max of 100 frames in an episode, 2 episodes
deterministic_sampling = False # False = random, True = in order
# ''' END HYPERPARAMETERS'''

# Set up display for rendering our Astracraft game
# We'll use pygame for this
pygame.init()
env_width = 800
env_height = 600
pygame.display.set_mode((env_width, env_height))

train_py_env = AstracraftEnvironment(env_width, env_height)
eval_py_env = AstracraftEnvironment(env_width, env_height)

train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

print("Observation Spec:")
print(train_env.observation_spec())
print("Action Spec:")
print(train_env.action_spec())

# Begin setting up the agent
# print("Validating specs...")
# Begin setting up the DQN Agent (Q-network)
print("Network instantiation...")
q_net = q_network.QNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=q_net_layers
)
q_network.validate_specs(
    train_env.action_spec(),
    train_env.observation_spec()
)

# DqnAgent
print("Agent instantiation...")
# Requires Optimizer, Loss Function, Integer Step Counter
learning_rate = 1e-3  # @param {type:"number"}
optimizer = tf.compat.v1.train.AdamOptimizer()
#default learning_rate = 1e-3, or 0.001

train_step_counter = tf.Variable(0)

agent = dqn_agent.DqnAgent( # failing with non-scalar action spec
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter
)

print("Initializing DGN Agent...")
agent.initialize()
# How to validate successful initialization?

# Policies
eval_policy = agent.policy
collect_policy = agent.collect_policy

# Setup a replay buffer
print("Creating replay buffer... with batch size {0}".format(train_env.batch_size))
replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size, # batch size of 1 = 1 episode per run
    # dataset_window_shift=1, # Trying this for better training # Nope
    max_length=replay_buffer_max_length)

# replay_buffer = episodic_replay_buffer.EpisodicReplayBuffer(
#     data_spec=agent.collect_data_spec
# )

# Trying Episodic Replay buffer
# ep_replay_buffer = episodic_replay_buffer.EpisodicReplayBuffer(
#     data_spec=agent.collect_data_spec
# )

# Must use dataset to iterate replay buffer, gather_all is deprecated
print("As dataset...")
dataset = replay_buffer.as_dataset(
    sample_batch_size=train_env.batch_size,
    num_steps=2,
    num_parallel_calls=2,
    single_deterministic_pass=deterministic_sampling
)

# dataset = replay_buffer.as_dataset( # From Episodic
#     num_steps=None, # Return full length episodes
#     # single_deterministic_pass
# )

iterator = iter(dataset)
# iterator = dataset.make_initializable_iterator()

return_metric = tf_metrics.AverageReturnMetric()
replay_observers = [replay_buffer.add_batch, return_metric]

episode_driver = dynamic_episode_driver.DynamicEpisodeDriver(
    train_env,
    agent.collect_policy,
    replay_observers,
    num_episodes=2
)

loss_values = []
return_values = []

# Begin Training the Agent
print("Begin training DQN network...")
for i in range(num_iterations):
    print("Iteration {0}...".format(i))
    episode_driver.run()
    # buffer_frames = replay_buffer.num_frames()
    # print("Replay Buffer: {0} frames".format(replay_buffer.num_frames()))
    # iterator = iter(dataset)
    # for _ in range(buffer_frames):
    # frame_process_count = 0
    for _ in range(collection_steps_per_iteration):
    # for experience, _ in dataset: # Deterministic loop
        try:
            experience, _ = next(iterator)
            # print("Iterating...")
            # frame_process_count += 1
            loss_info = agent.train(experience)
            loss_values.append(loss_info.loss)
        except StopIteration:
            # print("Iterated {0} frames...".format(frame_process_count))
            break

        # step = agent.train_step_counter.numpy()
        # if step % 100 == 0:
        #     print("Step {0}: Loss = {1}".format(step, loss_info.loss))

    # print("Iteration {0} over...".format(i))
    avg_return = return_metric.result()
    print("Average Return: {0}".format(avg_return))
    return_values.append(avg_return)

plt.plot(return_values)
plt.ylabel('Average Return')
plt.xlabel('Number of Training Loops/Iterations')

plt.show(block=True)

plt.plot(loss_values)
plt.ylabel('Loss Value')
plt.xlabel('Number of Training Steps/Frames')

plt.show(block=True)