import airsim
from airgym.envs.airsim_env import AirSimEnv

import copy
import numpy as np
import time
from gym import spaces


"""
gym environment for car intercepting based on airsim

action = {"Escaper","Catcher"}
brake = (0, 1), throttle = (0, 1), steering = (-0.5 - 0.5)

observation = a dict 

with keys Escaper and Catcher, each has following attributes.
position: x_val, y_val, z_val
linear_acceleration: x_val, y_val, z_val
linear_velocity: x_val, y_val, z_val
angular_accerleration: x_val, y_val, z_val
angular_velocity: x_val, y_val, z_val
orientation: w_val, x_val, y_val, z_val

with key:
goal_position: x_val, y_val, z_val
"""
class AirSimCarInterceptEnv(AirSimEnv):
    def __init__(self, ip_address, self_control_escaper, self_control_catcher):
        super().__init__((84, 84, 1))  # image shape for default gym env
        self.start_ts = 0
        ## self control setup
        self.control_escaper = self_control_escaper
        self.control_catcher = self_control_catcher

        ## observation 
        self.car_state = {
            "Escaper" : CarState(),
            "Catcher" : CarState()
        } 

        ## action
        self.car_controls = {
            "Escaper":airsim.CarControls(),
            "Catcher":airsim.CarControls()
        }

        ## car client, connect to airsim unreal simulator
        self.cars = airsim.CarClient(ip=ip_address)


    # reset to origin state
    def _setup_car(self):
        self.cars.enableApiControl(True,"Catcher") if not self.control_catcher else self.cars.enableApiControl(False,"Catcher")
        self.cars.enableApiControl(True,"Escaper") if not self.control_escaper else self.cars.enableApiControl(False,"Escaper")
        self.cars.armDisarm(True,"Catcher") if not self.control_catcher else self.cars.enableApiControl(False,"Catcher")
        self.cars.armDisarm(True,"Escaper") if not self.control_escaper else self.cars.enableApiControl(False,"Escaper")
        time.sleep(0.01)

    def __del__(self):
        self.cars.reset()


    ## initialize action
    def _init_action(self):
        for car_style in self.car_controls.keys():
            self.car_controls[car_style].throttle = 1
            self.car_controls[car_style].brake = 0
            self.car_controls[car_style].steering = 0
        return self.car_controls

    # do action
    def _do_action(self, action): 
        self.cars.setCarControls(action["Catcher"], "Catcher") 
        self.cars.setCarControls(action["Escaper"], "Escaper")

    # get observation
    def _get_car_state(self):
        for car_role in ["Escaper", "Catcher"]:
            self.car_state[car_role].position = self.cars.simGetObjectPose(car_role).position
            self.car_state[car_role].linear_acceleration = self.cars.getCarState(car_role).kinematics_estimated.linear_acceleration  
            self.car_state[car_role].linear_velocity = self.cars.getCarState(car_role).kinematics_estimated.linear_velocity
            self.car_state[car_role].angular_accerleration = self.cars.getCarState(car_role).kinematics_estimated.angular_acceleration
            self.car_state[car_role].angular_velocity = self.cars.getCarState(car_role).kinematics_estimated.angular_velocity
            self.car_state[car_role].orientation = self.cars.getCarState(car_role).kinematics_estimated.orientation
            img_response = self.cars.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False),
                                            airsim.ImageRequest("0", airsim.ImageType.DepthVis, False, False)], car_role)
            img_rgb = np.fromstring(img_response[0].image_data_uint8, dtype=np.uint8) 
            self.car_state[car_role].img_rgb = img_rgb.reshape(img_response[0].height, img_response[0].width, 3)
            img_depth = np.fromstring(img_response[1].image_data_uint8, dtype=np.uint8) 
            self.car_state[car_role].img_depth = img_depth.reshape(img_response[1].height, img_response[1].width, 3)
            self.car_state[car_role].lidar_data = self.cars.getLidarData("Lidar1", car_role)
        return self.car_state

    def _get_obs(self):
        obs = self._get_car_state()
        obs["goal_position"] = self.cars.simGetObjectPose("Goal").position
        return obs

    # compute reward
    def _compute_reward(self):
        reward = 0
        return reward
    
    # compute ending condition
    def _if_end(self):
        done = False
        info = False
        escaper_position = self.car_state["Escaper"].position
        catcher_position = self.car_state["Catcher"].position
        goal_position = self.cars.simGetObjectPose("Goal").position
        r_b_distance = np.linalg.norm([escaper_position.x_val-catcher_position.x_val, \
                escaper_position.y_val-catcher_position.y_val,escaper_position.z_val-catcher_position.z_val])
        r_g_distance = np.linalg.norm([escaper_position.x_val-goal_position.x_val, \
                escaper_position.y_val-goal_position.y_val,escaper_position.z_val-escaper_position.z_val])

        if r_b_distance < 8:
            # Catcher catch escaper
            done = True
            info = "Being caught"
        elif escaper_position.z_val > 10:
            # one of the car fall out of playground
            done = True
            info = "escaper fall off playground"
        elif catcher_position.z_val > 10:
            # one of the car fall out of playground
            done = True
            info = "catcher fall off playground"
        elif r_g_distance < 15:
            done = True
            info = "Reach goal"
        return info, done

    def step(self, action):
        actions = copy.deepcopy(action)
        self._do_action(actions)
        obs = self._get_obs()
        info, done = self._if_end()
        reward = self._compute_reward()
        if done:
            self.cars.simPrintLogMessage(info, message_param='', severity=3)
        return copy.deepcopy(obs), reward, done, info

    def reset(self):
        self._setup_car()
        action = self._init_action()
        self._do_action(action)
        done = False
        return copy.deepcopy(self._get_obs()), copy.deepcopy(action), done

    def add_vehicle(self, vehicle_name, position, vehicle_type):
        if vehicle_name in self.cars.listVehicles():
            print("warning!! car: ", vehicle_name, "exist, destroying it!")
            self.cars.simDestroyObject(vehicle_name)
        created = self.cars.simAddVehicle(vehicle_name=vehicle_name, vehicle_type=vehicle_type, pose=position)
        print(vehicle_name," car created?", created)

    def del_vehicle(self, vehicle_name):
        if vehicle_name not in self.cars.listVehicles():
            print("warning!! car: ", vehicle_name, "not exist! wont delete anything!")
            return
        self.cars.simDestroyObject(vehicle_name)

    def spawn_object(self, name, object_name, pose, scale, physic_enabled, is_blueprint):
        self.cars.simSpawnObject(name, object_name, pose, scale, physic_enabled, is_blueprint)

class CarState():
    position = airsim.Vector3r()
    orientation = airsim.Quaternionr()
    linear_velocity = airsim.Vector3r()
    angular_velocity = airsim.Vector3r()
    linear_acceleration = airsim.Vector3r()
    angular_accerleration = airsim.Vector3r()
    img_rgb = None
    img_depth = None
    lidar_data = None

