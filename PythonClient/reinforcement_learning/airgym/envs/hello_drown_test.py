import airsim
import numpy as np


# connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()

# add new vehicle
vehicle_name = "Drone2"
pose = airsim.Pose(airsim.Vector3r(0, 10, 0), airsim.to_quaternion(0, 0, 0))

client.simAddVehicle(vehicle_name, "physxcar", pose)
client.enableApiControl(True, vehicle_name)
client.armDisarm(True, vehicle_name)
# client.takeoffAsync(10.0, vehicle_name)
