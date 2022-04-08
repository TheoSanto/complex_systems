import functions as f
import global_variables as glob

glob.np.random.seed(196808822)

# Random Positioning & Opinion Defining of the Individuals
if glob.fixed_or_random==0 :
    print('yes')
    glob.ambient_evolution[0] = f.init_random()
if glob.fixed_or_random==1 :
    print('no')
    glob.ambient_evolution[0] = f.init_fixed()

# Implementation and Storage of Time Evolution of 1° Scenario
if glob.setup==0 :
    for t in range(0, glob.nsteps) : 
                print("Step", t, ', Mode',glob.setup)
                if t>0 :
                    glob.ambient_evolution[t] = f.evolve_norm(glob.ambient_evolution[t-1])
    time_data = f.time_distribution(glob.ambient_evolution)
    fig1 = glob.plt.figure()
    ax1 = fig1.add_axes([0.1, 0.1, 0.5, 0.75])
    ax1.hist(time_data)
    glob.plt.show()

# Implementation and Storage of Time Evolution of 2° Scenario
if glob.setup==1 :
    for t in range(0, glob.nsteps) : 
                print("Step", t, ', Mode',glob.setup)
                if t>0 :
                    glob.ambient_evolution[t] = f.evolve_grav(glob.ambient_evolution[t-1])

# Implementation and Storage of Time Evolution of 3° Scenario
if glob.setup==2 :
    for t in range(0, glob.nsteps) : 
                print("Step", t, ', Mode',glob.setup)
                if t>0 :
                    glob.ambient_evolution[t] = f.evolve_vis(glob.ambient_evolution[t-1])

## Fulfilling of the CSV File for Initial State of the System 
#data_in = 'data_in.csv'
#with open(data_in, 'w') as fout1 :
#    fout1.write('Class, Opinion, Position, Time_Step\n')
#    for i in range(glob.dimension) :
#        f.data_extr(glob.ambient_evolution[0], i, fout1, 0)
#
## Fulfilling of the CSV File for Final State of the System 
#data_fin = 'data_fin.csv'
#with open(data_fin, 'w') as fout2 :
#    fout2.write('Class, ID, Opinion, Position, Time_Step\n')
#    for i in range(glob.dimension) :
#        f.data_extr(glob.ambient_evolution[glob.nsteps-1], i, fout2, glob.nsteps-1)

# Implementaion of Cellular Automata Visualization and Animation
fig = glob.plt.figure()
glob.ax = fig.add_axes([0.1, 0.1, 0.5, 0.75])
glob.ax_histo = fig.add_axes([0.65, 0.1, 0.3, 0.4])
anim = glob.animation.FuncAnimation(fig, f.update_scatter, frames=glob.nsteps, interval=glob.interval)
anim.save('simulation_try.gif')
#glob.plt.show() 
