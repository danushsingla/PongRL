import gym
from gym.envs.registration import register
import PongEnv


if __name__ == '__main__':
    register(
        id='PongGame',
        entry_point='PongEnv',
        max_episode_steps=300,
    )

    ep_length = 2048 * 8
    env = SubprocVecEnv([make_env(i, env_config) for i in range(num_cpu)])

    model = PPO('CnnPolicy', env, verbose=1, n_steps=ep_length, batch_size=512, n_epochs=1, gamma=0.999)

    for i in range(learn_steps):
        model.learn(total_timesteps=(ep_length) * num_cpu * 1000, callback=checkpoint_callback)