import time
from Xboxcmd import *
import pygame

pygame.init()
pygame.joystick.init()

#查看现在有几个遥控器
joycount = pygame.joystick.get_count()
print("joycount:"+str(joycount))

#连接第一个控制器
joystick = pygame.joystick.Joystick(0)

while True:
    #接收事件
    pygame.event.get()

    axis = get_axis(joystick=joystick)
    button = get_button(joystick=joystick)
    hats = get_hats(joystick=joystick)

    print("_____________")
    print(" axis_value:")
    print(axis)
    print(" button_value")
    print(button[3])
    print("hat_value")
    print(hats)
    print("_____________")
    time.sleep(3)
