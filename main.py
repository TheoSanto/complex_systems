import functions as f
import global_variables as glob

start_all = glob.time.time()
#glob.np.random.seed(196808819)

# Random Positioning & Opinion Defining of the Individuals
if glob.fixed_init==False :
    glob.ambient_evolution[0] = f.init_random()
if glob.fixed_init==True :
    glob.ambient_evolution[0] = f.init_fixed()

# CSV Files for Magnetization & Decision Time Data Storage

# Implementation and Storage of Time Evolution of 1° Scenario
if glob.setup==0 :
    
    for t in range(glob.nsteps) : 
        print("Step", t, ', Mode',glob.setup)
        if t>0 :
            glob.ambient_evolution[t] = f.evolve_norm(glob.ambient_evolution[t-1])
            print(f.count_all(glob.ambient_evolution[t]))
            if glob.balancing==True :
                balance = f.stop_if_eq(glob.ambient_evolution[t], t) #sono in equilibrio?
                if balance!=False : 
                    print("Equilibrio raggiunto: ", balance)
                    glob.nsteps = t
                    break

    # Magnetization Analysis
    if glob.magnetization_analysis==True :
        magnetization_data = []
        for t in range(glob.nsteps) :
            spin_data_t = f.count_all(glob.ambient_evolution[t])
            magnetization_data.append((1/glob.npeople)*(spin_data_t[1]-spin_data_t[0]))
        times = glob.np.linspace(0,glob.nsteps,glob.nsteps)
        glob.plt.title('Magnetization\'s Time Evolution')
        glob.plt.plot(times, magnetization_data, marker='.',linestyle='--')
        glob.plt.ylabel('Magnetization')
        glob.plt.xlabel('Time Step')
        glob.plt.show()
        
        magnetization_data_file = 'magn_data_n100_d1.csv'
        with open(magnetization_data_file, 'w') as magn_fout :
            f.magnetization_data_storage(magnetization_data, magn_fout)
    
    # Decision Time Distribution Analysis
    if glob.time_analysis==True :
        decision_time_data = f.decision_time_data(glob.ambient_evolution)
        fig1 = glob.plt.figure()
        ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
        times_counts, bins = glob.np.histogram(decision_time_data,bins=glob.np.linspace(0,glob.nsteps,glob.nsteps))
        glob.plt.title('Decision Time Occurrences')
        glob.plt.plot(glob.np.linspace(1,glob.nsteps,glob.nsteps-1),times_counts,marker='.',linewidth=0)
        glob.plt.ylabel('Occurrences')
        glob.plt.xlabel('Time Steps')
        glob.plt.yscale('log')
        glob.plt.xscale('log')
        glob.plt.show()

        decision_time_data_file = 'time_data_n100_d1.csv'
        with open(decision_time_data_file, 'w') as time_fout :
            f.decision_time_data_storage(times_counts, time_fout)

    # Initial Conditions Influence Analysis
    if glob.init_analysis==True :
        norm_file = 'init_data_sim500_d4_random.txt'
        with open(norm_file, 'a') as n_fout :
            n_fout.write(f'{balance}\n')


# Implementation and Storage of Time Evolution of 2° Scenario
if glob.setup==1 :

    #third_stationary_duration = 0
    for t in range(glob.nsteps) : 
        print("Step", t, ', Mode',glob.setup)
        if t>0 :
            glob.ambient_evolution[t] = f.evolve_grav(glob.ambient_evolution[t-1])
            print(f.count_all(glob.ambient_evolution[t]))
            if glob.balancing==True :
                #if f.count_all(glob.ambient_evolution[t])==f.count_all(glob.ambient_evolution[t-1]) :
                #    third_stationary_duration += 1
                #else : 
                #    third_stationary_duration = 0
                balance = f.stop_if_eq(glob.ambient_evolution[t], t) #sono in equilibrio?
                if balance!=False : #or third_stationary_duration==100 : 
                    print("Equilibrio raggiunto: ", balance)
                    glob.nsteps = t
                    break

    # Magnetization Analysis
    if glob.magnetization_analysis==True :
        magnetization_data = [] 
        for t in range(glob.nsteps) :
            spin_data_t = f.count_all(glob.ambient_evolution[t]) #proportion of opinions
            m = (1/glob.npeople)*(spin_data_t[1]-spin_data_t[0]) #magnetizzazione al tempo t generico
            magnetization_data.append(m)

        times = glob.np.linspace(0,glob.nsteps,glob.nsteps)
        glob.plt.title('Gravitational magnetization\'s Time Evolution')
        glob.plt.plot(times, magnetization_data, marker='.',linestyle='--')
        glob.plt.ylabel('Magnetization')
        glob.plt.xlabel('Time Step')
        glob.plt.show()

        flocking = 'flocking.csv'
        with open(flocking, 'w') as flock_fout :
            f.magnetization_data_storage(magnetization_data, flock_fout)

    # Decision Time Distribution Analysis
    if glob.time_analysis==True :
        decision_time_data = f.decision_time_data(glob.ambient_evolution)
        fig1 = glob.plt.figure()
        ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
        times_counts, bins = glob.np.histogram(decision_time_data,bins=glob.np.linspace(0,glob.nsteps,glob.nsteps))
        glob.plt.title('Gravitational decision Time Occurrences')
        glob.plt.plot(glob.np.linspace(1,glob.nsteps,glob.nsteps-1),times_counts,marker='.',linewidth=0)
        glob.plt.ylabel('Occurrences')
        glob.plt.xlabel('Time Steps')
        glob.plt.yscale('log')
        glob.plt.xscale('log')
        glob.plt.show()

        #csv file tau
        '''problema'''
        decision_time_data_file = 'grav_time_data.csv'
        with open(decision_time_data_file, 'w') as gtime_fout :
            f.decision_time_data_storage(times_counts, gtime_fout)

    # Initial Conditions Influence Analysis
    if glob.init_analysis==True :
        grav_file = "grav_prob.txt"
        with open(grav_file, 'a') as g_fout :
            g_fout.write(f'{balance}\n')
        
        

''''''''''''''''''''''''''''''''''''''''''''''''




# Implementation and Storage of Time Evolution of 3° Scenario
if glob.setup==2 :

    for t in range(glob.nsteps) : 
        print("Step", t, ', Mode',glob.setup)
        if t>0 :
            glob.ambient_evolution[t] = f.evolve_vis(glob.ambient_evolution[t-1])
            if glob.balancing==True :
                balance = f.stop_if_eq(glob.ambient_evolution[t], t) #sono in equilibrio?
                if balance!=False : 
                    print("Equilibrio raggiunto: ", balance)
                    glob.nsteps = t
                    break
    
    # Magnetization Analysis 
    if glob.magnetization_analysis==True :
        magnetization_data = [] 
        for t in range(glob.nsteps) :
            spin_data_t = f.count_all(glob.ambient_evolution[t]) #proportion of opinions
            m = (1/glob.npeople)*(spin_data_t[1]-spin_data_t[0]) #magnetizzazione al tempo t generico
            magnetization_data.append(m)

        times = glob.np.linspace(0,glob.nsteps,glob.nsteps)
        glob.plt.title('Partial magnetization\'s Time Evolution')
        glob.plt.plot(times, magnetization_data, marker='.',linestyle='--')
        glob.plt.ylabel('Magnetization')
        glob.plt.xlabel('Time Step')
        glob.plt.show()

        #csv file magnetization
        partial_v= 'partial_vision_magnetization.csv'
        with open(partial_v, 'w') as partial_fout :
            f.magnetization_data_storage(magnetization_data, partial_fout)

    # Decision Time Distribution Analysis
    if glob.time_analysis==True :
        decision_time_data = f.decision_time_data(glob.ambient_evolution)
        fig1 = glob.plt.figure()
        ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
        times_counts, bins = glob.np.histogram(decision_time_data,bins=glob.np.linspace(0,glob.nsteps,glob.nsteps))
        glob.plt.title('Partial decision Time Occurrences')
        glob.plt.plot(glob.np.linspace(1,glob.nsteps,glob.nsteps-1),times_counts,marker='.',linewidth=0)
        glob.plt.ylabel('Occurrences')
        glob.plt.xlabel('Time Steps')
        glob.plt.yscale('log')
        glob.plt.xscale('log')
        glob.plt.show()

        #csv file tau
        decision_time_data_file = 'partial_time_data.csv'
        with open(decision_time_data_file, 'w') as ptime_fout :
            f.decision_time_data_storage(times_counts, ptime_fout)

    # Initial Conditions Influence Analysis
    if glob.init_analysis==True :
        vis_file = 'vis_prob_file.txt'
        with open(vis_file, 'a') as v_fout :
            v_fout.write(f'{balance}\n')


#bench
end_all = glob.time.time()
print('all time:',end_all-start_all)

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
