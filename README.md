# Airsim carintercept env

### Airsim Installation

1. install visual studio 2019 https://docs.microsoft.com/en-us/visualstudio/releases/2019/release-notes
    - select 使用C++的桌面开发” under 工作负荷
    - select “Windows 10 SDK 10.0.18362”
    - select 使用.NET桌面开发
    - after installation complete, restart destop

2. install Unreal engine https://www.unrealengine.com/zh-CN/
    - you need to sign up for an epic game account
    - install epic games
    
    <img width="640" height="640" src="https://user-images.githubusercontent.com/85209880/144985961-1da6be19-5e89-4fd1-a2c2-f09471875dcd.png"/>
    
    - install unreal engine 
    
    <img width="640" height="640" src="https://user-images.githubusercontent.com/85209880/144958513-2d4bb89b-0682-4177-a71c-4dd4e61806bb.png"/>
    
    - select version 4.26
    
3. install Airsim
    - open "Developer Command Prompt for VS 2019"
    - git clone https://github.com/zewuzheng17/Airsim.git(if dont work, go to https://github.com/zewuzheng17/Airsim and download zip file directly)
    - cd Airsim
    - build.cmd(you'd better use vpn)
 

4. Car intercept project
    - link: https://pan.baidu.com/s/13iTxV4SKaksK9brcbeJs2A 提取码：zzw1
    - unzip Carintercept
    - open unreal editor, choose CarIntercept\CarIntercept.uproject project

5. Airsim python client
    - prerequisite: 'msgpack-rpc-python', 'numpy', 'opencv-contrib-python', 'gym'
    - cd Airsm/Airsim/PythonClient
    - run pip install -e . (install local airsim package in python)
    - cd Airsim/Airsim/pythonClient/reinforcement_learning/
    - run pip install -e . (install local airgym package in python)
    
6. settings.json
    - put Airsim/settings.json into 此电脑/文档/Airsim/ 

7. Go to Airsim/PythonClient/reinforcement_learning/airgym/envs/
   - test_noxbox.py (the files that test gym env with no xbox control)
   - car_intercept_env.py (gym envs)
   - test.py (test gym with xbox control)
    
### airgym
    - gym envs and relative files are in Airsim/PythonClient/reinforcement_learning/airgym/envs/
    
### Use other environment from unreal marketplace and add airsim as plugin
    - https://zhuanlan.zhihu.com/p/271953448
