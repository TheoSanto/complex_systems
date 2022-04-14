import global_variables as glob

def count_all(ambient) :
    nred = 0
    for i in range(glob.dimension) :
        if ambient[i][1]==-1 :
            nred += 1
    return [nred, glob.npeople-nred]

def init_random() :
    ambient = [[-3,-3]]*glob.dimension
    j = 0
    while j<glob.npeople :
        rand_pos = glob.np.random.randint(0, glob.dimension-1) 
        rand_extr = 0
        if j<glob.initial_reds : rand_extr = -1
        else : rand_extr = 1
    
        if ambient[rand_pos]==[-3,-3] :
            ambient[rand_pos] = [j, rand_extr]
            j += 1
    
    assert j == glob.npeople, 'ATTENTION: The Inizialization of the Ambient has not been finished.'
    return ambient

def init_fixed() :
    ambient = [[-3,-3]]*glob.dimension
    j = 0
    while j<glob.npeople :
        rand_pos = glob.np.random.randint(0, glob.dimension-1) 
        if ambient[rand_pos]==[-3,-3] :
            ambient[rand_pos] = [-3, 1]
            j += 1

    j = 0
    for k in range(glob.dimension) :
        if ambient[k]==[-3,1] and j<glob.initial_reds :
            ambient[k] = [j,-1]
            j += 1
        if ambient[k]==[-3,1] and j>=glob.initial_reds :
            ambient[k] = [j,1]
            j += 1
    
    assert j == glob.npeople, 'ATTENTION: The Inizialization of the Ambient has not been finished.'
    return ambient

def decision_time_data(evolution) :
    assert len(evolution) == glob.nsteps, 'ATTENTION: decision_time_data() needs a (nsteps)-dim. array as argument.'

    time_distribution = []
    for j in range(glob.npeople) :

        jth_times = 0
        for t in range(1, glob.nsteps) :
            jth_position_t = ID_position(evolution[t],j)
            jth_opinion_t = evolution[t][jth_position_t][1]
            if jth_opinion_t!=evolution[t-1][ID_position(evolution[t-1],j)][1] :
                if jth_times==0 :
                    time_distribution.append(t)
                if jth_times>0 :
                    time_distribution.append(t-time_distribution[-1])
                jth_times += 1
            if jth_opinion_t==evolution[0][ID_position(evolution[0],j)][1] and t==glob.nsteps-1 :
                time_distribution.append(t)
                break
    
    return time_distribution

def ID_position(ambient, ID) :
    assert len(ambient) == glob.dimension, 'ATTENTION: ID_position() needs a (dimension)-dim. array as first argument.'
    assert (ID!=-3) and (ID>=0) and (ID<glob.npeople), 'ATTENTION: ID_position() second argument must be integer and different from -3.'

    for i in range(glob.dimension) :
        if ambient[i][0]==ID :
            return i

# THIS IS OK ########################################################
# Function that returns x & y Coordinates of a Single Individual
# given its Index in the Ambient Array.
def xydata(which) :
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: xydata() needs a non-negative integer as argument, lower than dimension.'

    # Discovering of Y Position of which
    ywhich = 0
    for y in range(1, glob.side+1) :
        if which<y*glob.side :
            ywhich = y
            break

    # Discovering of X Position of which
    xwhich = 0
    for x in range(1, glob.side+1) :
        if which<=(ywhich-1)*glob.side+x-1 :
            xwhich = x
            break

    return xwhich, ywhich

# THIS IS OK ########################################################
# Function that defines the Chebyshev Distance in this 2D Discrete Space
# taking into account the Periodic Conditions.
def table_distance(first, second) :
    assert (first>=0) and (first<glob.dimension), 'ATTENTION: table_distance() needs a non-negative integer as first argument, lower than dimension.'
    assert (second>=0) and (second<glob.dimension), 'ATTENTION: table_distance() needs a non-negative integer as second argument, lower than dimension.'

    # Coordinates x & y of first
    xfirst, yfirst = xydata(first) 

    # Coordinates x & y of second
    xsecond, ysecond = xydata(second)

    # Arrays filled with all possible pairs of Coordinates x & y of second due to Periodic Conditions
    second_xs = [-3]*3
    second_ys = [-3]*3
    for i in range(3) :
        second_xs[i] = xsecond+(i-1)*glob.side+1
        second_ys[i] = ysecond+(i-1)*glob.side+1
    
    # Array filled with all possible Distances between first and second
    possible_distances = [-3]*9
    for j in range(3) :
        jth_xdistance = abs(second_xs[j]-xfirst-1)
        for k in range(3) :
            kth_ydistance = abs(second_ys[k]-yfirst-1)
            jkth_maxdistance = max(jth_xdistance,kth_ydistance)
            possible_distances[3*j+k] = jkth_maxdistance
    
    # Final Distance as the Minimum of those in previous Array
    distance = min(possible_distances)
    return distance

# THIS IS OK ########################################################
# Function that returns an Array of Integers, indicating the Position 
# of Empty Spaces in the Von Neumann Neighborhood of the Individual 
# at (which)-th Site in the Ambient with Periodic Conditions, 
# for both the Distance Control Model and the Partial Vision Model.
def empty_spaces(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: empty_spaces() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: empty_spaces() needs a non-negative integer as second argument, lower than dimension.'

    # Array filled with Indexes of Empty Spaces next to which
    empty_spaces = []
    how_many = 0

    # Left Burden Management
    if which%(glob.side)==0 :
        for j in [which-glob.side, which+glob.side-1, which+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]==[-3,-3] :
                    empty_spaces.append(j)
                    how_many += 1
    
    # Right Burden Management
    if (which+1)%(glob.side)==0 :
        for j in [which-glob.side, which-1, which-glob.side+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]==[-3,-3] :
                    empty_spaces.append(j)
                    how_many += 1
    
    # General Case & High-Low Burden Management
    if which%(glob.side)!=0 and (which+1)%(glob.side)!=0 :
        for j in [which-glob.side, which-1, which+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]==[-3,-3] :
                    empty_spaces.append(j)
                    how_many += 1

    return empty_spaces

# THIS IS OK ########################################################
# Function that returns an Array of Integers, indicating the Position 
# (0 if that particular Site is already occupied)
# of Empty Spaces in the Von Neumann Neighborhood of the Individual 
# at (which)-th Site in the Ambient with Periodic Conditions, 
# for the specific case of Gravitational Flocking Model.
def empty_spaces_grav(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: empty_spaces_grav() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: empty_spaces_grav() needs a non-negative integer as second argument, lower than dimension.'

    # Array filled with Indexes of Empty Spaces next to which
    spaces = []
    how_many = 0

    # Left Burden Management
    if which%(glob.side)==0 :
        for j in [which-glob.side, which+glob.side-1, which+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]!=[-3,-3] :
                    spaces.append(-3)
                if ambient[j]==[-3,-3] :
                    spaces.append(j)
                    how_many += 1
    
    # Right Burden Management
    if (which+1)%(glob.side)==0 :
        for j in [which-glob.side, which-1, which-glob.side+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]!=[-3,-3] :
                    spaces.append(-3)
                if ambient[j]==[-3,-3] :
                    spaces.append(j)
                    how_many += 1
    
    # General Case & High-Low Burden Management
    if which%(glob.side)!=0 and (which+1)%(glob.side)!=0 :
        for j in [which-glob.side, which-1, which+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]!=[-3,-3] :
                    spaces.append(-3)
                if ambient[j]==[-3,-3] :
                    spaces.append(j)
                    how_many += 1

    return spaces

# THIS IS OK ########################################################
# Function that returns an Array of Floats, indicating the Probability 
# of Transition towards the Directions specified in 'spaces'
# (0 if the particular Site in that Direction is already occupied)
# of the Individual at (which)-th Site in the Ambient with Periodic 
# Conditions, for the specific case of Gravitational Flocking Model.
def empty_probs_grav(ambient, spaces, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: empty_probs_grav() needs a (dimension)-dim. array as first argument.'
    assert len(spaces) == 5, 'ATTENTION: empty_probs_grav() needs a 5_dim. array as second argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: empty_probs_grav() needs a non-negative integer as third argument, lower than dimension.'

    # Array filled with Probabilities of Transition towards a specific Empty Space next to which
    probs = []
    how_many = 0

    #print('SPACES: ',spaces)
    for i in range(5) :
        if spaces[i]==-3 :
            probs.append(0)
        if spaces[i]!=-3 :
            probs.append(1)
    # correzione della predilezione degli individui di muoversi rispetto che a stare fermi
    if probs.count(0)<4 and probs[4]!=0 :
        probs[4] = 0 
    max_ = probs.count(1)
    prob_ref = 1/max_
    grav_attraction = gravity(ambient, which)
    grav_x2 = grav_attraction[0]*grav_attraction[0]
    grav_y2 = grav_attraction[1]*grav_attraction[1]
    grav_modulus2 = grav_x2+grav_y2 

    #print('GRAVITY: ',grav_attraction[0],';',grav_attraction[1])

    prob_up = 0   
    prob_down = 0
    prob_left = 0
    prob_right = 0

    #sotto,sinistra,destra,sopra,which
    if grav_attraction[0]==0 and grav_attraction[1]==0 :
        prob_up    = 0.25
        prob_down  = 0.25
        prob_left  = 0.25
        prob_right = 0.25
    if grav_attraction[0]>0 or (grav_attraction[0]==0 and grav_attraction[1]!=0) :
        prob_left  = 0.25*(1-(grav_x2/grav_modulus2))
        prob_right = 0.25*(1+(grav_x2/grav_modulus2))
    if grav_attraction[0]<0 : 
        prob_left  = 0.25*(1+(grav_x2/grav_modulus2))
        prob_right = 0.25*(1-(grav_x2/grav_modulus2))
    if grav_attraction[1]>0 or (grav_attraction[1]==0 and grav_attraction[0]!=0) :
        prob_up   = 0.25*(1+(grav_y2/grav_modulus2))
        prob_down = 0.25*(1-(grav_y2/grav_modulus2)) 
    if grav_attraction[1]<0 :
        prob_up   = 0.25*(1-(grav_y2/grav_modulus2))   
        prob_down = 0.25*(1+(grav_y2/grav_modulus2))
    rescaled_probs = [prob_down, prob_left, prob_right, prob_up]

    if max_==4 :
        print('il numero è ', max_)
        for i in range(4) :
            probs[i] = rescaled_probs[i]
    if max_==3 :
        print('il numero è ', max_)
        occupied = -1
        for i in range(4) :
            if spaces[i]==-3 :
                occupied = i
                break
        missed_prob = rescaled_probs[occupied]
        probs[occupied] = 0
        for i in range(4) :
            if i!=occupied :
                probs[i] = rescaled_probs[i]+(1/max_)*missed_prob
    if max_==2 :
        print('il numero è ', max_)
        occupied1 = -1
        occupied2 = -1
        for i in range(4) :
            if spaces[i]==-3 and occupied1==-1 :
                occupied1 = i
            if spaces[i]==-3 and i>occupied1 :
                occupied2 = i
                break
        missed_prob1 = rescaled_probs[occupied1]
        missed_prob2 = rescaled_probs[occupied2]
        probs[occupied1] = 0
        probs[occupied2] = 0
        for i in range(4) :
            if i!=occupied1 and i!=occupied2 :
                probs[i] = rescaled_probs[i]+((1/max_)*(missed_prob1+missed_prob2))
    if max_==1 :
        print('il numero è ', max_)
        for i in range(4) :
            if probs[i]!=0 :
                probs[i] = 1  # dovrebbe già esserlo per costruzione
    if max_==0 and how_many==1 :
        print('il numero è ', max_)
        probs[4] = 1
    if max_==0 and how_many==0 :
        print('Shit, how tha fuck is this even possibleeeeeeeeeeeeeee? Explain me, Bazzani.')

    #print('PROBS: ',probs[0],probs[1],probs[2],probs[3],probs[4])
    #print('SUM: ',probs[0]+probs[1]+probs[2]+probs[3]+probs[4])
    assert probs[0]+probs[1]+probs[2]+probs[3]+probs[4] == 1, 'ATTENTION: empty_probs_grav is giving a Distribution of Transition Probabilities non-Normalized to 1.'
    return probs

# THIS IS OK #########################################################
# Function that defines the Opinion Influence acting on the Individual
# at the (which)-th Site in the Ambient as the Mean Opinion
# of all Individual included in his Influence Zone,
# given by the extended Moore Neighborhood of 'distance' Radius.
# It is valid both for Distance Variation Model and Gravitational Flocking Model.
def influence_norm(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: influence_norm() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: influence_norm() needs a non-negative integer as second argument, lower than dimension.'

    neighs = 0
    opinions = []
    for j in range(0, glob.dimension) :
        if j!=which :
            if ambient[j]!=[-3,-3] and table_distance(which,j)<=glob.distance :
                opinions.append(ambient[j][1])
                neighs += 1
    #print(opinions)

    # Influence as the Mean Opinion
    influence = ambient[which][1] # No Changements of Opinion in Absence of Friends
    if neighs>0 :
        sum_opinions = 0
        for i in range(len(opinions)) :
            sum_opinions += opinions[i]   # Each of their Opinion with same Weight
        influence = sum_opinions/neighs
    return influence

# THIS IS OK #########################################################
# Function that defines the Opinion Influence acting on the Individual
# at the 'which'-th Site in the Ambient as the Mean Opinion
# of 'vision' randomly-chosen Individuals included in his Influence Zone,
# given by the extended Moore Neighborhood of 'distance' Radius.
# It is valid only for the Partial Vision Model.
def influence_vis(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: influence_vis() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: influence_vis() needs a non-negative integer as second argument, lower than dimension.'

    neighs = 0
    opinions = []
    for j in range(0, glob.dimension) :
        if j!=which :
            if ambient[j]!=[-3,-3] and table_distance(which,j)<=glob.dimension :
                opinions.append(ambient[j][1])
                neighs += 1
    
    viewed_opinions = []
    if len(opinions)>=glob.vision :
        choice_indices = []
        while len(choice_indices)<glob.vision :
            choice_index = glob.np.random.randint(0,len(opinions))
            if choice_indices.count(choice_index)==0 :
                choice_indices.append(choice_index)
                viewed_opinions.append(opinions[choice_indices])
    if len(opinions)<glob.vision :
        viewed_opinions = opinions

    # Influence as the Mean Opinion
    influence = ambient[which][1]
    if len(viewed_opinions)>0 : 
        sum_opinions = 0
        for i in range(len(viewed_opinions)) :
            sum_opinions += viewed_opinions[i]  
        influence = sum_opinions/len(viewed_opinions)
        if len(viewed_opinions)==len(opinions) :
            normal_influence = influence_norm(ambient, which)
            print(influence,'&&&',normal_influence)
            assert influence==normal_influence, 'ATTENTION: Partial Vision Influence does not reduce to Normal Influence when vision is elevated.'
    
    return influence

# WORK IN PROGRESS ##################################################
# Function that features the One-Step Time Evolution of the Population
# on the Ambient for the 1° Scenario.
def evolve_norm(initial) :
    assert len(initial) == glob.dimension, 'ATTENTION: evolve_norm() needs a (dimension)-dim. array as argument.'


    final = [[-3,-3]]*glob.dimension
    eff_changes = 0
    people = 0
    for i in range(glob.dimension) :
        
        if initial[i]!=[-3,-3] :
            people += 1
            mean = influence_norm(initial, i)
            
            prob_change = glob.np.random.uniform(0,1)

            # First Attempt
            changed_opinion = glob.np.sign(mean)
            if changed_opinion==0 :
                changed_opinion = initial[i][1]

            #print('x =',mean,', y =',changed_opinion,', s =',initial[i])
            empty_spacez = empty_spaces(final, i)
            how_many = len(empty_spacez)
            step_4dir = glob.np.random.randint(0,4)
            step_3dir = glob.np.random.randint(0,3)
            step_2dir = glob.np.random.randint(0,2)
            

            # Event of Opinion Change
            if prob_change<=glob.np.tanh(glob.T) :
                #if changed_opinion!=initial[i][1] :
                    #print(initial[i][1],'-->',mean,'-->',changed_opinion)
                    #eff_changes += 1
                    #print('There have been ', eff_changes, ' changements of opinion.')
                match how_many:
                    case 1:
                        final[empty_spacez[0]] = [initial[i][0], changed_opinion] 
                
                    case 2:
                        if empty_spacez[1]!=i :
                            final[empty_spacez[step_2dir]] = [initial[i][0], changed_opinion]
     
                        if empty_spacez[1]==i :
                            final[empty_spacez[0]] = [initial[i][0], changed_opinion]
         
                    case 3:
                        if empty_spacez[2]!=i :
                            final[empty_spacez[step_3dir]] = [initial[i][0], changed_opinion]
  
                        if empty_spacez[2]==i :
                            final[empty_spacez[step_2dir]] = [initial[i][0], changed_opinion]

                    case 4:
                        if empty_spacez[3]!=i :
                            final[empty_spacez[step_4dir]] = [initial[i][0], changed_opinion]

                        if empty_spacez[3]==i :
                            final[empty_spacez[step_3dir]] = [initial[i][0], changed_opinion]

                    case 5:
                        final[empty_spacez[step_4dir]] = [initial[i][0], changed_opinion]
            
            # Event of Same Opinion as Before
            if prob_change>glob.np.tanh(glob.T) :
       
                match how_many:
                    case 1:
                        final[empty_spacez[0]] = initial[i]

                    case 2:
                        if empty_spacez[1]!=i :
                            final[empty_spacez[step_2dir]] = initial[i]

                        if empty_spacez[1]==i :
                            final[empty_spacez[0]] = initial[i]
 
                    case 3:
                        if empty_spacez[2]!=i :
                            final[empty_spacez[step_3dir]] = initial[i]

                        if empty_spacez[2]==i :
                            final[empty_spacez[step_2dir]] = initial[i]

                    case 4:
                        if empty_spacez[3]!=i :
                            final[empty_spacez[step_4dir]] = initial[i]

                        if empty_spacez[3]==i :
                            final[empty_spacez[step_3dir]] = initial[i]

                    case 5:
                        final[empty_spacez[step_4dir]] = initial[i] 
    #print('\n\n')             
    return final

# WORK IN PROGRESS ##################################################
# Function that features the One-Step Time Evolution of the Population 
# on the Ambient for the 2° Scenario
def evolve_grav(initial) :
    assert len(initial) == glob.dimension, 'ATTENTION: evolve_grav() needs a (dimension)-dim. array as argument.'

    final = [[-3,-3]]*glob.dimension
    eff_changes = 0
    people = 0
    for i in range(glob.dimension) :
        
        if initial[i]!=[-3,-3] :
            people += 1
            mean = influence_norm(initial, i)
            
            # First Attempt
            changed_opinion = glob.np.sign(mean*initial[i][1])
            if changed_opinion==0 :
                changed_opinion = initial[i][1]
            
            #print('x =',mean,', y =',changed_opinion,', s =',initial[i])
            spaces = empty_spaces_grav(final, i)
            #print('WHO: ', i)
            #print('SPACES: ',spaces)
            probs = empty_probs_grav(initial, spaces, i)
            #step_4dir = glob.np.random.randint(0,4)
            #step_3dir = glob.np.random.randint(0,3)     # USELESSSSSSSS
            #step_2dir = glob.np.random.randint(0,2)

            # Event of Opinion Change
            prob_change = glob.np.random.uniform(0,1)
            if prob_change<=glob.np.tanh(glob.T) :
                if changed_opinion!=initial[i][1] :
                    eff_changes += 1
                    print('There have been ', eff_changes, ' changements of opinion.')
                
                final[glob.np.random.choice(spaces, p=probs)] = [initial[i][0], changed_opinion] 
                
            # Event of Same Opinion as Before
            if prob_change>glob.np.sign(initial[i][1])*glob.np.tanh(initial[i][1]*glob.T) :  #di nuovo per ora
       
                final[glob.np.random.choice(spaces, p=probs)] = initial[i]

    #print('\n\n')             
    return final

# WORK IN PROGRESS ##################################################
# Function that features the One-Step Time Evolution of the Population 
# on the Ambient of the 3° Scenario
def evolve_vis(initial) :
    assert len(initial) == glob.dimension, 'ATTENTION: evolve_vis() needs a (dimension)-dim. array as argument.'

    final = [[-3,-3]]*glob.dimension
    eff_changes = 0
    people = 0
    for i in range(glob.dimension) :
        
        if initial[i]!=[-3,-3] :
            people += 1
            mean = influence_vis(initial, i)
            #print('mean is',mean)
            
            prob_change = glob.np.random.uniform(0,1)

            # First Attempt
            changed_opinion = glob.np.sign(mean)
            if changed_opinion==0 :
                changed_opinion = initial[i][1]
            #print('initial opinion is',initial[i][1])
            #print('changed opinion is',changed_opinion)


            #print('x =',mean,', y =',changed_opinion,', s =',initial[i])
            step_4dir = glob.np.random.randint(0,4)
            step_3dir = glob.np.random.randint(0,3)
            step_2dir = glob.np.random.randint(0,2)
            empty_spacez = empty_spaces(final, i)
            how_many = len(empty_spacez)

            # Event of Opinion Change
            if prob_change<=glob.np.tanh(glob.T) :
                if changed_opinion!=initial[i][1] :
                    eff_changes += 1
                    print('There have been ', eff_changes, ' changements of opinion.')
                    print(initial[i][1],'-->',changed_opinion)
                match how_many:
                    case 1:
                        final[empty_spacez[0]] = [initial[i][0], changed_opinion] 
                
                    case 2:
                        if empty_spacez[1]!=i :
                            final[empty_spacez[step_2dir]] = [initial[i][0], changed_opinion]
     
                        if empty_spacez[1]==i :
                            final[empty_spacez[0]] = [initial[i][0], changed_opinion]
         
                    case 3:
                        if empty_spacez[2]!=i :
                            final[empty_spacez[step_3dir]] = [initial[i][0], changed_opinion]
  
                        if empty_spacez[2]==i :
                            final[empty_spacez[step_2dir]] = [initial[i][0], changed_opinion]

                    case 4:
                        if empty_spacez[3]!=i :
                            final[empty_spacez[step_4dir]] = [initial[i][0], changed_opinion]

                        if empty_spacez[3]==i :
                            final[empty_spacez[step_3dir]] = [initial[i][0], changed_opinion]

                    case 5:
                        final[empty_spacez[step_4dir]] = [initial[i][0], changed_opinion]
            
            # Event of Same Opinion as Before
            if prob_change>glob.np.tanh(glob.T) :
       
                match how_many:
                    case 1:
                        final[empty_spacez[0]] = initial[i]

                    case 2:
                        if empty_spacez[1]!=i :
                            final[empty_spacez[step_2dir]] = initial[i]

                        if empty_spacez[1]==i :
                            final[empty_spacez[0]] = initial[i]
 
                    case 3:
                        if empty_spacez[2]!=i :
                            final[empty_spacez[step_3dir]] = initial[i]

                        if empty_spacez[2]==i :
                            final[empty_spacez[step_2dir]] = initial[i]

                    case 4:
                        if empty_spacez[3]!=i :
                            final[empty_spacez[step_4dir]] = initial[i]

                        if empty_spacez[3]==i :
                            final[empty_spacez[step_3dir]] = initial[i]

                    case 5:
                        final[empty_spacez[step_4dir]] = initial[i] 
    #print('\n\n')             
    return final

# THIS IS OK ########################################################
# Function that collects the X and Y Positions for each Individual with Opinion
# corresponding to color in Two different Arrays
def xydata_scatter(ambient, color) :
    assert len(ambient) == glob.dimension, 'ATTENTION: xydata_scatter() needs a (dimension)-dim. array as first argument.'
    assert (color=='empty') or (color=='red') or (color=='blue'), 'ATTENTION: xydata_scatter() needs a precise string literal as second argument.' 

    which_color = 0
    if color=='empty' :
        which_color = -3
    if color=='red' :
        which_color = -1
    if color=='blue' :
        which_color = +1
    
    # Fullfilling of the Position Arrays for each Color
    xdata_color = []
    ydata_color = []
    j = -1
    for i in range(glob.dimension) :
        j += 1
        ydata = abs(int((i/glob.side)+1))
        xdata = abs(int(i+1-(ydata-1)*glob.side))
        if ambient[i][1]==which_color : 
            xdata_color.append(xdata)
            ydata_color.append(ydata)

    return xdata_color, ydata_color 

# MAYBE, THIS IS USELESS ############################################
# THIS IS OK ########################################################
# Function that saves on CSV File the Info about the i-th Individual
def data_extr(ambient, i, fout, t):
    assert len(ambient) == glob.dimension, 'ATTENTION: data_extr() needs a (dimension)-dim. array as first argument.'
    assert (i>=0) and (i<glob.dimension), 'ATTENTION: data_extr() needs a non-negative integer as second argument, lower than dimension.'
    assert (t>=0) and (t<glob.nsteps), 'ATTENTION: data_extr() needs a non-negative integer as fourth argument, lower than nsteps.'

    empty = 0
    red = 0
    blue = 0
    opinion_class = ['empty','red','blue']
    if ambient[i]==[-3,-3] :
        empty = i
        fout.write(f'{opinion_class[0]}, {-3}, {ambient[i][1]}, {empty}, {t}\n')
    if ambient[i][1]==-1 : 
        red = i
        fout.write(f'{opinion_class[1]}, {ambient[i][0]}, {ambient[i][1]}, {red}, {t}\n')
    if ambient[i][1]==+1 :
        blue = i
        fout.write(f'{opinion_class[4]}, {ambient[i][0]}, {ambient[i][1]}, {blue}, {t}\n')

def magnetization_data_storage(data, fout):
    assert len(data) == glob.nsteps, 'ATTENTION: magnetization_data_storage() needs a (nsteps)-dim. array of floats as first argument.'
    
    fout.write('Time_Step, Magnetization_Value\n')
    for t in range(glob.nsteps) :
        fout.write(f'{t} {data[t]}\n')

def decision_time_data_storage(data, fout):
    assert len(data) == glob.nsteps-1, 'ATTENTION: time_data_storage() needs a (nsteps)-dim. array of floats as first argument.'
    
    fout.write('Occurrences, Corresponding_Decision_Time\n')
    for t in range(glob.nsteps) :
        fout.write(f'{t+1} {data[t]}\n')

# THIS IS OK ########################################################
# Function that makes possible to view the Animation
def update_scatter(time) :
    assert (time>=0) and (time<glob.nsteps), 'ATTENTION: update_scatter() needs a non-negative integer as argument, lower than nsteps.'

    glob.ax_histo.clear()  
    glob.ax.clear()  
    glob.ax.set_title('Agent-Based Cellular Automata Simulation') 
    glob.ax.set_xlabel('x')
    glob.ax.set_ylabel('y')
    glob.ax.grid(False) #False to not show 

    xempties, yempties = xydata_scatter(glob.ambient_evolution[time], 'empty')
    xred, yred = xydata_scatter(glob.ambient_evolution[time], 'red')
    xblue, yblue = xydata_scatter(glob.ambient_evolution[time], 'blue')

    glob.ax.scatter(xempties, yempties, s=200-0.15*glob.dimension, c='w', label= 'Step Temporale '+ str(time), alpha=0, edgecolors='k')
    glob.ax.scatter(xred, yred, s=200-0.15*glob.dimension, c='tab:red', label='Agente A', edgecolors='k')
    glob.ax.scatter(xblue, yblue, s=200-0.15*glob.dimension, c='tab:blue', label='Agente B', edgecolors='k')

    glob.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

    bar_heights = [len(xred),len(xblue)]
    glob.ax_histo.bar([-0.5,0.5], height=bar_heights, color=['tab:red','tab:blue'])
    glob.ax_histo.set_title('Occorrenze delle Opinioni')
    glob.ax_histo.set_xlabel('Opinioni')
    glob.ax_histo.set_ylabel('Occorrenze')

    # glob.plt.tight_layout() ERRORE DI COMPATIBIITà CON GLI ASSI

def local_density2(ambient, which, distance) :
    assert len(ambient) == glob.dimension, 'ATTENTION: local_density2() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: local_density2() needs a non-negative integer as second argument, lower than dimension.'
    assert (distance>0) and (distance<=int((glob.side-1)/2)), 'ATTENTION: local_density2() needs a non-negative integer as third argument, lower than its max. value int((side-1)/2)).'

    opinion = ambient[which][1]
    assert opinion != -3, 'ATTENTION: The Individual passed through the Local Density Function is instead an Empty Space.'

    density = 0
    density_indices = []
    for j in range(glob.dimension) :
        if j!=which and j>=0 and j<glob.dimension :
            if ambient[j][1]==opinion and table_distance(which,j)<=distance :
                density_indices.append(j)
                density += 1
    
    density_indices.sort()
    return [density, which, density_indices]

# THIS IS OK ########################################################
# Function that return how many people with a certain opinion can be seen by a person with that opinion in his range of influence
def local_density(opinion, ambient, distance) : #provo a scrivere una funzione che calcola la densità locale di una certa opinione (utile per il flocking)
    assert len(ambient) == glob.dimension, 'ATTENTION: local_density() needs a (dimension)-dim. array as second argument.'
    assert (opinion==-1) or (opinion==+1), 'ATTENTION: local_density() needs a two-valued integer (-1 or +1) as first argument.'
    assert (distance>0) and (distance<=int((glob.side-1)/2)), 'ATTENTION: local_density() needs a non-negative integer as third argument, lower than its max. value int((side-1)/2)).'

    grav_interaction = [] #densità, posizione
    
    for i in range(0, glob.dimension) : #scorro ambient ricercando persone con l'opinione desiderata
        density = 0 #si riparte a contare da zero tra un individuo e l'altro
        counter_left = 0 #potrebbe non servire a un caZZ0
        known_box = []
        density_index = []
        
        if ambient[i][1]==opinion :   #oppure solo ambient[i] se togliamo gli amici
            for j in range(0, 2*distance+1) : #sale di uno ogni volta [0,2distace]

                #print("JEY",j)
                line = int(i/glob.side)
                counter_down = 0
                right_increment = 0
                left_increment = 0

                #sfora di sotto
                if line-distance<0 : 
                    down_increment = abs(line-distance)
                    #print("Down", down_increment)
                    xdata = int(i-(int((i/glob.side)+1)-1)*glob.side)

                    if j<down_increment :
                        for d in range( glob.side*(glob.side-down_increment)+xdata-distance+j*glob.side, glob.side*(glob.side-down_increment)+xdata+distance+1+j*glob.side) :
                            counter_down = j+1
                            #print("D", d)
                            if known_box.count(d)==0 and d!=i and d>=0 and d<glob.dimension :
                                if int(d/glob.side)*glob.side>=(glob.side-down_increment)*glob.side :
                                    known_box.append(d)
                                    if ambient[d][1]==opinion :
                                        density = density+1
                                        if d!=i and density_index.count(d)<1 :
                                            density_index.append(d)

                #sfora di sopra
                if line+distance>glob.side-1 :
                    up_increment = abs(line+distance-glob.side+1)
                    #print("Up", up_increment)
                    xdata = int(i-(int((i/glob.side)+1)-1)*glob.side)

                    if j<up_increment :
                        for u in range( xdata-distance+j*glob.side, xdata+distance+1+j*glob.side) :
                            #if u < 0: print("bro wtf")
                            if known_box.count(u)==0 and u!=i and u>=0 and u<glob.dimension:
                                if int(u/glob.side)*glob.side<(up_increment)*glob.side  :
                                    known_box.append(u)
                                    #ambient[u] = [ambient[u][0], +2]
                                    if ambient[u][1]==opinion :
                                        density = density+1
                                        if u!=i and density_index.count(u)<1 :
                                            density_index.append(u)

                #sfora a destra
                if int((i+distance)/glob.side)>line or (i+distance)/glob.side>glob.dimension-1 :
                    xdata = int(i-(int((i/glob.side)+1)-1)*glob.side)
                    #l'ultimo elemento della riga di i è (side*(line+1)-1)
                    right_increment = int(abs((glob.side*(line+1)-1)-(xdata+glob.side*line)-distance))
                    #print("Right", right_increment)
                    for r in range( line*(glob.side)-distance*glob.side+j*glob.side, line*(glob.side)-distance*glob.side+right_increment+j*glob.side ) :
                        
                        if r<0 : 
                            b = glob.dimension+r
                            if known_box.count(b)==0 :
                                known_box.append(b)
                                if ambient[b][1]==opinion :
                                    density = density+1
                                    if b!=i and density_index.count(b)<1 :
                                        density_index.append(b)
                        
                        if known_box.count(r)==0 and r!=i and r>=0 :
                            if r<glob.dimension :
                                known_box.append(r)
                                if ambient[r][1]==opinion :
                                        density = density+1
                                        if r!=i and density_index.count(r)<1 :
                                            density_index.append(r)
                                
                            else :
                                r = r-glob.dimension
                                if known_box.count(r)==0 :
                                    known_box.append(r)
                                    if ambient[r][1]==opinion :
                                        density = density+1
                                        if r!=i and density_index.count(r)<1 :
                                            density_index.append(r)

                #sfora a sinistra
                if int((i-distance)/glob.side)<line or (i-distance)/glob.side<0 :
                    xdata = int(i-(int((i/glob.side)+1)-1)*glob.side)
                    left_increment = int(abs(distance-(xdata+glob.side*line-glob.side*line)))
                    #print("Left", left_increment)
                    for l in range( (line+1)*glob.side-left_increment-distance*glob.side+j*glob.side, (line+1)*glob.side-1-distance*glob.side+1+j*glob.side ) :
                        
                        if l<0 : 
                            a = glob.dimension+l
                            if known_box.count(a)==0 :
                                known_box.append(a)
                                if ambient[a][1]==opinion :
                                    density = density+1
                                    if a!=i and density_index.count(a)<1 :
                                        density_index.append(a)
                        
                        if l!=i and l>=0 :
                            if l<glob.dimension :
                                counter_left = counter_left+1
                                if known_box.count(l)==0 :
                                    known_box.append(l)
                                    if ambient[l][1]==opinion :
                                        density = density+1
                                        if l!=i and density_index.count(l)<1 :
                                            density_index.append(l)
                                
                            else :
                                l = l-glob.dimension
                                if known_box.count(l)==0 :
                                    known_box.append(l)
                                    if ambient[l][1]==opinion :
                                        density = density+1
                                        if l!=i and density_index.count(l)<1 :
                                            density_index.append(l)

                # LOOP dell'intorno "buono" di i
                for k in range(i-distance*(glob.side+1)+(j+counter_down)*glob.side+left_increment, i-distance*(glob.side-1)+1-right_increment+(j+counter_down)*glob.side ) : #scorro tutte le caselle di un quadrato di lato 2 distance+1. j*side fa salire di riga ad ogni iterazione del for più esterno

                    if k>=0 and k<=glob.dimension-1 :
                        #print("MACARENA", counter) #numero di iterazioni 
                        if k!=i and known_box.count(k)==0 :
                            if k<0 : print("bro wtf")
                            known_box.append(k)
                            if ambient[k][1]==opinion :
                                        density = density+1
                                        if k!=i and density_index.count(k)<1 :
                                            density_index.append(k)

            known_box.sort()
            #print(known_box)
            assert len(known_box) == (2*distance+1)*(2*distance+1)-1, print('sticazzi')#assertion to ensure that the area of range is a constant
            for g in range(0, len(known_box)) :
                assert known_box.count(g) <= 1, print('stocazzo')

            #####################################################################################################################
            density_index.sort() # aggiunto da me ###############################################################################
            #####################################################################################################################

            #print("Density:", density," at position ", i)
            grav_interaction.append([density, i, density_index])

    #print("Gravition: ", grav_interaction)
                    
    # bada bene che density non misura il numero di persone che ci sono in un certo spazio, ma è un parametro che quantifica il numero di persone (che hanno una certa
    # opinione) percepite da un certo individuo che ha quella stessa opinione. In pratica dice quante persone vede un dato individuo, infatti esclude se stesso. è ovvio
    # che se ho 4 persone tutte ammassate, density aumenta molto perchè ogni individuo dei 4 ne vede 3 (quindi density = 12) ed è evidente che non quantifica il numero di 
    # individui ma è solo un parametro di ammassamento
    return grav_interaction

#SEEMS TO BE OK, mi serve una funzione simile a table distance ma che restituisca la distanza di x e di y
def xy_distance(first, second) :
    assert (first>=0) and (first<glob.dimension), 'ATTENTION: xy_distance() needs a non-negative integer as first argument, lower than dimension.'
    assert (second>=0) and (second<glob.dimension), 'ATTENTION: xy_distance() needs a non-negative integer as second argument, lower than dimension.'

    #salvo le coordinate in un array
    xy1 = []
    xy1.append(xydata(first)[0])
    xy1.append(xydata(first)[1])
    
    xy2 = []
    xy2.append(xydata(second)[0])
    xy2.append(xydata(second)[1])

    periodic_distance = [0, 0]

    #distanza calcolata in modo normale
    #da sinistra a destra è +
    #da basso ad alto è +
    
    sgnx_2_1_norm = glob.np.sign(xy2[0]-xy1[0])

    sgny_2_1_norm = glob.np.sign(xy2[1]-xy1[1])

    normal_distance = [sgnx_2_1_norm*abs(xy2[0]-xy1[0]), sgny_2_1_norm*abs(xy2[1]-xy1[1])]

    #distanza calcolata in modo periodico
    #da destra a sinistra è -
    #da alto ad basso è -

    periodic_distance[0] = normal_distance[0]-glob.side
    if abs(periodic_distance[0])>glob.side : periodic_distance[0] = glob.side-abs(periodic_distance[0])+glob.side
    if abs(periodic_distance[0])==glob.side : periodic_distance[0] = 0

    periodic_distance[1] = glob.side+normal_distance[1]
    if abs(periodic_distance[1])>glob.side : periodic_distance[1] = -glob.side+abs(periodic_distance[1])-glob.side
    if abs(periodic_distance[1])==glob.side : periodic_distance[1] = 0

    return normal_distance, periodic_distance

#OK? depends on xy_distance
def gravity(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: gravity() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: gravity() needs a non-negative integer as second argument, lower than dimension.'

    opinion = ambient[which][1]
    grav_int = local_density(opinion, ambient, int((glob.side-1)/2)) #passo il range massimo per renderla non locale (campo medio)
    nth = 0
    gravitation_x = 0
    gravitation_y = 0
    force_x = 0
    force_y = 0

    #if opinion==-3 : return False
    assert opinion != -3
    for k in range(0, glob.dimension) :
        if ambient[k][1]==opinion :
            nth += 1
            if k==which : break

    #print (grav_int[nth-1]) #la persona alla posizione i sente una forza pari a density/pos?? dalle persone di density index
    
    for j in range(0, grav_int[nth-1][0]) :
    
        #assert len(grav_int[nth-1][2]) == numero di persone di una data opinione - 1
        # x[0] normale, x[1] periodico
        x = [xy_distance(which, grav_int[nth-1][2][j])[0][0], xy_distance(which, grav_int[nth-1][2][j])[1][0]]
        y = [xy_distance(which, grav_int[nth-1][2][j])[0][1], xy_distance(which, grav_int[nth-1][2][j])[1][1]]
        
        #print("le x ",x,"le y ", y)
        # salvo i segni
        sgnx0 = glob.np.sign(x[0])
        sgnx1 = glob.np.sign(x[1])
        sgny0 = glob.np.sign(y[0])
        sgny1 = glob.np.sign(y[1])

        # cerco i minori in valore assoluto
        x_ = [abs(x[0]), abs(x[1])]
        y_ = [abs(y[0]), abs(y[1])]

        #print(x_)
        #print(y_)

        # mi ricordo dei segni
        if sgnx0*min(x_)==x[0] : x_dist = x[0]
        if sgnx1*min(x_)==x[1] : x_dist = x[1]
        if sgny0*min(y_)==y[0] : y_dist = y[0]
        if sgny1*min(y_)==y[1] : y_dist = y[1]
        
        #print(x_dist)
        #print(y_dist)

        if x_dist==0 : force_x = 0
        if y_dist==0 : force_y = 0

        if x[1]==x_dist and x_dist!=0 :
            # le distanze contate periodicamente sono negative
            '''volevo mettere density come costante moltilpicativa ma ha più senso non mettere nulla...è come avere le masse uguali a 1'''
            #force_x = grav_int[nth-1][0]*(  -1*pow(x_dist, -2) )
            #x_dist = -1*x_dist
            force_x = ( glob.G*glob.np.sign(x_dist)/pow(x_dist, 2) )
            #print(force_x)

        if y[1]==y_dist and y_dist!=0 :
            # le distanze contate periodicamente sono negative
            #y_dist = -1*y_dist
            force_y = ( glob.G*glob.np.sign(y_dist)/pow(y_dist, 2) )
            #print(force_y)

        if x[0]==x_dist and x_dist!=0 :
            # le distanze contate normalmente sono positive
            force_x = ( glob.G*glob.np.sign(x_dist)/pow(x_dist, 2) )
            #print(force_x)

        if y[0]==y_dist and y_dist!=0 :
            # le distanze contate normalmente sono positive
            force_y = ( glob.G*glob.np.sign(y_dist)/pow(y_dist, 2) )
            #print(force_y)

        #se le distanze sono uguali la forza è nulla
        if x[0]==x[1] :
            force_x = 0
            #print("forza y nulla")

        if y[0]==y[1] :
            force_y = 0
            #print("forza x nulla")
        
        #componente x e y totali del campo di forze, con segno
        gravitation_x = gravitation_x+force_x
        gravitation_y = gravitation_y+force_y
    

    return [gravitation_x, gravitation_y]

def gravity2(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: gravity2() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: gravity2() needs a non-negative integer as second argument, lower than dimension.'

    opinion = ambient[which][1]
    grav_int = local_density2(ambient, which, int((glob.side-1)/2)) #passo il range massimo per renderla non locale (campo medio)
    nth = 0
    gravitation_x = 0
    gravitation_y = 0
    force_x = 0
    force_y = 0

    #if opinion==-3 : return False
    assert opinion != -3
    for k in range(0, glob.dimension) :
        if ambient[k][1]==opinion :
            nth += 1
            if k==which : break

    #print (grav_int[nth-1]) #la persona alla posizione i sente una forza pari a density/pos?? dalle persone di density index
    
    for j in range(0, grav_int[0]) :
    
        #assert len(grav_int[nth-1][2]) == numero di persone di una data opinione - 1
        # x[0] normale, x[1] periodico
        x = [xy_distance(which, grav_int[2][j])[0][0], xy_distance(which, grav_int[2][j])[1][0]]
        y = [xy_distance(which, grav_int[2][j])[0][1], xy_distance(which, grav_int[2][j])[1][1]]
        
        #print("le x ",x,"le y ", y)
        # salvo i segni
        sgnx0 = glob.np.sign(x[0])
        sgnx1 = glob.np.sign(x[1])
        sgny0 = glob.np.sign(y[0])
        sgny1 = glob.np.sign(y[1])

        # cerco i minori in valore assoluto
        x_ = [abs(x[0]), abs(x[1])]
        y_ = [abs(y[0]), abs(y[1])]

        #print(x_)
        #print(y_)

        # mi ricordo dei segni
        if sgnx0*min(x_)==x[0] : x_dist = x[0]
        if sgnx1*min(x_)==x[1] : x_dist = x[1]
        if sgny0*min(y_)==y[0] : y_dist = y[0]
        if sgny1*min(y_)==y[1] : y_dist = y[1]
        
        #print(x_dist)
        #print(y_dist)

        if x_dist==0 : force_x = 0
        if y_dist==0 : force_y = 0

        if x[1]==x_dist and x_dist!=0 :
            # le distanze contate periodicamente sono negative
            '''volevo mettere density come costante moltilpicativa ma ha più senso non mettere nulla...è come avere le masse uguali a 1'''
            #force_x = grav_int[nth-1][0]*(  -1*pow(x_dist, -2) )
            #x_dist = -1*x_dist
            force_x = ( glob.G*glob.np.sign(x_dist)/pow(x_dist, 2) )
            #print(force_x)

        if y[1]==y_dist and y_dist!=0 :
            # le distanze contate periodicamente sono negative
            #y_dist = -1*y_dist
            force_y = ( glob.G*glob.np.sign(y_dist)/pow(y_dist, 2) )
            #print(force_y)

        if x[0]==x_dist and x_dist!=0 :
            # le distanze contate normalmente sono positive
            force_x = ( glob.G*glob.np.sign(x_dist)/pow(x_dist, 2) )
            #print(force_x)

        if y[0]==y_dist and y_dist!=0 :
            # le distanze contate normalmente sono positive
            force_y = ( glob.G*glob.np.sign(y_dist)/pow(y_dist, 2) )
            #print(force_y)

        #se le distanze sono uguali la forza è nulla
        if x[0]==x[1] :
            force_x = 0
            #print("forza y nulla")

        if y[0]==y[1] :
            force_y = 0
            #print("forza x nulla")
        
        #componente x e y totali del campo di forze, con segno
        gravitation_x = gravitation_x+force_x
        gravitation_y = gravitation_y+force_y
    

    return [gravitation_x, gravitation_y]


#def partial_vision(ambient, which) : #ritorna un array delle posizioni che vede un certo individuo
#    
#    opinion = ambient[which][1]
#    grav_int = local_density(opinion, ambient, glob.distance)
#    nth = 0 # mi darà la posizione ordinale della persona i all'interno dell'array grav_int
#    choosen = []
#    if opinion==-3 : return False
#    for k in range(0, glob.dimension) :
#        if ambient[k][1]==opinion :
#            nth = nth+1
#            if k==which : break
#     
#    if glob.vision>=len(grav_int[nth-1][2]) : 
#        return grav_int[nth-1][2] # lo lascia inalterato
#
#    if glob.vision<len(grav_int[nth-1][2]) :
#        for j in range(0, glob.vision) :
#            choice = glob.np.random.choice(grav_int[nth-1][2])
#            choosen.append(choice)
#            #controllo di non avere più volte la stessa estrazione
#            for i in range(0, len(choosen)) :
#                while choosen.count(choosen[i]) > 1 : #genero una scelta non doppione
#                    choosen[i] = glob.np.random.choice(grav_int[nth-1][2])
#
#        assert len(choosen) == glob.vision
#        #choosen.sort() 
#        #print(choosen)
#    
#        return choosen #funziona
                
