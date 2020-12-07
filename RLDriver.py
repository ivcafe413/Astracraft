import pygame
import tensorflow as tf

from tf_agents.environments import tf_py_environment
from tf_agents.networks import q_network
from tf_agents.agents.dqn import dqn_agent
from tf_agents.utils import common
from tf_agents.trajectories import trajectory
from tf_agents.replay_buffers import tf_uniform_replay_buffer

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
print("Validating specs...")
q_net_layers = (100,) # fc_layer_params
q_net = q_network.QNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=q_net_layers
)
print(q_network.validate_specs(
    train_env.action_spec(),
    train_env.observation_spec()
))

# DqnAgent
# Requires Optimizer, Loss Function, Integer Step Counter
learning_rate = 1e-3  # @param {type:"number"}
optimizer = tf.compat.v1.train.AdamOptimizer() #default learning_rate = 1e-3, or 0.001

train_step_counter = tf.Variable(0)

agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter # failing with non-scalar action spec
)

print("Initializing DGN Agent...")
agent.initialize()
# How to validate successful initialization?

# Policies
eval_policy = agent.policy
collect_policy = agent.collect_policy

# Metrics module contains a more standard implementation?
num_eval_episodes = 10
def compute_average_return(environment, policy, num_episodes=10):
    total_return = 0.0
    for _ in range(num_episodes):
        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return
    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]

def collect_step(environment, policy, buffer):
  time_step = environment.current_time_step()
  action_step = policy.action(time_step)
  next_time_step = environment.step(action_step.action)
  traj = trajectory.from_transition(time_step, action_step, next_time_step)

  # Add trajectory to the replay buffer
  buffer.add_batch(traj)

def collect_data(env, policy, buffer, steps):
  for _ in range(steps):
    collect_step(env, policy, buffer)

# Setup a replay buffer
print("Creating replay buffer...")
replay_buffer_max_length = 10000
replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_max_length)

print("Hydrate initial replay buffer...")
collect_data(train_env, agent.collect_policy, replay_buffer, 100)

# Dataset generates trajectories with shape [Bx2x...]
batch_size = 64
dataset = replay_buffer.as_dataset(
    num_parallel_calls=3, 
    sample_batch_size=batch_size, 
    num_steps=2).prefetch(3)

iterator = iter(dataset)

# Begin Training the Agent
print("Begin training DQN network...")
agent.train = common.function(agent.train)
agent.train_step_counter.assign(0)

# Evaulate agent policy once before training (?)
# avg_return = compute_average_return(eval_env, agent.policy, num_eval_episodes)
returns = []

# num_iterations = 20000 # 20k too many?
collect_steps_per_iteration = 1
log_interval = 200
eval_interval = 1000

# for _ in range(num_iterations) # See 5 lines above
for i in range(10000):
    # print (f"Step: {i}") # Py 3.6 String Interpolation
    collect_data(train_env, agent.collect_policy, replay_buffer, collect_steps_per_iteration)

    # Sample a batch of data from the buffer and update the agent's network.
    experience, unused_info = next(iterator)
    train_loss = agent.train(experience).loss

    step = agent.train_step_counter.numpy()

    if step % log_interval == 0:
        print('step = {0}: loss = {1}'.format(step, train_loss))

    if step % eval_interval == 0:
        avg_return = compute_average_return(eval_env, agent.policy, num_eval_episodes)
        print('step = {0}: Average Return = {1}'.format(step, avg_return))
        returns.append(avg_return)