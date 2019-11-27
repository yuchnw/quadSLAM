# Quadcopter Lidar Sensing and Mapping
**Yuchen Wang**

*Northwestern University*


## Introduction
The goal of this project is to implement 3D mapping for a quadcopter.

## Hardware
### Parts List
Frame: [DJI Flamewheel F450](https://www.dji.com/flame-wheel-arf) ($230)

Controller: [Pixracer](https://docs.px4.io/en/flight_controller/pixracer.html) ($99)

Sensor: HTC Vive Lighthouse, [Lidar-Lite V3](https://buy.garmin.com/en-US/US/p/557294) ($130)

Power Module: AUAV [Power Module](https://store.mrobotics.io/product-p/auav-acsp4-mr.htm)(ACSP4)

Battery: Turnigy 3000mAh 3S 20C [Lipo Battery](https://www.amazon.com/Turnigy-3000mAh-Lipo-Pack-XT-60/dp/B075RTRWSC/ref=sr_1_25?gclid=EAIaIQobChMIz9OKqtuI5gIV7x6tBh2aNwcOEAAYASAAEgLsMPD_BwE&hvadid=178102491821&hvdev=c&hvlocphy=9021565&hvnetw=g&hvpos=1t1&hvqmt=e&hvrand=307303628176748876&hvtargid=kwd-13703202200&hydadcr=2113_9907432&keywords=lipo+3s+3000mah&qid=1574800068&sr=8-25)


### Assemble Instruction
According to PX4 website, it's possible to control multiple types if UAV using pixhawk. However, considering the size of any extra sensor or camera, I decided to use DJI Flamewheel F450 and the Pixracer controller.

The original drone kit was a pack of parts including 4 motors, 4 propellors, 4 ESCs, 2 main boards, 4 frame bases, and necessary screws. To assemble the quadcopter, I mostly followed the official DJI [tutorial](https://www.youtube.com/watch?v=pUTHIL_Xfcc). However, since I am using pixhawk instead of the included Maza flight controller system, I slightly adjust the arrangement of the electronic parts. As the figure shows, the power module is in between of the top board and bottom board, with the battery port and ESCs soldered on. The pixhawk and WiFi module(ESP8266) are put at the top board with a piece of foam to reduce vibration.

There are specs and examples online showing the detailed wiring instruction.


## PX4 Configuration
### QGroundControl
After the assembly being properly done, the quad should be connected and configured at ground station. In this case, QGroundControl has been selected since it's the default ground station UI for PX4. Following the instruction online to install QGC on a laptop, the next step would be connect/pair the pixhawk with it. After booting the pixracer, the WiFi module plugged on that should be able to establish a local WiFi network with the name **ArduPilot** with password **ardupilot**. Connect to that network on the laptop and then launch QGC, wait for a few seconds, QGC will show that it has successfully connected to the pixhawk. All the parameters and current status of the flight controller will be displayed.

### Configuration and Tuning

### Companion Computer
#### ROS Installation

## Lidar Sensor

## Code
### Particle Filter
Monte Carlo localization (MCL), also known as particle filter localization, is an algorithm for robots to localize using a particle filter. Given a map of the environment, the algorithm estimates the position and orientation of a robot as it moves and senses the environment. The algorithm uses a particle filter to represent the distribution of likely states, with each particle representing a possible state, i.e., a hypothesis of where the robot is.[4] The algorithm typically starts with a uniform random distribution of particles over the configuration space, meaning the robot has no information about where it is and assumes it is equally likely to be at any point in space.  Whenever the robot moves, it shifts the particles to predict its new state after the movement. Whenever the robot senses something, the particles are resampled based on recursive Bayesian estimation, i.e., how well the actual sensed data correlate with the predicted state. Ultimately, the particles should converge towards the actual position of the robot.

In this project, the verticle distance from the quadcopter to the 3D map would be measured by lidar sensor. Giving the data, Particle Filter will generate a series of possible locations in the map to represent the current position and update the candidates each time.

![init](/img/init.png)
![2](/img/2.png)
![1](/img/1.png)
