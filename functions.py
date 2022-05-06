import global_variables as glob

#####################################################################
# Function that returns a 2-dim. list of integers indicating the total
# number of Agents with Opinion +1 and -1 respectively.
def count_all(ambient) :
    nred = 0
    for i in range(glob.dimension) :
        if ambient[i][1]==-1 :
            nred += 1
    return [nred, glob.npeople-nred]

#####################################################################
# Function that allows the Inizialization of the Ambient 
# with randomly-chosen Positions for all Individuals.
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

#####################################################################
# Function that allows the Inizialization of the Ambient
# with randomly-chosen Positions for all Individuals,
# but the first 'initial_reds' are specifically reserved for
# Agents with Opinion -1. 
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

#####################################################################
# Function that analyzes the Ambient Time Evolution to obtain a list 
# of integers indicating the Time Interval needed to each Individual
# one by one for changing its own Opinion.
def decision_time_data(evolution) :
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

#####################################################################
# Function that returns the Position Index of the Individual, identified 
# by ID, on the Ambient.
def ID_position(ambient, ID) :
    assert len(ambient) == glob.dimension, 'ATTENTION: ID_position() needs a (dimension)-dim. array as first argument.'
    assert (ID!=-3) and (ID>=0) and (ID<glob.npeople), 'ATTENTION: ID_position() second argument must be integer and different from -3.'

    for i in range(glob.dimension) :
        if ambient[i][0]==ID :
            return i

#####################################################################
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
    end = glob.time.time()
    return xwhich, ywhich

#####################################################################
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

#####################################################################
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
        for j in [which-glob.side, which+glob.side-1, which+1, which+glob.side, which] : # sotto,sinistra,destra,sopra
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
        for j in [which-glob.side, which-1, which-glob.side+1, which+glob.side, which] : # sotto,sinistra,destra,sopra
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
        for j in [which-glob.side, which-1, which+1, which+glob.side, which] : # sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]==[-3,-3] :
                    empty_spaces.append(j)
                    how_many += 1
    return empty_spaces

#####################################################################
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
        for j in [which-glob.side, which+glob.side-1, which+1, which+glob.side, which] : # sotto,sinistra,destra,sopra
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
        for j in [which-glob.side, which-1, which-glob.side+1, which+glob.side, which] : # sotto,sinistra,destra,sopra
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
        for j in [which-glob.side, which-1, which+1, which+glob.side, which] : # sotto,sinistra,destra,sopra
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

#####################################################################
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
    exception = 0
    how_many = 0

    for i in range(5) :
        if spaces[i]==-3 :
            probs.append(0)
        if spaces[i]!=-3 :
            probs.append(1)
    # correzione della predilezione degli individui di muoversi rispetto che a stare fermi
    if probs.count(0)<4 and probs[4]==1 :
        probs[4] = 0 
    max_ = probs.count(1)
    grav_attraction = gravity(ambient, which)
    grav_x2 = grav_attraction[0]*grav_attraction[0]
    grav_y2 = grav_attraction[1]*grav_attraction[1]
    grav_modulus2 = grav_x2+grav_y2 

    prob_up = 0   
    prob_down = 0
    prob_left = 0
    prob_right = 0

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
        for i in range(4) :
            probs[i] = rescaled_probs[i]
    if max_==3 :
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
        for i in range(4) :
            if probs[i]!=0 :
                probs[i] = 1
    if max_==0 and how_many==1 :
        probs[4] = 1
    if max_==0 and how_many==0 :
        exception = 1
        probs[4] = 1

    assert (probs[0]+probs[1]+probs[2]+probs[3]+probs[4]>0.9999) and (probs[0]+probs[1]+probs[2]+probs[3]+probs[4]<1.0001),'ATTENTION: empty_probs_grav is giving a Distribution of Transition Probabilities non-Normalized to 1 at all.'
    return probs, exception

#####################################################################
# Function that handles a particular exception often occurring
# in the 2° Scenario, because it could happen that the Individual
# at the 'which'-th Site on the Ambient does not have any free 
# Movement Direction, including its own actual Position.
def find_most_near(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: find_most_near() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: find_most_near() needs a non-negative integer as second argument, lower than dimension.'

    ywhich = xydata(which)[1]
    d = 1
    while d<int((glob.side-1)/2) :
        low_ref = (ywhich-1-glob.distance)*glob.side
        if low_ref<0 :
            low_ref = glob.dimension+low_ref
        high_ref = (ywhich+glob.distance)*glob.side
        if high_ref>glob.dimension :
            high_ref = high_ref-glob.dimension

        equidistant_empties = []
        j = 0
        while j<glob.dimension :
            if j!=which :
                if low_ref<high_ref : # CASO NORMALE
                    if j<low_ref :
                        j = low_ref
                    if j>high_ref :
                        break
                if low_ref>high_ref : # 2 CASI DI SFORO
                    if j>high_ref and j<low_ref :
                        j = low_ref
                if ambient[j]==[-3,-3] and table_distance(which,j)==d :
                    if equidistant_empties.count(j)==0 :
                        equidistant_empties.append(j)
            j += 1
        if len(equidistant_empties)>0 :
            which_empty = glob.np.random.choice(equidistant_empties)
            return which_empty
            break
        d += 1
    

#####################################################################
# Function that defines the Opinion Influence acting on the Individual
# at the (which)-th Site in the Ambient as the Mean Opinion
# of all Individual included in his Influence Zone,
# given by the extended Moore Neighborhood of 'distance' Radius.
# It is valid both for Distance Variation Model and Gravitational Flocking Model.
def influence_norm(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: influence_norm() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: influence_norm() needs a non-negative integer as second argument, lower than dimension.'

    ywhich = xydata(which)[1]
    low_ref = (ywhich-1-glob.distance)*glob.side
    if low_ref<0 :
        low_ref = glob.dimension+low_ref
    high_ref = (ywhich+glob.distance)*glob.side
    if high_ref>glob.dimension :
        high_ref = high_ref-glob.dimension
    neighs = 0
    opinions = []
    j = 0
    while j<glob.dimension :
        if j!=which :
            if low_ref<high_ref : # CASO NORMALE
                if j<low_ref :
                    j = low_ref
                if j>high_ref :
                    break
            if low_ref>high_ref : # 2 CASI DI SFORO
                if j>high_ref and j<low_ref :
                    j = low_ref

            if ambient[j]!=[-3,-3] and table_distance(which,j)<=glob.distance :
                opinions.append(ambient[j][1])
                neighs += 1
        j += 1

    # Influence as the Mean Opinion
    influence = ambient[which][1] # No Changements of Opinion in Absence of Friends
    if neighs>0 :
        sum_opinions = 0
        for i in range(len(opinions)) :
            sum_opinions += opinions[i]   # Each of their Opinion with same Weight
        influence = sum_opinions/neighs
    return influence

#####################################################################
# Function that defines the Opinion Influence acting on the Individual
# at the 'which'-th Site in the Ambient as the Mean Opinion
# of 'vision' randomly-chosen Individuals included in his Influence Zone,
# given by the extended Moore Neighborhood of 'distance' Radius.
# It is valid only for the Partial Vision Model.
def influence_vis(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: influence_vis() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: influence_vis() needs a non-negative integer as second argument, lower than dimension.'

    ywhich = xydata(which)[1]
    low_ref = (ywhich-1-glob.distance)*glob.side
    if low_ref<0 :
        low_ref = glob.dimension+low_ref
    high_ref = (ywhich+glob.distance)*glob.side
    if high_ref>glob.dimension :
        high_ref = high_ref-glob.dimension
    neighs = 0
    opinions = []
    j = 0
    while j<glob.dimension :
        if j!=which :
            if low_ref<high_ref : # CASO NORMALE
                if j<low_ref :
                    j = low_ref
                if j>high_ref :
                    break
            if low_ref>high_ref : # 2 CASI DI SFORO
                if j>high_ref and j<low_ref :
                    j = low_ref

            if ambient[j]!=[-3,-3] and table_distance(which,j)<=glob.distance :
                opinions.append(ambient[j][1])
                neighs += 1
        j += 1
    
    viewed_opinions = []
    if len(opinions)>=glob.vision :
        choice_indices = []
        while len(choice_indices)<glob.vision :
            choice_index = glob.np.random.randint(0,len(opinions))
            if choice_indices.count(choice_index)==0 :
                choice_indices.append(choice_index)
                viewed_opinions.append(opinions[choice_index])
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
            assert influence==normal_influence, 'ATTENTION: Partial Vision Influence does not reduce to Normal Influence when vision is elevated.'
    return influence

#####################################################################
# Function that features the One-Step Time Evolution of the Population
# on the Ambient for the 1° Scenario.
def evolve_norm(initial) :
    assert len(initial) == glob.dimension, 'ATTENTION: evolve_norm() needs a (dimension)-dim. array as argument.'

    final = [[-3,-3]]*glob.dimension
    for i in range(glob.dimension) :
        
        if initial[i]!=[-3,-3] :
            mean = influence_norm(initial, i)
            
            prob_change = glob.np.random.uniform(0,1)

            changed_opinion = glob.np.sign(mean)
            if changed_opinion==0 :
                changed_opinion = initial[i][1]

            empty_spacez = empty_spaces(final, i)
            how_many = len(empty_spacez)
            step_4dir = glob.np.random.randint(0,4)
            step_3dir = glob.np.random.randint(0,3)
            step_2dir = glob.np.random.randint(0,2)

            # Event of Opinion Change
            if prob_change<=glob.np.tanh(glob.T) :                
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
    return final

#####################################################################
# Function that features the One-Step Time Evolution of the Population 
# on the Ambient for the 2° Scenario
def evolve_grav(initial) :
    assert len(initial) == glob.dimension, 'ATTENTION: evolve_grav() needs a (dimension)-dim. array as argument.'

    final = [[-3,-3]]*glob.dimension
    for i in range(glob.dimension) :
        
        if initial[i]!=[-3,-3] :
            mean = influence_norm(initial, i)
            
            changed_opinion = glob.np.sign(mean)
            if changed_opinion==0 :
                changed_opinion = initial[i][1]
            
            spaces = empty_spaces_grav(final, i)
            probs, exception = empty_probs_grav(initial, spaces, i)

            # Event of Opinion Change
            prob_change = glob.np.random.uniform(0,1)
            if prob_change<=glob.np.tanh(glob.T) :
                if exception==0 :
                    final[glob.np.random.choice(spaces, p=probs)] = [initial[i][0], changed_opinion] 
                else :
                    final[find_most_near(final,i)] = [initial[i][0], changed_opinion]
                
            # Event of Same Opinion as Before
            if prob_change>glob.np.tanh(glob.T) :
                if exception==0 :
                    final[glob.np.random.choice(spaces, p=probs)] = initial[i]
                else :
                    final[find_most_near(final,i)] = initial[i]
       
    return final

#####################################################################
# Function that features the One-Step Time Evolution of the Population 
# on the Ambient of the 3° Scenario
def evolve_vis(initial) :
    assert len(initial) == glob.dimension, 'ATTENTION: evolve_vis() needs a (dimension)-dim. array as argument.'

    final = [[-3,-3]]*glob.dimension
    for i in range(glob.dimension) :
        
        if initial[i]!=[-3,-3] :
            mean = influence_vis(initial, i)
            
            prob_change = glob.np.random.uniform(0,1)

            changed_opinion = glob.np.sign(mean)
            if changed_opinion==0 :
                changed_opinion = initial[i][1]

            step_4dir = glob.np.random.randint(0,4)
            step_3dir = glob.np.random.randint(0,3)
            step_2dir = glob.np.random.randint(0,2)
            empty_spacez = empty_spaces(final, i)
            how_many = len(empty_spacez)

            # Event of Opinion Change
            if prob_change<=glob.np.tanh(glob.T) :
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
           
    return final

#####################################################################
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

#####################################################################
# Function that saves on CSV File the whole Magnetization Time Evolution.
def magnetization_data_storage(data, fout) :
    assert len(data) == glob.nsteps, 'ATTENTION: magnetization_data_storage() needs a (nsteps)-dim. array of floats as first argument.'
    
    fout.write('Time_Step, Magnetization_Value\n')
    for t in range(glob.nsteps) :
        fout.write(f'{t} {data[t]}\n')

#####################################################################
# Function that saves on CSV File the Occurrences of all the detected
# values of Decision Time.
def decision_time_data_storage(data, fout):
    assert len(data) == glob.nsteps-1, 'ATTENTION: time_data_storage() needs a (nsteps)-dim. array of floats as first argument.'
    
    fout.write('Corresponding_Decision_Time, Occurrences\n')
    for t in range(glob.nsteps) :
        fout.write(f'{t+1} {data[t]}\n')

#####################################################################
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

    bar_heights = [0,len(xred),len(xblue),0]
    glob.ax_histo.bar([-1,-0.5,0.5,1], height=bar_heights, color=['tab:red','tab:blue'])
    glob.ax_histo.set_title('Occorrenze delle Opinioni')
    glob.ax_histo.set_xlabel('Opinioni')
    glob.ax_histo.set_ylabel('Occorrenze')

#####################################################################
# Function that returns a 3-dim. list relative to the specific Individual
# at the 'which'-th Site in the Ambient. The elements of that list are:
# number of other Agents with same Opinion in his extended Moore Neighborhood
# of 'distance' Radius, its Position Index on the Ambient and, finally,
# the Position Indices of the other previously-detected Agents.
def local_density(ambient, which, distance) :
    assert len(ambient) == glob.dimension, 'ATTENTION: local_density() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: local_density() needs a non-negative integer as second argument, lower than dimension.'
    assert (distance>0) and (distance<=int((glob.side-1)/2)), 'ATTENTION: local_density() needs a non-negative integer as third argument, lower than its max. value int((side-1)/2)).'

    opinion = ambient[which][1]
    assert opinion != -3, 'ATTENTION: The Individual passed through the Local Density Function is instead an Empty Space.'

    ywhich = xydata(which)[1]
    low_ref = (ywhich-1-distance)*glob.side
    if low_ref<0 :
        low_ref = glob.dimension+low_ref
    high_ref = (ywhich+distance)*glob.side
    if high_ref>glob.dimension :
        high_ref = high_ref-glob.dimension
    density = 0
    density_indices = []
    j = 0
    while j<glob.dimension :
        if j!=which :
            if low_ref<high_ref : # CASO NORMALE
                if j<low_ref :
                    j = low_ref
                if j>high_ref :
                    break
            if low_ref>high_ref : # 2 CASI DI SFORO
                if j>high_ref and j<low_ref :
                    j = low_ref

            if ambient[j][1]==opinion and table_distance(which,j)<=distance :
                density_indices.append(j)
                density += 1
        j += 1
    
    density_indices.sort()
    return [density, which, density_indices]

#####################################################################
# Function that returns a 2-dim. list of 2-dim. arrays of the
# x & y Coordinates of the Vector Distance between 'first'-th and
# 'second'-th Sites on the Ambient. First without, and second with
# taking into account the Periodic Boundary Conditions.
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

    #distanza calcolata in "modo normale"
    #da sinistra a destra è +
    #da basso ad alto è +
    
    sgnx_2_1_norm = glob.np.sign(xy2[0]-xy1[0])
    sgny_2_1_norm = glob.np.sign(xy2[1]-xy1[1])
    normal_distance = [sgnx_2_1_norm*abs(xy2[0]-xy1[0]), sgny_2_1_norm*abs(xy2[1]-xy1[1])]

    #distanza calcolata in "modo periodico"
    #da destra a sinistra è -
    #da alto ad basso è -

    periodic_distance[0] = normal_distance[0]-glob.side
    if abs(periodic_distance[0])>glob.side : periodic_distance[0] = glob.side-abs(periodic_distance[0])+glob.side
    if abs(periodic_distance[0])==glob.side : periodic_distance[0] = 0

    periodic_distance[1] = glob.side+normal_distance[1]
    if abs(periodic_distance[1])>glob.side : periodic_distance[1] = -glob.side+abs(periodic_distance[1])-glob.side
    if abs(periodic_distance[1])==glob.side : periodic_distance[1] = 0

    return normal_distance, periodic_distance

#####################################################################
# Function that calculates the x & y Coordinates of the Gravitational 
# Attraction Force acting on the Individual at 'which'-th Site
# on the Ambient.
def gravity(ambient, which) :
    assert len(ambient) == glob.dimension, 'ATTENTION: gravity() needs a (dimension)-dim. array as first argument.'
    assert (which>=0) and (which<glob.dimension), 'ATTENTION: gravity() needs a non-negative integer as second argument, lower than dimension.'

    opinion = ambient[which][1]
    grav_int = local_density(ambient, which, int((glob.side-1)/2))
    gravitation_x = 0
    gravitation_y = 0
    force_x = 0
    force_y = 0
    assert opinion != -3
    
    for j in range(0, grav_int[0]) :
        # x[0] normale, x[1] periodico
        x = [xy_distance(which, grav_int[2][j])[0][0], xy_distance(which, grav_int[2][j])[1][0]]
        y = [xy_distance(which, grav_int[2][j])[0][1], xy_distance(which, grav_int[2][j])[1][1]]
        
        # salvo i segni
        sgnx0 = glob.np.sign(x[0])
        sgnx1 = glob.np.sign(x[1])
        sgny0 = glob.np.sign(y[0])
        sgny1 = glob.np.sign(y[1])

        # cerco i minori in valore assoluto
        x_ = [abs(x[0]), abs(x[1])]
        y_ = [abs(y[0]), abs(y[1])]

        # mi ricordo dei segni
        if sgnx0*min(x_)==x[0] : x_dist = x[0]
        if sgnx1*min(x_)==x[1] : x_dist = x[1]
        if sgny0*min(y_)==y[0] : y_dist = y[0]
        if sgny1*min(y_)==y[1] : y_dist = y[1]
        
        if x_dist==0 : force_x = 0
        if y_dist==0 : force_y = 0

        if x[1]==x_dist and x_dist!=0 :
            force_x = ( glob.G*glob.np.sign(x_dist)/pow(x_dist, 2) )

        if y[1]==y_dist and y_dist!=0 :
            force_y = ( glob.G*glob.np.sign(y_dist)/pow(y_dist, 2) )

        if x[0]==x_dist and x_dist!=0 :
            force_x = ( glob.G*glob.np.sign(x_dist)/pow(x_dist, 2) )

        if y[0]==y_dist and y_dist!=0 :
            force_y = ( glob.G*glob.np.sign(y_dist)/pow(y_dist, 2) )

        #se le distanze sono uguali la forza è nulla
        if x[0]==x[1] :
            force_x = 0

        if y[0]==y[1] :
            force_y = 0
        
        #componente x e y totali del campo di forze, con segno
        gravitation_x = gravitation_x+force_x
        gravitation_y = gravitation_y+force_y
    
    return [gravitation_x, gravitation_y]

#####################################################################
# Function that returns False until the Ambient reaches a known
# Stationary Distribution of the Opinions at 'step' Instant,
# when instead returns a 2-dim. list of integers indicating which of 
# the Two Known Stationary Distributions is reached, and when this
# finally occurred.
def stop_if_eq (ambient, step) :
    assert len(ambient) == glob.dimension, 'ATTENTION: gravity() needs a (dimension)-dim. array as first argument.'

    static_case = [] #condizioni di equilibrio
    counter = 0
    count_red = 0 #sono i +1
    count_blue = 0 # sono i -1

    for i in range(len(ambient)) : 
        if ambient[i][1] == +1 : count_red += 1
        if ambient[i][1] == -1 : count_blue += 1
    assert count_red + count_blue == glob.npeople

    if count_red == glob.npeople :
        static_case.append([1, step])
        counter += 1
    if count_blue == glob.npeople :
        static_case.append([-1, step])
        counter += 1

    if counter != 0 : 
        assert len(static_case) == 1 
        return static_case
    
    else : return False
