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
    - build.cmd
 
4. Use environment from unreal marketplace and add airsim as plugin
    - https://zhuanlan.zhihu.com/p/271953448

### Car intercept project
    - link: https://pan.baidu.com/s/13iTxV4SKaksK9brcbeJs2A 提取码：zzw1

### Airsim python client
    - prerequisite: 'msgpack-rpc-python', 'numpy', 'opencv-contrib-python'
    - cd Airsm/Airsim/pythonClient
    - run pip install -e . (install local airsim package in python)
    - cd Airsim/Airsim/pythonClient/reinforcementlearning/
    - run pip install -e . (install local airgym package in python)
    
### settings.json
    - put this file into 文档/Airsim/ 
