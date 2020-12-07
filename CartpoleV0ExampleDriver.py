from tf_agents.environments import suite_gym

env_name = 'CartPole-v0'
env = suite_gym.load(env_name)

print('Action Spec:')
print(env.action_spec())