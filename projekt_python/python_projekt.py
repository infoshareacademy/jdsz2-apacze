import pandas as pd
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from numpy import random, sqrt, log, sin, cos, pi


###Box-Muller

# transformation function
def box_muller(u1,u2):
  z1 = sqrt(-2*log(u1))*cos(2*pi*u2)
  z2 = sqrt(-2*log(u1))*sin(2*pi*u2)
  return z1,z2

# uniformly distributed values between 0 and 1
u1 = random.rand(4000)
u2 = random.rand(4000)

# run the transformation
z1,z2 = box_muller(u1,u2)

#print(z1,z2)
plt.hist(z1)
plt.hist(z2)

###Generator Python
mu, sigma = 0, 0.1
g1 = random.normal(mu, sigma, 4000)
plt.hist(g1)
plt.show()

##test Shapiro - Wilk
szapiro = scipy.stats.shapiro(z1)
print("\nShapiro-Wilk\n", szapiro)

##test Kołmogorov - Smirnov
ks = scipy.stats.kstest(z1, 'norm')
print("\n",ks)

##centralne twierdzenie graniczne
##test metoda montecarlo
##wykresy
##rezultat: tabela ktora porownuje rezultaty w zaleznosci od wybranego testu i zmiennych

def sampling2pmf(n, dist, m=10000):
  """
  n: sample size for each experiment
  m: how many times do you do experiment, fix in 10000
  dist: frozen distribution
  """
  ber_dist = dist
  sum_of_samples = []
  for i in range(m):
    samples = ber_dist.rvs(size=n)
    sum_of_samples.append(np.sum(samples))
  val, cnt = np.unique(sum_of_samples, return_counts=True)
  pmf = cnt / len(sum_of_samples)
  return val, pmf

sampling2pmf()

