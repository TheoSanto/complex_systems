from multiprocessing.connection import wait
from pickle import TRUE
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np
from numpy.random.mtrand import rand
from matplotlib import cm
from matplotlib import animation
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib.pyplot import figure
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import time
import unittest


# Instance of Global Axes for Visualization ##################################
global ax
global ax_histo


# Animation Settings #########################################################
nsteps = 300
interval = 60 #ms


# Ambient Variables ##########################################################
dimension = 961 
side = int(np.sqrt(dimension)) # 31
ambient = [[-3,-3]]*dimension
ambient_evolution = [ambient]*(nsteps)


# Scenario Choice ############################################################
setup = 2
# 0 per Scenario di Distanza, 
# 1 per Scenario di Flocking Gravitazionale,
# 2 per Scenario di Visione Parziale. 


# Global Analysis Selectors ##################################################
fixed_init = False
# False if Inizialization of the Ambient is Random
# True if Inizialization of the Ambient is Pre-fixed

magnetization_analysis = True
# False if Representation of Magnetization Time Evolution is not wanted
# True if Representation of Magnetization Time Evolution is wanted

time_analysis = True
# False if Representation of Time Distribution is not wanted
# True if Representation of Time Distribution is wanted

init_analysis = False
# False if Initial Conditions Analysis is not wanted
# True if Initial Conditions Analysis is wanted

balancing = False
# False if Stationary Condition Analysis is not wanted
# True if Stationary Condition Analysis is wanted (recommended)


# Control Parameters #######################################################
npeople = 100
distance = 4
G = 10
T = 1
vision = 8
initial_reds = 50


# Tests of Initialization's Consistence ####################################
assert nsteps >= 0, 'ATTENTION: Negative n° of Time Steps.'
assert interval > 0, 'ATTENTION: Negative Time Interval for Animation.'
assert (side-np.sqrt(dimension)) == 0, 'ATTENTION: The Root of dimension is not Integer, as it should be.'
assert (setup==0) or (setup==1) or (setup==2), 'ATTENTION: setup Value is not acceptable.' 
assert (npeople>0) and (npeople<dimension), 'ATTENTION: Negative or too elevated npeople Value.' 
assert (distance>0) and (distance<=int((side-1)/2)), 'ATTENTION: Negative or too elevated distance Value.'
assert G > 0, 'ATTENTION: Negative Universal Gravitational Constant G.'
assert T > 0, 'ATTENTION: Negative Temperature T.'
assert (vision>0) and (vision<npeople), 'ATTENTION: Negative or too elevated vision Value.'
