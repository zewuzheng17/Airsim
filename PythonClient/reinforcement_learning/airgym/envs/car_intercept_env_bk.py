import airsim
import numpy as np
import time
from gym import spaces
from airgym.envs.airsim_env import AirSimEnv


class AirSimCarInterceptEnv(AirSimEnv):
    def __init__(self, ip_address, car_names = ["Catcher"], 
                    car_pose = [{"orientation":
                                    {
                                        "w_val":0,
                                        "x_val":0,
                                        "y_val":0,
                                        "z_val":0,
                                    }, 
                                "position":
                                    {
                                        "x_val":0,
                                        "y_val":180,
                                        "z_val":0,
                                    }
                                }],
                    pawn_path = ["Class'/AirSim/VehicleAdv/SUV/SuvCarPawn.SuvCarPawn_C'"]):
        super().__init__((84, 84, 1))  # image shape for default gym env
        self.car_names = car_names
        self.car_pose = car_pose
        self.pawn_path = pawn_path
        self.cars = airsim.CarClient(ip=ip_address) ## connect to simulator
        ## observation 
        self.car_state = {}   
        ## car control
        self.car_controls = {}

    # set up default escaper
    def _setup_Escaper(self):
        self.cars.enableApiControl(True, "Escaper")
        self.cars.armDisarm(True, "Escaper")
        self.car_state["Escaper"] = {
                            "orientation":
                                    {
                                        "w_val":0,
                                        "x_val":0,
                                        "y_val":90,
                                        "z_val":0,
                                    }, 
                                "position":
                                    {
                                        "x_val":0,
                                        "y_val":0,
                                        "z_val":0,
                                    }
                                }
        self.car_controls["Escaper"] = airsim.CarControls()

    def _add_vehicles(self):
        poses = airsim.Pose(airsim.Vector3r(0, 0, -20), airsim.to_quaternion(0, 0, 0))
        simcreate1 = self.cars.simAddVehicle("Catcher11", "PhysXCar", poses)
        print("multirotor created?", simcreate1)
        try:
            for name, pose, path in zip(self.car_names, self.car_pose, self.pawn_path):
                simcreate = self.cars.simAddVehicle("Catcher", "PhysXCar", poses)
                print("created or not?", simcreate)
                time.sleep(15)
                print(self.cars.listVehicles())
                self.cars.enableApiControl(True,name)
                self.cars.armDisarm(True,name)
                self.car_state[name] = pose 
                self.car_controls[name] = airsim.CarControls()
        except:
            raise ValueError("Caonnot add vehicles, please check if parameters are correct!")

    # reset to origin state
    def _setup_car(self):
        self.cars.reset() ## reset environment
        self._setup_Escaper() ## setup default escaper
        self._add_vehicles() ## add cars
        time.sleep(0.01)

    # do action
    def _do_action(self, action):
        try:
            for name in action.keys():
                assert name in self.car_controls.keys()
                self.car_controls[name].brake = 0
                self.car_controls[name].throttle = 1
                if action[name] == 0:
                    self.car_controls[name].throttle = 0
                    self.car_controls[name].brake = 1
                elif action[name] == 1:
                    self.car_controls[name].steering = 0
                elif action[name] == 2:
                    self.car_controls[name].steering = 0.5
                elif action[name] == 3:
                    self.car_controls[name].steering = -0.5
                elif action[name] == 4:
                    self.car_controls[name].steering = 0.25
                else:
                    self.car_controls[name].steering = -0.25
                self.cars.setCarControls(self.car_controls[name], name) 
        except:
            raise KeyError("Cannot find relevant vehicles \
                        for given actions, please check keys in action")

    # get observation
    def _get_obs(self):
        for name in self.car_state:
            self.car_state[name] = self.cars.simGetObjectPose(name)
        return self.car_state

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
        info = False
        red_car_position = self.car_state["Eacaper"].position
        blue_car_position = self.car_state["Catcher"].position
        goal_position = self.cars.simGetObjectPose("Goal").position
        r_b_distance = np.linalg.norm([red_car_position.x_val-blue_car_position.x_val, \
                red_car_position.y_val-blue_car_position.y_val,red_car_position.z_val-blue_car_position.z_val])
        r_g_distance = np.linalg.norm([red_car_position.x_val-goal_position.x_val, \
                red_car_position.y_val-goal_position.y_val,red_car_position.z_val-goal_position.z_val])
        if r_b_distance < 5:
            # Catcher catch escaper
            done = True
            info = "Catched"
        elif red_car_position.z_val > 5 or blue_car_position.z_val > 5:
            # one of the car fall out of playground
            done = True
            info = "One of the agents fall out of playground"
        elif r_g_distance < 5:
            done = True
            info = "Reached Target"
        return done, info

    def __del__(self):
        self.cars.reset()

    ## gym api for user
    def step(self, action):
        self._do_action(action)
        obs = self._get_obs()
        reward = self._compute_reward()
        done, info = self._if_end()
        return obs, reward, done, info

    def reset(self):
        self._setup_car()


