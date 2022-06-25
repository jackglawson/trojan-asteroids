import matplotlib.pyplot as plt
import scipy.integrate as integ
import time
import numpy as np
from numpy import pi
from other_functions import polar_to_cartesian


def run_sim(sun, jup, test, L4, tot_t):
	'''Uses scipy.odeint to propagate from the initial conditions. 
	Automatically calculates position of L4.
	Replaces initial conditions in objects with propagated conditions'''
	start_time = time.time()
	
	#defined quantities
	dt = 1e-2
	G = 4*pi**2
	iterations = int(tot_t/dt)

	def derivs(y, t, sun, jup):		
		'''Equations of motion to solve. The input y must be a 1D array, 
		and is organised as [x,y,z,x',y',z'], repeated for the number of bodies. 
		Sun and jup must be passed to access their masses.'''

		#converting back to an intuitive form
		sun_loc = y[0:3]
		sun_vel = y[3:6]
		jup_loc = y[6:9]
		jup_vel = y[9:12]
		test_loc = y[12:15]
		test_vel = y[15:18]
			
		jup_acc = -G*sun.m*(jup_loc-sun_loc)/np.linalg.norm(jup_loc-sun_loc)**3
		sun_acc = -G*jup.m*(sun_loc-jup_loc)/np.linalg.norm(sun_loc-jup_loc)**3
		test_acc = (-G*sun.m*(test_loc-sun_loc)/np.linalg.norm(test_loc-sun_loc)**3
					-G*jup.m*(test_loc-jup_loc)/np.linalg.norm(test_loc-jup_loc)**3)				
		
		ydot = np.hstack(
			(sun_vel, sun_acc, jup_vel, jup_acc, test_vel, test_acc))	
		return ydot


	#locs and vels must be in a 1D array
	y0 = np.ndarray(18)
	y0[0:3] = sun.loc[0]
	y0[3:6] = sun.vel[0]
	y0[6:9] = jup.loc[0]
	y0[9:12] = jup.vel[0]
	y0[12:15] = test.loc[0]
	y0[15:18] = test.vel[0]
	
	solution = integ.odeint(derivs, y0, np.linspace(0., tot_t, iterations), args=(sun, jup))
	
	#replace initial conditions with propagated locs and vels
	sun.loc = solution[:, 0:3]
	sun.vel = solution[:, 3:6]
	jup.loc = solution[:, 6:9]
	jup.vel = solution[:, 9:12]
	test.loc = solution[:, 12:15]
	test.vel = solution[:, 15:18]
	
	#Calculate position of L4
	phi = np.arctan2(jup.loc[:,1], jup.loc[:,0])	
	k = sun.m/(sun.m+jup.m)
	a = np.ndarray((iterations))
	a[:] = 5.2*np.sqrt(k**2-k+1)
	theta = np.arccos((2*k-1)/(2*np.sqrt(k**2-k+1)))
	L4.loc = polar_to_cartesian(
		np.transpose([a, theta+phi, np.zeros((iterations))]), 
		np.array([[0, 0, 0]]))[0] 	#ang_vel doesnt matter - we only want location of L4
	
	times = np.arange(iterations)*dt	
	
	print('Time taken to run sim: '+str(time.time()-start_time)+' seconds')		
	return times, sun, jup, test, L4
