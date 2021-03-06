# Quadcopter Lidar Sensing and Mapping
**Yuchen Wang**

*Northwestern University*


## Introduction
The goal of this project is to implement 3D mapping for a quadcopter using lidar sensor.

## Hardware
### Parts List
Frame: [DJI Flamewheel F450](https://www.dji.com/flame-wheel-arf) ($230)

Controller: [Pixracer](https://docs.px4.io/en/flight_controller/pixracer.html) ($99)

Sensor: HTC Vive Lighthouse, [Lidar-Lite V3](https://buy.garmin.com/en-US/US/p/557294) ($130)

Power Module: AUAV [Power Module](https://store.mrobotics.io/product-p/auav-acsp4-mr.htm)(ACSP4)

Battery: Turnigy 3000mAh 3S 20C [Lipo Battery](https://www.amazon.com/Turnigy-3000mAh-Lipo-Pack-XT-60/dp/B075RTRWSC/ref=sr_1_25?gclid=EAIaIQobChMIz9OKqtuI5gIV7x6tBh2aNwcOEAAYASAAEgLsMPD_BwE&hvadid=178102491821&hvdev=c&hvlocphy=9021565&hvnetw=g&hvpos=1t1&hvqmt=e&hvrand=307303628176748876&hvtargid=kwd-13703202200&hydadcr=2113_9907432&keywords=lipo+3s+3000mah&qid=1574800068&sr=8-25)


### Assemble Instruction
According to PX4 website, it's possible to control multiple types if UAV using pixhawk. However, considering the size of any extra sensor or camera, I decided to use DJI Flamewheel F450 and the Pixracer controller.

![quad](/img/quad.png)

The original drone kit was a pack of parts including 4 motors, 4 propellors, 4 ESCs, 2 main boards, 4 frame bases, and necessary screws. To assemble the quadcopter, I mostly followed the official DJI [tutorial](https://www.youtube.com/watch?v=pUTHIL_Xfcc). However, since I am using pixhawk instead of the included Maza flight controller system, I slightly adjust the arrangement of the electronic parts. As the figure shows, the power module is in between of the top board and bottom board, with the battery port and ESCs soldered on. The pixhawk and WiFi module(ESP8266) are put at the top board with a piece of foam to reduce vibration.

![power](/img/power.png)

There are specs and examples online showing the detailed wiring instruction.


## PX4 Configuration
### QGroundControl
After the assembly being properly done, the quad should be connected and configured at ground station. In this case, QGroundControl has been selected since it's the default ground station UI for PX4. Following the instruction online to install QGC on a laptop, the next step would be connect/pair the pixhawk with it. After booting the pixracer, the WiFi module plugged on that should be able to establish a local WiFi network with the name **ArduPilot** with password **ardupilot**. Connect to that network on the laptop and then launch QGC, wait for a few seconds, QGC will show that it has successfully connected to the pixhawk. All the parameters and current status of the flight controller will be displayed.

Here is the close look of the wiring of pixhawk.
![pixhawk](/img/px4.png)

### Calibration
The first time booting PX4 on pixhawk, connect pixracer to laptop using USB cable. Click **Firmware** at left side of QGroundControl and start flashing the PX4 firmware to the pixhawk. Once done, the general configuration could be set either wirelessly or using USB cable. For the convinience of setting the compass properly, I chose to do it through WiFi. After connecting pixhawk with QGC, click **Airframe** and choose **Quadrotor X** -> **DJI Flame Wheel 450**. Reboot the vehicle and then start the calibration step by step (i.e. compass, battery, sensors).

![calibrate](/img/qgc1.png)

:bangbang:Considering that RC is not used for this project, make sure to set `ARMING_CHECK` to **0**:bangbang:

### Tuning
![fly](/img/fly.gif)

### Companion Computer
As the quadcopter having a lidar sensor mounted on, it's easier and faster to process lidar data on a direct connected companion computer instead of transmitting the data to laptop using WiFi.

#### Raspberry Pi
Interfacing a companion computer (Raspberry Pi, Odroid, Tegra K1) to Pixhawk-family boards always works the same way: They are interfaced using a serial port to `TELEM 2`, the port intended for this purpose. The message format on this link is MAVLink. In order to receive MAVLink, the companion computer needs to run some software talking to the serial port. **MAVROS** has been chosen for this project to communicate to ROS node. ROS Kinetic only supports Ubuntu 16.04 and Raspbian, and Ubuntu Mate 16.04 is no longer available for Raspberry Pi, I decided to build Raspbian Jessie on RPi 3+. 

![pi](/img/pi.png)

The raspberry pi has been wired through TX/RX peripheral pins to **TELEM1** port on pixhawk.

#### ROS Installation
Follow the instruction [here](http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi) to install ROS Kinetic on RPi. Here are some notes for the installation:
* **DON'T** install packages using `sudo apt-get install`, this command doesn't work for Raspbian OS. Use `rosinstall_generator depName --rosdistro kinetic --deps -wet-only --tar > kinetic-depName-wet.rosinstall`.

* When installing MAVROS, it's highly likely that the board would get overheated. Use a mini desk fan to cool it down during the installation.

* To prevent system crash, run `catkin_make_isolated -j1` to build only one package at a time.

#### MAVPROXY
MAVProxy is a fully-functioning GCS for UAV’s. The intent is for a minimalist, portable and extendable GCS for any UAV supporting the MAVLink protocol. The companion computer communicates with the master pixhawk flight controller through MAVPROXY. It supports multiple protocols including *tcp*, *udp*, USB and serial. This project used serial connection so the connection string for MAVLINK should be **/dev/ttyAMA0**. Note that the baudrate on both the pixhawk and raspberry pi should be set to **57600**.

Once connection has been established, you can use the connection's `mavutil.messages` dictionary to synchronously access the last message of a particular type that was received (and when it was received).

## Lidar Sensor
As a compact and high-performace distance measurement device, *Lidar Lite V3* has been used to generate 3D map.
![lidar](/img/lidar.png)

The rapsberry pi will take the altitude and orientation return from pixhawk through MAVPROXY, and the distance measured by the lidar sensor, to generate a customized 3D point cloud data map. The point cloud data would be saved to a *.xyz* file and visualized in Meshlab.

Here is the point cloud map generated from the lidar sensor when it's scanning the corner of the lab room.
![piintcloud](/img/pointcloud.gif)

And this is the real environment of that corner of the lab.
![real](/img/real.gif)

## Code
### Connection
[`mavlink_control.cpp`](https://github.com/yuchnw/c_uart_interface_example/blob/master/mavlink_control.cpp) is the file that sets up the connection through MAVPROXY and retrieve data from LIDAR sensor. It comes from the original `c_uart_interface_example` [repository](https://github.com/yuchnw/c_uart_interface_example) and has been modified to establish connection and integrated with lidar data.

### Particle Filter
As the advanced goal for this project, `pf.py` is the script accomplishes localization with particle filter.

Monte Carlo localization (MCL), also known as particle filter localization, is an algorithm for robots to localize using a particle filter. Given a map of the environment, the algorithm estimates the position and orientation of a robot as it moves and senses the environment. The algorithm uses a particle filter to represent the distribution of likely states, with each particle representing a possible state, i.e., a hypothesis of where the robot is.[4] The algorithm typically starts with a uniform random distribution of particles over the configuration space, meaning the robot has no information about where it is and assumes it is equally likely to be at any point in space.  Whenever the robot moves, it shifts the particles to predict its new state after the movement. Whenever the robot senses something, the particles are resampled based on recursive Bayesian estimation, i.e., how well the actual sensed data correlate with the predicted state. Ultimately, the particles should converge towards the actual position of the robot.

In this project, the verticle distance from the quadcopter to the 3D map would be measured by lidar sensor. Giving the data, Particle Filter will generate a series of possible locations in the map to represent the current position and update the candidates each time.

![init](/img/init.png)
![2](/img/2.png)
![1](/img/1.png)
