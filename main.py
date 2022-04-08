import functions as f
import global_variables as glob

#glob.np.random.seed(19680822)

red = -2
orange = -1
gray = 0
cyan = +1
blue = +2

# Random Positioning & Opinion Defining of the Individuals
j = 0
for i in range(glob.dimension) :
    rand_pos = glob.np.random.randint(0, glob.dimension-1) 
    rand_extr = glob.np.random.randint(-2,3)
    if glob.ambient[rand_pos]==-3 :
        glob.ambient[rand_pos] = rand_extr
        j += 1
        if rand_extr==-2 :
            glob.nred += 1
        if rand_extr==-1 :
            glob.norange += 1
        if rand_extr==0 : 
            glob.nwhite += 1
        if rand_extr==1 :
            glob.ncyan += 1
        if rand_extr==2 :
            glob.nblue += 1
    if j==glob.npeople : 
        nempties = glob.dimension-glob.npeople
        break

# Fullfilling of the Position Arrays for each Color
xdata_empties = []
ydata_empties = []
xdata_red = []
ydata_red = []
xdata_orange = []
ydata_orange = []
xdata_white = []
ydata_white = []
xdata_cyan = []
ydata_cyan = []
xdata_blue = []
ydata_blue = []
xdata = []
ydata = []
colorsdata = []

for i in range(glob.dimension) :
    ydata = int((i/glob.side)+1)
    xdata = int(i+1-(ydata-1)*glob.side)
    if glob.ambient[i]==-3 :
        xdata_empties.append(xdata)
        ydata_empties.append(ydata)
    if glob.ambient[i]!=-3 :
        colorsdata.append(glob.ambient[i])
        if glob.ambient[i]==-2 :
            xdata_red.append(xdata)
            ydata_red.append(ydata)
        if glob.ambient[i]==-1 :
            xdata_orange.append(xdata)
            ydata_orange.append(ydata)
        if glob.ambient[i]==0 :
            xdata_white.append(xdata)
            ydata_white.append(ydata)
        if glob.ambient[i]==1 :
            xdata_cyan.append(xdata)
            ydata_cyan.append(ydata)
        if glob.ambient[i]==2 :
            xdata_blue.append(xdata)
            ydata_blue.append(ydata)

# Definition of the Matrix of Friends' Links
#friends_matrix = c.choose_friends()
#print(friends_matrix)

# Implementation and Storage of Time Evolution of 1° Scenario
if glob.setup==0 :
    for t in range(0, glob.nsteps) : 
                print("Step", t, ', Mode',glob.setup)
                #if t == 0 :
                #    print("------------------")
                #    print("RED", "time: ", t)
                #    c.local_density(red, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("ORANGE", "time: ", t)
                #    c.local_density(orange, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("GRAY", "time: ", t)
                #    c.local_density(gray, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("CYAN", "time: ", t)
                #    c.local_density(cyan, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("BLUE", "time: ", t)
                #    c.local_density(blue, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                if t>0 :
                    glob.ambient_evolution[t] = f.evolve_norm(glob.ambient_evolution[t-1])
                    #print("------------------")
                    #print("RED", "time: ", t)
                    #c.local_density(red, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("ORANGE", "time: ", t)
                    #c.local_density(orange, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("GRAY", "time: ", t)
                    #c.local_density(gray, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("CYAN", "time: ", t)
                    #c.local_density(cyan, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("BLUE", "time: ", t)
                    #c.local_density(blue, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")

# Implementation and Storage of Time Evolution of 2° Scenario
if glob.setup==1 :
    for t in range(0, glob.nsteps) : 
                print("Step", t, ', Mode',glob.setup)
                #if t == 0 :
                #    print("------------------")
                #    print("RED", "time: ", t)
                #    c.local_density(red, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("ORANGE", "time: ", t)
                #    c.local_density(orange, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("GRAY", "time: ", t)
                #    c.local_density(gray, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("CYAN", "time: ", t)
                #    c.local_density(cyan, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("BLUE", "time: ", t)
                #    c.local_density(blue, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                if t>0 :
                    glob.ambient_evolution[t] = f.evolve_grav(glob.ambient_evolution[t-1])
                    #print("------------------")
                    #print("RED", "time: ", t)
                    #c.local_density(red, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("ORANGE", "time: ", t)
                    #c.local_density(orange, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("GRAY", "time: ", t)
                    #c.local_density(gray, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("CYAN", "time: ", t)
                    #c.local_density(cyan, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("BLUE", "time: ", t)
                    #c.local_density(blue, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")

# Implementation and Storage of Time Evolution of 3° Scenario
if glob.setup==2 :
    for t in range(0, glob.nsteps) : 
                print("Step", t, ', Mode',glob.setup)
                #if t == 0 :
                #    print("------------------")
                #    print("RED", "time: ", t)
                #    c.local_density(red, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("ORANGE", "time: ", t)
                #    c.local_density(orange, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("GRAY", "time: ", t)
                #    c.local_density(gray, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("CYAN", "time: ", t)
                #    c.local_density(cyan, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                #    print("BLUE", "time: ", t)
                #    c.local_density(blue, glob.ambient_evolution[t], glob.distance)
                #    print("------------------")
                if t>0 :
                    glob.ambient_evolution[t] = f.evolve_vis(glob.ambient_evolution[t-1])
                    #print("------------------")
                    #print("RED", "time: ", t)
                    #c.local_density(red, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("ORANGE", "time: ", t)
                    #c.local_density(orange, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("GRAY", "time: ", t)
                    #c.local_density(gray, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("CYAN", "time: ", t)
                    #c.local_density(cyan, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")
                    #print("BLUE", "time: ", t)
                    #c.local_density(blue, glob.ambient_evolution[t], glob.distance)
                    #print("------------------")

#print(c.local_density(orange, glob.ambient_evolution[0], glob.distance))
#print(c.gravity(92 , glob.ambient_evolution[0])) #per provare, funzia
#print(c.partial_vision(24, glob.ambient_evolution[0]))

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
#
## Fulfilling of the CSV File for Friends' Links
#friend_data = 'friend.csv'
#with open(friend_data, 'w') as fout3 :
#    fout3.write('nth_people, friend_list\n')
#    for i in range(glob.npeople) :
#            f.friend_extr(friends_matrix, i, fout3)

# Implementaion of Cellular Automata Visualization and Animation
fig = glob.plt.figure()
glob.ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
anim = glob.animation.FuncAnimation(fig, f.update_scatter, frames=glob.nsteps, interval=glob.interval)
anim.save('simulation2.gif')
#glob.plt.show() 

#START: 23.49  STOP: 23.59  (30 people) simulation1
#START: 00.32  STOP: 01.12  (60 people) simulation2
