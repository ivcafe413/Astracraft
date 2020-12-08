# import pygame
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt

from tf_agents.environments import tf_py_environment
from tf_agents.networks import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.utils import common
from tf_agents.trajectories import trajectory
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.drivers import dynamic_step_driver, dynamic_episode_driver
from tf_agents.metrics import tf_metrics

from environment.AstracraftEnvironment import AstracraftEnvironment

tf.compat.v1.enable_v2_behavior()
print("Tensorflow version:")
print(tf.version.VERSION)

# Set up display for rendering our Astracraft game
# We'll use pygame for this
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
env_width = 800
env_height = 600

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
q_net_layers = (100,) # fc_layer_params
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
print("Creating replay buffer...")
replay_buffer_max_length = 3600 # One full max episode step count (30 seconds * 60 FPS)
replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_max_length)

return_metric = tf_metrics.AverageReturnMetric()
replay_observers = [replay_buffer.add_batch, return_metric]

episode_driver = dynamic_episode_driver.DynamicEpisodeDriver(
    train_env,
    agent.collect_policy,
    replay_observers,
    num_episodes=1
)

num_episode_iterations = 100 # Number of episodes to train on
loss_values = []
return_values = []

# Begin Training the Agent
print("Begin training DQN network...")
for i in range(num_episode_iterations):
    episode_driver.run()
    experience = replay_buffer.gather_all()
    loss = agent.train(experience)
    replay_buffer.clear()
    loss_values.append(loss)
    return_values.append(return_metric.result())

# for _ in range(num_iterations) # See 5 lines above
# for i in range(10000):
#     # print (f"Step: {i}") # Py 3.6 String Interpolation
#     collect_data(train_env, agent.collect_policy, replay_buffer, collect_steps_per_iteration)

#     # Sample a batch of data from the buffer and update the agent's network.
#     experience, unused_info = next(iterator)
#     train_loss = agent.train(experience).loss

#     step = agent.train_step_counter.numpy()

#     if step % log_interval == 0:
#         print('step = {0}: loss = {1}'.format(step, train_loss))

plt.plot(loss_values)
plt.ylabel('Loss Value')
plt.xlable('Number of Episodes')