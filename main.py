import functions as f
import global_variables as glob

glob.np.random.seed(196808822)

# Random Positioning & Opinion Defining of the Individuals
if glob.fixed_or_random==0 :
    glob.ambient_evolution[0] = f.init_random()
if glob.fixed_or_random==1 :
    glob.ambient_evolution[0] = f.init_fixed()

# Implementation and Storage of Time Evolution of 1° Scenario
if glob.setup==0 :
    # lista di array 2D per lo storage degli effetti prodotti da condizioni iniziali diverse
    initial_conditions = []
    final_conditions = []
    for n in range(glob.nsimulations) :
        print("Simulation n°", n)

        if glob.fixed_or_random==0 :
            glob.ambient_evolution[0] = f.init_random()
        if glob.fixed_or_random==1 :
            glob.ambient_evolution[0] = f.init_fixed()
        # utile per Magnetization Analysis
        #magnetization_data = []
        #spin_data_0 = f.count_all(glob.ambient_evolution[0])
        #magnetization_data.append((1/glob.npeople)*(spin_data_0[1]-spin_data_0[0]))

        for t in range(0, glob.nsteps) : 
                    #print("Step", t, ', Mode',glob.setup)
                    if t>0 :
                        glob.ambient_evolution[t] = f.evolve_norm(glob.ambient_evolution[t-1])

                        #spin_data_t = f.count_all(glob.ambient_evolution[t])
                        #magnetization_data.append((1/glob.npeople)*(spin_data_t[1]-spin_data_t[0]))

        #times = glob.np.linspace(0,glob.nsteps,glob.nsteps)
        #glob.plt.plot(times,magnetization_data)
        #glob.plt.show()

        # utile per Time Distribution Analysis
        time_data = f.time_distribution(glob.ambient_evolution)
        fig1 = glob.plt.figure()
        ax1 = fig1.add_axes([0.1, 0.1, 0.5, 0.75])
        ax1.hist(time_data,bins=int(glob.nsteps))
        glob.plt.yscale('log')
        glob.plt.xscale('log')
        glob.plt.show()
        print('\n\n')

        # utile per Initial Conditions Analysis
        #nth_opinion_data_in = f.count_all(glob.ambient_evolution[0])
        #nth_opinion_data_fin = f.count_all(glob.ambient_evolution[glob.nsteps-1])
        #initial_conditions.append(nth_opinion_data_in)
        #final_conditions.append(nth_opinion_data_fin)
    #prob_blue = (final_conditions.count([0, glob.npeople]))/(glob.nsimulations)
    #prob_red = (final_conditions.count([glob.npeople, 0]))/(glob.nsimulations)
    #assert (len(initial_conditions)==glob.nsimulations) and (len(final_conditions)==glob.nsimulations), 'ATTENTION: Something wrong about the Storage of Simulations\' initial and final conditions.'
    #print(initial_conditions,'\n\n',final_conditions)
    #print(prob_blue, 'of Blue &', prob_red, 'of Red.')

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
glob.ax_histo = fig.add_axes([0.7, 0.1, 0.23, 0.4])
anim = glob.animation.FuncAnimation(fig, f.update_scatter, frames=glob.nsteps, interval=glob.interval)
anim.save('simulation_try.gif')
#glob.plt.show() 
