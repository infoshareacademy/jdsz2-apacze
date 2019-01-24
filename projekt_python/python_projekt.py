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


# Part 1

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


def clt_transform(x_size, out_count):
    """
    Box Muller transformation function
    :param x_size: int (N)
    :param out_count: int (count of generated output numbers)
    :return: transformed list of values
    """

    try:
        output_clt = []
        for k in range(out_count):
            trans_x = np.random.uniform(-1, 1, size=x_size)
            trans_value = np.mean(trans_x - np.mean(trans_x)) / (np.std(trans_x) / np.sqrt(x_size))
            output_clt.append(trans_value)
    except (TypeError, AttributeError, ZeroDivisionError) as msg:
        logging.warning(msg='Error {0}, \nexiting program'.format(msg))
        exit(0)

    return output_clt


# Generate numbers with Box Muller transformation
# uniformly distributed values between 0 and 1
u_1 = random.rand(4000)
u_2 = random.rand(4000)
bm_1, bm2 = box_muller_transform(u_1, u_2)

# Generate numbers with Central Limit Theorem transformation
clt_1 = clt_transform(30, 1000)


# Part 2

plt.hist(bm_1)
plt.hist(bm_2)
plt.show()

plt.hist(clt_1)
plt.show()


# Part 3

# Shapiro - Wilk test
szapiro = scipy.stats.shapiro(z1)
print("\nShapiro-Wilk\n", szapiro)

# Kołmogorov - Smirnov test
ks = scipy.stats.kstest(z1, 'norm')
print("\n", ks)

