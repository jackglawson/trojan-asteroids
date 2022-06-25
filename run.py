import numpy as np
from numpy import pi
from simulate import run_sim
from other_functions import polar_to_cartesian


def run(rad_disp=0, ang_disp=0, z_disp=0, rad_vel=0, ang_vel=0, z_vel=0, 
	planet_mass=0.001, tot_t=100*11.85):
	'''run the simulation given the displacement of the test mass from L4.
	Returns times and sun, jup, test, L4 bodies with propagated positions attached'''
	
	class Sun():
		def __init__(self):
			self.loc = [0,0,0]
			self.vel = [0,0,0]
			self.m = 1
	
	class Planet():
		def __init__(self):
			self.loc = [0,0,0]
			self.vel = [0,0,0]
			self.m = planet_mass
	
	class TestMass():
		def __init__(self):
			self.loc = [0,0,0]
			self.vel = [0,0,0]
	
	#initialise the bodies
	sun = Sun()
	jup = Planet()
	test = TestMass()
	L4 = TestMass()
	
	#ang vel of orbit of jupiter in the two-body problem
	w = np.sqrt(4*pi**2*(sun.m+jup.m)/5.2**3)
	
	#set up initial conditions of bodies
	sun_r = 5.2*jup.m/(sun.m+jup.m)
	sun.loc, sun.vel =  polar_to_cartesian(
		np.array([[5.2*jup.m/(sun.m+jup.m), pi, 0]]), 
		np.array([[0, w, 0]]))
	jup.loc, jup.vel = polar_to_cartesian(
		np.array([[5.2*sun.m/(sun.m+jup.m), 0, 0]]), 
		np.array([[0, w, 0]]))
	
	k = sun.m/(sun.m+jup.m)			#k, a and theta as defined in equations 10-12
	a = 5.2*np.sqrt(k**2-k+1)
	theta = np.arccos((2*k-1)/(2*np.sqrt(k**2-k+1)))
	test.loc, test.vel = polar_to_cartesian(
		np.array([[a+rad_disp, theta+ang_disp, z_disp]]), 
		np.array([[rad_vel, w+ang_vel, z_vel]]))
	
	
	#run the simulation.
	#We replace the initial conditions stored in the objects with a 2D 
	#array of their propagated positions and velocities
	times, sun, jup, test, L4 = run_sim(sun, jup, test, L4, tot_t)
	return times, sun, jup, test, L4
