import gym
from gym.envs.registration import register
from gym_envs.envs.pong_env import PongEnv
from stable_baselines3 import PPO


if __name__ == '__main__':
    register(
        id='PongGame',
        entry_point='PongEnv',
        max_episode_steps=300,
    )

    ep_length = 2048 * 8
    env = gym.make('PongEnv')

