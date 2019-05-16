# Toy Helicopter SLAM
**Yuchen Wang**

*Northwestern University*


## Introduction
The goal of this project is to implement SLAM for a quadcopter.

## Hardware
### Parts List
Frame: [DJI Flamewheel F450](https://docs.px4.io/en/frames_multicopter/dji_flamewheel_450.html) ($230)

Controller: [Pixracer](https://docs.px4.io/en/flight_controller/pixracer.html) ($99)

Sensors: HTC Vive Lighthouse, [Lidar-Lite V3](https://buy.garmin.com/en-US/US/p/557294) ($130)

### Wiring Instruction
There are specs and examples online showing the detailed wiring instruction.

According to PX4 website, it's possible to control Blade 130X helicopter using pixhawk. However, considering the size of the helicopter is not capable of extra sensors or cameras, I decided not to use that.

## Code
### Particle Filter
Monte Carlo localization (MCL), also known as particle filter localization, is an algorithm for robots to localize using a particle filter. Given a map of the environment, the algorithm estimates the position and orientation of a robot as it moves and senses the environment. The algorithm uses a particle filter to represent the distribution of likely states, with each particle representing a possible state, i.e., a hypothesis of where the robot is.[4] The algorithm typically starts with a uniform random distribution of particles over the configuration space, meaning the robot has no information about where it is and assumes it is equally likely to be at any point in space.  Whenever the robot moves, it shifts the particles to predict its new state after the movement. Whenever the robot senses something, the particles are resampled based on recursive Bayesian estimation, i.e., how well the actual sensed data correlate with the predicted state. Ultimately, the particles should converge towards the actual position of the robot.

In this project, the verticle distance from the quadcopter to the 3D map would be measured by lidar sensor. Giving the data, Particle Filter will generate a series of possible locations in the map to represent the current position and update the candidates each time.