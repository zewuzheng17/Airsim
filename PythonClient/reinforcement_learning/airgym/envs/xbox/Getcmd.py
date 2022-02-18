from .Xboxcmd import *
import pygame

class Getcmd():
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.reset = 0
        self.end = 0

    # do action
    def do_action(self, action): 
        pygame.event.get() 
        axis = get_axis(joystick=self.joystick)
        button = get_button(joystick=self.joystick) 
        action["Escaper"].throttle = 1 if int(button[3]) == 0 else 1 
        action["Escaper"].brake = 0 if int(button[0]) == 0 else 1 
        action["Escaper"].steering = float(axis[0]) / 2
        self.reset = 1 if int(button[6]) == 1 else 0
        self.end = 1 if int(button[7]) == 1 else 0
        return action

