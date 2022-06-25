import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from other_functions import get_real_phi
from run import run
import scipy.stats as stats
from visualise import plot


def calc_wander_1D(r):
	'''
	Calculates the wander and tests stability of the array of rs inputted.
	Saves wander.txt, stable.txt and r.txt 
	Can easily be modified for a different independent variable
	'''
	
	def wander_func_1D(r):
		'''returns the wander and stability, given a delta r'''
		
		times, sun, jup, test, L4 = run(rad_disp=r)
		dist_from_L4 = np.linalg.norm(test.loc-L4.loc, axis=1)
		wander = np.max(dist_from_L4)
		
		#An orbit is unstable if it deviates more than 2pi from L4
		rel_phi = get_real_phi(test.loc)-get_real_phi(L4.loc)
		if np.max(rel_phi) > 2*pi or np.min(rel_phi) < -2*pi:
			stable = False
		else:
			stable = True
				
		return wander, stable


	vwander = np.vectorize(wander_func_1D)
	wander, stable = vwander(r)

	np.savetxt('wander.txt', wander)
	np.savetxt('stable.txt', stable)
	np.savetxt('r.txt', r)


def plot_wander_1D():
	'''Plots the wander against r. Gives different colours for stable and unstable'''
	wander = np.loadtxt('wander.txt')
	stable = np.loadtxt('stable.txt')
	r = np.loadtxt('r.txt')
	
	#sort the stable and unstable orbits into separate data sets
	wander_stable = np.extract(stable==True, wander)
	r_stable = np.extract(stable==True, r)
	wander_unstable = np.extract(stable==False, wander)
	r_unstable = np.extract(stable==False, r)

	plt.scatter(r_stable, wander_stable, color='k', s=3, label='Stable')
	plt.scatter(r_unstable, wander_unstable, color='r', s=3, label='Unstable')
	plt.xlabel('$\Delta r$, AU')
	plt.ylabel('wander, AU')
	plt.legend()
	plt.show()	


def fit_log_wander_1D():
	'''plots log(wander) against log(r) and fits a straight line to it.
	Prints the parameters for the line'''
	r = np.loadtxt('r.txt')
	wander = np.loadtxt('wander.txt')

	reg = stats.linregress(np.log(r), np.log(wander))
	print(reg)
	def bestfit(x):
		return x*reg.slope + reg.intercept 

	plt.plot(np.log(r), np.log(wander))
	plt.plot(
		[min(np.log(r)), max(np.log(r))], 
		[bestfit(min(np.log(r))), bestfit(max(np.log(r)))])
	plt.xlabel('log(r)')
	plt.ylabel('log(wander)')
	plt.show()


r = np.linspace(0.01, 0.15, 11)
calc_wander_1D(r=r)
plot_wander_1D()
fit_log_wander_1D()
