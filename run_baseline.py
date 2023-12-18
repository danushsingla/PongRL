import gym
import gym_envs
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed


def make_env(env_id, rank, seed=0):
    def _init():
        env = gym.make(env_id)
        env.reset(seed=seed + rank)
        return env

    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    num_cpu = 1  # Number of processes to use

    # env = gym.make('gym_envs/PongGame', render_mode='human')
    env = SubprocVecEnv([make_env("gym_envs/PongGame", i) for i in range(num_cpu)])
    # model = PPO('MultiInputPolicy', env, verbose=1)
    model = PPO.load("PongGame_model", env=env, verbose=1)

    print('Training model...')
    model.learn(total_timesteps=50000)
    print('Training complete!')

    model.save("PongGame_model")
    print('Model saved!')
