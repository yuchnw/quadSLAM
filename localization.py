import numpy as np
import random
from math import *
import random

class ParticleFilter:

	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0
		self.noise = 0.0
		self.particles = []

	def getLidar(self,z):
		"""
		Retrive vertical distance data from lidar sensor
		"""
		return 0

	def getZ(self,map,x,y):
		"""
		Return verticle distance to the real map
		"""
		return map[x][y]


	def withinRange(self,actual,estimated,thresh):
		error = float((actual - estimated) / estimated)
		if abs(error) < thresh:
			return True
		else:
			return False

	def getCandidates(self,map,add_noise=False):
		canidate = []
		currentZ = getLidar(self.z)
		for i in range(len(map)):
			for j in range(len(map[0])):
				z = getZ(map[i]map[j])
				if withinRange(currentZ,z,0.05):
					canidate.append([i,j])

	def correct(self):
		