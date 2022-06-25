import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from other_functions import get_real_phi
from other_functions import polar_to_cartesian
from run import run


def calc_wander_2D(rr, tt):
	'''
	Calculates wander and tests stability of the meshgrid of rs and ts inputted.
	t = theta = angular displacement
	Saves wander.txt, stable.txt and r.txt 
	Can easily be modified for a different independent variable
	'''
	
	def wander_func_2D(r, t):	
		'''returns the wander and stability, given a delta r and delta t'''		
		
		times, sun, jup, test, L4 = run(rad_disp=r, ang_disp=t)
		dist_from_L4 = np.linalg.norm(test.loc-L4.loc, axis=1)
		wander = np.max(dist_from_L4)
		
		rel_phi = get_real_phi(test.loc)-get_real_phi(L4.loc)
		if np.max(rel_phi) > 2*pi or np.min(rel_phi) < -2*pi:
			stable = False
		else:
			stable = True
				
		return wander, stable

	vwander = np.vectorize(wander_func_2D)
	wander, stable = vwander(rr, tt)

	np.savetxt('wander.txt', wander)
	np.savetxt('stable.txt', stable)
	np.savetxt('rr.txt', rr)
	np.savetxt('tt.txt', tt)


def plot_wander_2D():
	'''plots a 2D map of the wander. White = unstable point'''
	wander = np.loadtxt('wander.txt')
	stable = np.loadtxt('stable.txt')
	rr = np.loadtxt('rr.txt')
	tt = np.loadtxt('tt.txt')
	
	#allow plt to distinguish between stable and unstable points
	wander = np.ma.masked_where(stable==False, wander)
	my_cmap = plt.get_cmap('viridis')
	my_cmap.set_bad(color='w')
	
	plt.pcolor(tt, rr, wander, cmap=my_cmap)
	plt.xlabel(r'$\Delta \theta$, rad')
	plt.ylabel('$\Delta r$, AU')
	cbar = plt.colorbar()
	cbar.ax.set_ylabel('Range of wander, AU')
	plt.show()


r = np.linspace(-0.15, 0.15, num=20)
t = np.linspace(-0.8, 2, num=20)
rr , tt = np.meshgrid(r, t)

calc_wander_2D(rr, tt)
plot_wander_2D()
