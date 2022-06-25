import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from other_functions import get_real_phi
from other_functions import polar_to_cartesian
from run import run
from visualise import plot
import scipy.stats as stats


def calc_wander_m(r, m):
	'''
	Calculates the wander and tests stability of the array of ms inputted.
	Requires an initial radial displacement.
	Saves masses.txt, containing arrays for ms, stable and wander
	'''
	
	def wander_func_m(r, m):
		'''returns the wander and stability, given a delta r and m.
		Runs the sim for 1000 orbits, rather than the default of 100'''
		
		times, sun, jup, test, L4 = run(rad_disp=r, planet_mass=m, tot_t=11.85*1000)
		dist_from_L4 = np.linalg.norm(test.loc-L4.loc, axis=1)
		wander = np.max(dist_from_L4)
		
		rel_phi = get_real_phi(test.loc)-get_real_phi(L4.loc)
		if np.max(rel_phi) > 2*pi or np.min(rel_phi) < -2*pi:
			stable = False
		else:
			stable = True
		
		return wander, stable

	vwander = np.vectorize(wander_func_m)
	wander, stable = vwander(0.00001, m)
	np.savetxt('masses.txt', [m, stable, wander])
	

def plot_wander_m():
	''' plots log(m) against log(wander), with different colours for stable and unstable'''
	m, stable, wander = np.loadtxt('masses.txt')
	
	#sort the stable and unstable orbits into separate data sets
	wander_stable = np.extract(stable==True, wander)
	m_stable = np.extract(stable==True, m)
	wander_unstable = np.extract(stable==False, wander)
	m_unstable = np.extract(stable==False, m)

	plt.scatter(
		np.log10(m_stable), np.log10(wander_stable), 
		color='k', s=3, label='Stable')
	plt.scatter(
		np.log10(m_unstable), np.log10(wander_unstable), 
		color='r', s=3, label='Unstable')
	plt.xlabel(r'$\log_{10}(M/M_{\odot})$')
	plt.ylabel(r'$\log_{10}(wander/AU)$')
	plt.legend()
	plt.show()	


def fit_log_wander_m():
	'''fits a straight line to the log-log graph and prints the parameters'''
	m, stable, wander = np.loadtxt('masses.txt')
	
	reg = stats.linregress(np.log(m), np.log(wander))
	print(reg)
	
	def bestfit(logm):
		return logm*reg.slope + reg.intercept 

	plt.plot(np.log(m), np.log(wander))
	plt.plot(
		[min(np.log(m)), max(np.log(m))], 
		[bestfit(min(np.log(m))), bestfit(max(np.log(m)))])
	plt.xlabel('log(mass)')
	plt.ylabel('log(wander)')
	plt.show()	


m = np.geomspace(0.0001, 0.1, num=20)
calc_wander_m(0.001, m)
plot_wander_m()
fit_log_wander_m()
