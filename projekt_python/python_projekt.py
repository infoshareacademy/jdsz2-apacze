"""
http://home.agh.edu.pl/~chwiej/mn/generatory_2015.pdf
http://www.if.pw.edu.pl/~agatka/numeryczne/wyklad_12.pdf

1. Wygenerowaæ liczby za pomoc¹ "Generatora liczb z rozk³adu normalnego" dwoma metodami
- Metod¹ Boxa-Mullera (funkcja)
- Metod¹ Centralnego twierdzenia granicznego(funkcja)

2. Przetestowaæ czy generetory, generuj¹ w taki sam sposób jak wbudowany w Pythona generator liczb z rozk³adu normalnego

3. Wykonaæ testy statystyczne:
- Test Shapiro-Wilka
- Test Kolmogorov–Smirnov
- Test Monte Carlo
"""

import logging
import pandas as pd
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from numpy import random, sqrt, log, sin, cos, pi

logging.basicConfig()


def box_muller_transform(inp_u1, inp_u2):
    """
    Box Muller transformation function
    :param inp_u1: numpy.ndarray  or numeric
    :param inp_u2: numpy.ndarray or numeric
    :return: transformed numpy.ndarray or numeric
    """

    try:
        out_z1 = sqrt(-2 * log(inp_u1)) * cos(2 * pi * inp_u2)
        out_z2 = sqrt(-2 * log(inp_u1)) * sin(2 * pi * inp_u2)
    except (TypeError, AttributeError) as msg:
        logging.warning(msg='Error {0}, \nexiting program'.format(msg))
        exit(0)

    return out_z1, out_z2







# uniformly distributed values between 0 and 1
u1 = random.rand(4000)
u2 = random.rand(4000)

# run the transformation
z1,z2 = box_muller_transform(u1,u2)

#print(z1,z2)
#plt.hist(z1)
#plt.hist(z2)

###Generator Python
mu, sigma = 0, 0.1
g1 = random.normal(mu, sigma, 4000)
#plt.hist(g1)
#plt.show()

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


###CLT

x = random.uniform(-1,1,50)
print(x)
x_mean = np.mean(x)
x_var = np.var(x)
x_std = np.std(x)
print("wariancja {} średnia {} odchylenie standardowe {}".format(x_var, x_mean, x_std))

n=50

for i in range(n):
  y_clt = np.mean((x[:i]-(x_mean*i)))/(x_std/np.sqrt(n))

plt.hist(y_clt)
plt.show()