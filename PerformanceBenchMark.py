import timeit
from math import *
import numpy as np
import numexpr as ne
loops = 25000000


a = range(1, loops)

def f(x):
    return 3 * log(x) + cos(x) ** 2

start_time = timeit.default_timer()
r = [f(x) for x in a]
elapsed = timeit.default_timer() - start_time
print elapsed

# use numpy operates directly on ndarray
def f_numpy(a):
    start_time = timeit.default_timer()
    R= 3 * np.log(a) + np.cos(a) ** 2
    elapsed = timeit.default_timer() - start_time
    print elapsed

# use numerical expressions,
# which compiles the expression to improve upon the performance of general numpy functionality
# avoid in-memory copies of arrays along the way
def f_numexpr(a):
    ne.set_num_threads(1)
    f = '3 * log(a) + cos(a) ** 2'


a = np.arange(1, loops)

r = f_numpy(a)

