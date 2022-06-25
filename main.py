#this file is a useful space to run the simulation from

from run import run
from visualise import animate
from visualise import plot

times, sun, jup, test, L4 = run(rad_disp=0.05)		
plot(sun, jup, test, L4)
animate(sun, jup, test, L4)
