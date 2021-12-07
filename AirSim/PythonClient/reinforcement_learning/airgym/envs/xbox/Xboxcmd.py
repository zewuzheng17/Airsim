import pygame
import time

def get_axis(joystick):
    joystick.init()
    numaxes = joystick.get_numaxes()
    axis = []
    for i in range(numaxes):
        axis.append(joystick.get_axis(i))
    return axis

def get_button(joystick):
    joystick.init()
    numbuttons = joystick.get_numbuttons()
    button = []
    for i in range(numbuttons):
        button.append(joystick.get_button(i))
    return button

def get_hats(joystick):
    joystick.init()
    numhats = joystick.get_numhats()
    hat = []
    for i in range(numhats):
        hat.append(joystick.get_hat(i))
    return hat

if __name__ == "__main__":
    #pygame 初始化
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
        print(button)
        print("hat_value")
        print(hats)
        print("_____________")
        time.sleep(3)


