import numpy as np

def polar_to_cartesian(pol_loc, pol_vel):
	'''converts an arrays of [r, phi, z] and [rad_vel, ang_vel, z_vel] 
	into [x,y, z] and [x', y', z'].	Takes and returns shape(N, 3)'''
	
	#put input into intuitive form
	r = pol_loc[:,0]
	phi = pol_loc[:,1]
	z = pol_loc[:,2]
	rad_vel = pol_vel[:,0]
	ang_vel = pol_vel[:,1]
	z_vel = pol_vel[:,2]
	
	#make transformation
	x = r*np.cos(phi)
	y = r*np.sin(phi)
	x_vel = rad_vel*np.cos(phi) - r*ang_vel*np.sin(phi)
	y_vel = rad_vel*np.sin(phi) + r*ang_vel*np.cos(phi)

	return np.transpose([x, y, z]), np.transpose([x_vel, y_vel, z_vel])
	

def get_real_phi(loc):
	'''returns the angle of an object from the origin, given its cartesian location.
	Real_phi monotonically increases. ie not restricted to [0,2pi)'''
	
	phi = np.arctan2(loc[:,1], loc[:,0])			#restricted to [0,2pi)
	
	#every time phi decreases significantly, this means that it has gone 
	#over the range [0,2pi), so need to add 2pi every time this happens 
	increment = np.diff(phi)						
	increment = np.insert(increment, 0, 0)		#make same length as phi
	to_add = np.cumsum(np.where(increment<-1, 2*np.pi, 0))
	real_phi = phi+to_add
	return real_phi
	
