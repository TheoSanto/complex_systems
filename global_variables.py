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

# Instance of Global Variables, Constants and Controls
global nsteps
global interval
global dimension
global side
global ambient
global ambient_evolution
global nempties
global nred
global nblue 
global setup
global npeople
global distance
global G
global T 
global vision
global ax
global ax_histo

# Animation Settings
nsteps = 100
interval = 60 #ms

# Ambient Variables
dimension = 961 
side = int(np.sqrt(dimension)) # 31
ambient = [[-3,-3]]*dimension
ambient_evolution = [ambient]*(nsteps)

# Scenario Choice
setup = 0
# 0 per Scenario di Distanza, 
# 1 per Scenario di Flocking Gravitazionale,
# 2 per Scenario di Visione Parziale. 

# ONLY FOR setup==0
fixed_or_random = 0
# 0 if Inizialization of the Ambient is Random
# 1 if Inizialization of the Ambient is Pre-fixed

# forse può essere interessante estendere questo tipo di analisi per i vari scenari
time_analysis = 1
# 0 if Representation of Time Distribution is not wanted
# 1 if Representation of Time Distribution is wanted

# Control Parameters
npeople = 50
distance = 3  # MAX = int((side-1)/2)
G = 10
T = 1
vision = 2
initial_blues = 30

# Tests of Initialization's Consistence
assert nsteps >= 0, 'ATTENTION: Negative n° of Time Steps.'
assert interval > 0, 'ATTENTION: Negative Time Interval for Animation.'
assert (side-np.sqrt(dimension)) == 0, 'ATTENTION: The Root of dimension is not Integer, as it should be.'
assert (setup==0) or (setup==1) or (setup==2), 'ATTENTION: setup Value is not acceptable.'
assert (fixed_or_random==0) or (fixed_or_random==1), 'ATTENTION: fixed_or_random Value is not acceptable.' 
if setup!=0 :
   assert fixed_or_random == 0, 'ATTENTION: Wrong Scenario for non-vanishing fixed_or_random.'
assert (npeople>0) and (npeople<dimension), 'ATTENTION: Negative or too elevated npeople Value.' 
assert (distance>0) and (distance<=int((side-1)/2)), 'ATTENTION: Negative or too elevated distance Value.'
assert G > 0, 'ATTENTION: Negative Universal Gravitational Constant G.'
assert T > 0, 'ATTENTION: Negative Temperature T.'
assert (vision>0) and (vision<npeople), 'ATTENTION: Negative or too elevated vision Value.'

'''
MODELLO DI ISING: here 'https://it.abcdef.wiki/wiki/Ising_model'

OBIETTIVI
1) Dobbiamo controllare il comportamento del sistema al variare del parametro del controllo DISTANCE
ossia vedere se si raggiunge o meno il consenso a parità di densità popolativa media(=npeople/dimension)

2) Una volta fatto ciò, possiamo introdurre un nuvo parametro di controllo, ossia il numero costante e limitato di amici,
da cui l'individuo viene influenzato ad ogni istante temporale

3) Provare ad implementare una memoria del sistema (mi sembra infattibile e molto impegnativo computazionalmente)

4) Provare ad implementare l'attrazione simil-gravitazionale tra individui con opinione concorde
   (la vedo già più fattibile, ci si può lavorare)

5) Inserire un campo esterno rappresentativo dei media (come già fatto, ma magari implementare due casi:
   uno dove le variazioni casuali dei media sono pseudo-continue, ossia piccole entro una certa tolleranza 
   scelta dall'utente, ed un'altro dove ad un certo istante il campo esterno subisce una o più variazione 
   improvvisa e significativa, per vedere se il sistema riesce a trovare un equilibrio comunque o meno)


DUBBI
1) Gli individui ai bordi sono influenzati anche dagli indidui dall'altra parte dell'ambiente??

2) Come implementare le probabilità di transizione tra le possibili opinioni (-2,-1,0,1,2) ??

3) In qualche modo forse il parametro di distanza è correlato alle fluttuazioni del sistema 
   che in teoria sono rappresentate fisicamente dal parametro di temperatura. Infatti, m aspetto 
   che maggiore è la distanza, maggiore è la temperature; ma allo stesso tempo anche che 
   minore è il numero limitato di amici che influenzano l individuo, minore è la temperatura.
   Ha senso??

4) Non so quanto senso abbia implementare tutte queste cose contemporaneamente. Proporrei di fare 
   una cosa alla volta tenendo le altre 'fissate', nel senso che:
   ad esempio, quando si intende studiare il comportamento del sistema per diversi valori di distanza,
   direi di annullare sia l'effetto del campo esterno dei media che dell'attrazione semi-gravitazionale
   e poi per andare a svolgere gli obiettivi successivi si può scegliere un valore fisso di distanza 
   per cui sappiamo sia possibile il raggiungimento del consenso
'''
