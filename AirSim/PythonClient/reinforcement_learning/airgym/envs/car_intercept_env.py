import airsim
import numpy as np
import time
from gym import spaces
from airgym.envs.airsim_env import AirSimEnv


class AirSimCarInterceptEnv(AirSimEnv):
    def __init__(self, ip_address):
        super().__init__((84, 84, 1))  # image shape for default gym env
        self.start_ts = 0

        ## observation 
        self.car_state = {}   

        ## action space
        self.action_space = spaces.Discrete(6)

        self.cars = airsim.CarClient(ip=ip_address)
        self.car_controls = {
            "red_car":airsim.CarControls(),
            "blue_car":airsim.CarControls()
        }

    # reset to origin state
    def _setup_car(self):
        self.cars.reset()
        self.cars.enableApiControl(True,"Catcher")
        self.cars.enableApiControl(True,"Escaper")
        self.cars.armDisarm(True,"Catcher")
        self.cars.armDisarm(True,"Escaper")
        time.sleep(0.01)

    def __del__(self):
        self.cars.reset()

    # do action
    def _do_action(self, action):
        for car_style in action.keys():
            self.car_controls[car_style].brake = 0
            self.car_controls[car_style].throttle = 1
            if action[car_style] == 0:
                self.car_controls[car_style].throttle = 0
                self.car_controls[car_style].brake = 1
            elif action[car_style] == 1:
                self.car_controls[car_style].steering = 0
            elif action[car_style] == 2:
                self.car_controls[car_style].steering = 0.5
            elif action[car_style] == 3:
                self.car_controls[car_style].steering = -0.5
            elif action[car_style] == 4:
                self.car_controls[car_style].steering = 0.25
            else:
                self.car_controls[car_style].steering = -0.25

        self.cars.setCarControls(self.car_controls["red_car"], "Escaper") 
        self.cars.setCarControls(self.car_controls["blue_car"], "Catcher") 

    # get observation
    def _get_obs(self):
        self.car_state["red_car"] = self.cars.simGetObjectPose("Escaper")
        self.car_state["blue_car"] = self.cars.simGetObjectPose("Catcher")

    """
    simGetObjectPose(object_name)[source]
    Parameters
    object_name (str) – Object to get the Pose of

    Returns
    Return type
    Pose

    class airsim.types.Pose(position_val=None, orientation_val=None)[source]
    containsNan()[source]
    static nanPose()[source]
    orientation= <Quaternionr> {   'w_val': 1.0,     'x_val': 0.0,     'y_val': 0.0,     'z_val': 0.0}
    position= <Vector3r> {   'x_val': 0.0,     'y_val': 0.0,     'z_val': 0.0}
    """
    # compute reward
    def _compute_reward(self):
        reward = 0
        return reward
    
    # compute ending condition
    def _if_end(self):
        done = False
        red_car_position = self.car_state["red_car"].position
        blue_car_position = self.car_state["blue_car"].position
        goal_position = self.cars.simGetObjectPose("Goal").position
        r_b_distance = np.linalg.norm([red_car_position.x_val-blue_car_position.x_val, \
                red_car_position.y_val-blue_car_position.y_val,red_car_position.z_val-blue_car_position.z_val])
        r_g_distance = np.linalg.norm([red_car_position.x_val-goal_position.x_val, \
                red_car_position.y_val-goal_position.y_val,red_car_position.z_val-goal_position.z_val])
        if r_b_distance < 5:
            # Catcher catch escaper
            done = True
        elif red_car_position.z_val > 5 or blue_car_position.z_val > 5:
            # one of the car fall out of playground
            done = True
        elif r_g_distance < 5:
            done = True
        return done

    def step(self, action):
        self._do_action(action)
        obs = self._get_obs()
        reward = self._compute_reward()
        done = self._if_end()
        info = None
        return obs, reward, done, info

    def reset(self):
        self._setup_car()
        self._do_action({"red_car":1,"blue_car":1})
        return self._get_obs()
