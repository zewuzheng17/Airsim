import airgym
import gym
import numpy as np
import copy

"""
gym environment for car intercepting based on airsim

usage:
env = gym.make("airsim-car-intercept-v0", ip_address="", self_control_escaper:bool, self_control_catcher:bool) 

action = a dict
with keys {"Escaper","Catcher"}, each has following attributes
brake = (0, 1), throttle = (0, 1), steering = (-0.5 - 0.5)

observation = a dict 
with keys Escaper and Catcher, each has following attributes.
position: x_val, y_val, z_val
linear_acceleration: x_val, y_val, z_val
linear_velocity: x_val, y_val, z_val
angular_accerleration: x_val, y_val, z_val
angular_velocity: x_val, y_val, z_val
orientation: w_val, x_val, y_val, z_val

and with key:
goal_position: x_val, y_val, z_val
  
"""

def main():
    env = gym.make("airsim-car-intercept-v0", ip_address="127.0.0.1", self_control_escaper = True, self_control_catcher = False)    
    obs, action, done = env.reset()
    pre_obs = obs
    skip_t = 0 # simmulation step to be skipped
    while not done:
        obs, rewards, done, info = env.step(action)
        if skip_t % 30 == 0 and (obs and pre_obs is not None):      
            action["Catcher"].steering = Propotional_navi(obs, pre_obs, 70)
            skip_t = 0
            pre_obs = copy.deepcopy(obs)
        skip_t += 1       
    print(info)

def Propotional_navi(cur_obs, pre_obs, K) -> float: 
    cur_relative_vec = cur_obs["Escaper"].position - cur_obs["Catcher"].position 
    pre_relative_vec = pre_obs["Escaper"].position - pre_obs["Catcher"].position
    theta = np.arccos(np.clip(cur_relative_vec.dot(pre_relative_vec) / (cur_relative_vec.get_length() * pre_relative_vec.get_length()), -1, 1))  ## calculate angle
    rho = -int(np.sign(np.cross(cur_relative_vec.to_numpy_array()[:2], pre_relative_vec.to_numpy_array()[:2]))) ## whether target located on left or right
    return 0 if theta < 0.01 else rho * np.clip(theta * K, 0, np.pi) / np.pi * 0.5

if __name__ == "__main__":
    main()
    

