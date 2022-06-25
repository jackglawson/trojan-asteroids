import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from other_functions import polar_to_cartesian

def animate(sun, jup, test, L4):
	'''takes the objects and animates them using funcanimation'''
	
	#defined quanitites
	num_of_frames = len(sun.loc[:,0])
	display_rate = 10		#display every n frames
	frame_interval = 1000/60
	
	fig = plt.figure()
	ax = plt.axes()
	ax.axis('scaled')	
	ax.set_xlim(-8, 8)
	ax.set_ylim(-8, 8)
	lines = [plt.plot([], [])[0] for _ in range(4)]		#points to animate	


	def init():
		'''initialisation function for FuncAnimation'''
		for i in range(len(lines)):
			lines[i].set_data([],[])
			lines[i].set_marker('.')
		lines[0].set_color('r')		#sun
		lines[1].set_color('b')		#Jupiter
		lines[2].set_color('k')		#test
		lines[3].set_color('0.5')	#L4
		lines[3].set_marker('+')	#L4
		return lines


	def update_screen(i):
		'''update function for FuncAnimation'''
		frame = i*display_rate
		lines[0].set_data([sun.loc[frame,0]], [sun.loc[frame,1]])	#sun
		lines[1].set_data([jup.loc[frame,0]], [jup.loc[frame,1]])	#Jupiter
		lines[2].set_data([test.loc[frame,0]], [test.loc[frame,1]])	#test
		lines[3].set_data([L4.loc[frame,0]], [L4.loc[frame,1]])		#L4
		return lines
		

	ani = FuncAnimation(
		fig, update_screen, frames=np.arange(0, num_of_frames), 
		init_func=init, blit=True, interval=frame_interval)
		
	plt.show()


def plot(sun, jup, test, L4):
	'''plots the motion of the test mass in a co-rotating frame'''
	fig, ax = plt.subplots()
	ax.axis('scaled')
	
	#find the coordinates in the co-rotating frame:
	test_x = test.loc[:,0]
	test_y = test.loc[:,1]
	jup_x = jup.loc[:,0]
	jup_y = jup.loc[:,1]
	jup_phi = np.arctan2(jup_y, jup_x)
	test_x_rot_frame = test_x*np.cos(jup_phi) + test_y*np.sin(jup_phi)
	test_y_rot_frame = -test_x*np.sin(jup_phi) + test_y*np.cos(jup_phi)
	
	#plot everything, making sure whole trajectory is shown
	ax.set_xlim(
		min(-1, min(test_x_rot_frame))-0.2, 
		max(6, max(test_x_rot_frame))+0.2)	
	ax.set_ylim(
		min(-1, min(test_y_rot_frame))-0.2, 
		max(6, max(test_y_rot_frame))+0.2)
	ax.plot(test_x_rot_frame, test_y_rot_frame, 'k', linewidth=1)	#test
	ax.add_artist(plt.Circle(sun.loc[0,0:2], 0.5, color='y'))		#sun
	ax.add_artist(plt.Circle(jup.loc[0,0:2], 0.1, color='b'))		#jupiter
	ax.scatter(L4.loc[0,0], L4.loc[0,1], c='r', marker='+')			#L4
	plt.show()

