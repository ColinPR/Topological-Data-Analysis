import numpy as np

def model(y, t, L, sources):
    if np.sin(t) > 0:
        return - L * y + sources
    else:
        return -L * y
