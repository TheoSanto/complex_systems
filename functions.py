import global_variables as glob

# THIS IS OK ########################################################
# Function that returns if a Value is already in an Array of Integers
def is_there_equals(array, value) :
    if array.count(value)!=0 : return True
    else: return False

# THIS IS OK ########################################################
# Function that returns a Matrix containing the Friends' Links 
# for each Individual
#def choose_friends() :
#    friends_matrix = [[-3]*(glob.npeople-1)]*glob.npeople
#    
#    for j in range(glob.npeople) :
#
#        # Extraction of the n° of Friends of j-th Individual
#        gaus_num_friends = int(glob.np.random.normal(2,2)) # da definire meglio 
#        '''NOTA: IL NUMERO DI AMICI GENERATI GAUSSIANAMENTE SOTTOSTIMA QUELLO REALE, QUESTO PERCHè LE AMICIZIE "NON CORRISPOSTE" VALGONO 
#        COME EFFETTIVE AMICIZIE DI ENTRAMBE LE PARTI'''
#
#        # Repeating the Extraction if the previous is unacceptable
#        while gaus_num_friends<=0 or gaus_num_friends>glob.npeople :
#            gaus_num_friends = abs(int(glob.np.random.normal(2,2)))
#        
#        j_friends = [-3]*(glob.npeople)
#
#        # Does j-th Individual have already some Friends between the previous Individuals??
#        # If YES, add that one to the Friends' Links of j-th Individual
#        # Just to grant the Symmetry of the Matrix of Friends' Links
#        c = 0
#        for a in range(j) :
#            if is_there_equals(friends_matrix[a], j)==True :
#                j_friends[c] = a
#                c += 1
#        
#        if gaus_num_friends!=0 :  # forse inutile
#            k = 0
#            n = 0
#            possible_outcomes = [-3]*(glob.npeople-(j+1)) #vabene
#            while j_friends[gaus_num_friends-1]==-3 :
#                friend_id = glob.np.random.randint(j,glob.npeople)
#                if is_there_equals(possible_outcomes,friend_id)==False and n<len(possible_outcomes) :
#                    possible_outcomes[n] = friend_id
#                    n += 1
#
#                if possible_outcomes.count(-3)==0 :
#                    break
#                
#                if j_friends[k]!=-3 :
#                    if k == len(j_friends)-1: break
#                    else: k += 1
#                
#                if j_friends[k]==-3 and is_there_equals(j_friends,friend_id)==False and friend_id!=j : #evita doppioni  #tolto friend_id!=j migliora un po' #j_friends[k]==-3 si ptrebbe togliere con un elif invece di if
#                    j_friends[k] = friend_id
#                    if k == len(j_friends)-1: break
#                    else: k += 1
#                 
#        friends_matrix[j] = j_friends
#    return friends_matrix

# THIS IS OK ########################################################
# Function that returns x & y Coordinates of a Single Individual
# given its Index in the Ambient Array
def xydata(ambient, which) :

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
# Function that defines the Distance in this 2D Discrete Space
# with Periodic Conditions
def table_distance(ambient, first, second) :

    # Coordinates x & y of first
    xfirst, yfirst = xydata(ambient,first) 

    # Coordinates x & y of second
    xsecond, ysecond = xydata(ambient,second)

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
# Function that returns a String indicating where is second
# with respect to first
def where(ambient, first, second) :
    assert table_distance(ambient, first, second) == 1
    difference = first-second
    # possible differences:
    d1 = -1              #right
    d2 = +1              #left
    d3 = +glob.side           #down
    d4 = -glob.side           #up
    d5 = +glob.side-1         #right
    d6 = -glob.side+1         #left
    d7 = +glob.dimension-glob.side #up
    d8 = -glob.dimension+glob.side #down

    if difference==d1 : return 'right'
    if difference==d2 : return 'left'
    if difference==d3 : return 'down'
    if difference==d4 : return 'up'
    if difference==d5 : return 'right'
    if difference==d6 : return 'left'
    if difference==d7 : return 'up'
    if difference==d8 : return 'down'

# THIS IS OK ########################################################
# Function that returns an Array of Integers indicating the Position 
# of Empty Spaces around (which)-th Individual in the Ambient
# with Periodic Conditions
def empty_spaces(ambient, which) :

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
                if ambient[j]==-3 :
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
                if ambient[j]==-3 :
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
                if ambient[j]==-3 :
                    empty_spaces.append(j)
                    how_many += 1

    return empty_spaces

def empty_spaces_grav(ambient, which) :

    # Array filled with Indexes of Empty Spaces next to which
    spaces = []
    #probs = []
    how_many = 0

    # Left Burden Management
    if which%(glob.side)==0 :
        for j in [which-glob.side, which+glob.side-1, which+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]!=-3 :
                    spaces.append(-3)
                    #probs.append(0)
                if ambient[j]==-3 :
                    spaces.append(j)
                    #probs.append(1)
                    how_many += 1
    
    # Right Burden Management
    if (which+1)%(glob.side)==0 :
        for j in [which-glob.side, which-1, which-glob.side+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]!=-3 :
                    spaces.append(-3)
                    #probs.append(0)
                if ambient[j]==-3 :
                    spaces.append(j)
                    #probs.append(1)
                    how_many += 1
    
    # General Case & High-Low Burden Management
    if which%(glob.side)!=0 and (which+1)%(glob.side)!=0 :
        for j in [which-glob.side, which-1, which+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
            if j<0 :
                j = j+glob.dimension
            if j>=glob.dimension :
                j = j-glob.dimension
            if j>=0 and j<glob.dimension :
                if ambient[j]!=-3 :
                    spaces.append(-3)
                    #probs.append(0)
                if ambient[j]==-3 :
                    spaces.append(j)
                    #probs.append(1)
                    how_many += 1

    # correzione della predilezione degli individui di muoversi rispetto che a stare fermi
    #if probs.count(0)<4 and probs[4]!=0 :
    #    probs[4] = 0 
    #max_ = probs.count(1)
    #prob_ref = 1/max_
    #grav_attraction = gravity(ambient, which)
    #grav_x2 = grav_attraction[0]*grav_attraction[0]
    #grav_y2 = grav_attraction[1]*grav_attraction[1]
    #grav_modulus2 = grav_x2+grav_y2 

    #print('GRAVITY: ',grav_attraction[0],';',grav_attraction[1])
#
    #prob_up = 0   
    #prob_down = 0
    #prob_left = 0
    #prob_right = 0
#
    ##sotto,sinistra,destra,sopra,which
    #if grav_attraction[0]==0 and grav_attraction[1]==0 :
    #    prob_up    = 0.25
    #    prob_down  = 0.25
    #    prob_left  = 0.25
    #    prob_right = 0.25
    #if grav_attraction[0]>0 or (grav_attraction[0]==0 and grav_attraction[1]!=0) :
    #    prob_left = 0.25*(1-(grav_x2/grav_modulus2))
    #    prob_right = 0.25*(1+(grav_x2/grav_modulus2))
    #if grav_attraction[0]<0 : 
    #    prob_left = 0.25*(1+(grav_x2/grav_modulus2))
    #    prob_right = 0.25*(1-(grav_x2/grav_modulus2))
    #if grav_attraction[1]>0 or (grav_attraction[1]==0 and grav_attraction[0]!=0) :
    #    prob_up = 0.25*(1+(grav_y2/grav_modulus2))
    #    prob_down = 0.25*(1-(grav_y2/grav_modulus2)) 
    #if grav_attraction[1]<0 :
    #    prob_up = 0.25*(1-(grav_y2/grav_modulus2))   
    #    prob_down = 0.25*(1+(grav_y2/grav_modulus2))
    #rescaled_probs = [prob_down, prob_left, prob_right, prob_up]
#
    #if max_==4 :
    #    print('il numero è ', max_)
    #    for i in range(4) :
    #        probs[i] = rescaled_probs[i]
    #if max_==3 :
    #    print('il numero è ', max_)
    #    occupied = -1
    #    for i in range(4) :
    #        if spaces[i]==0 :
    #            occupied = i
    #            break
    #    missed_prob = rescaled_probs[occupied]
    #    probs[occupied] = 0
    #    for i in range(4) :
    #        if i!=occupied :
    #            probs[i] = rescaled_probs[i]+(1/max_)*missed_prob
    #if max_==2 :
    #    print('il numero è ', max_)
    #    occupied1 = -1
    #    occupied2 = -1
    #    for i in range(4) :
    #        if spaces[i]==0 and occupied1==-1 :
    #            occupied1 = i
    #        if spaces[i]==0 and i>occupied1 :
    #            occupied2 = i
    #            break
    #    missed_prob1 = rescaled_probs[occupied1]
    #    missed_prob2 = rescaled_probs[occupied2]
    #    probs[occupied1] = 0
    #    probs[occupied2] = 0
    #    for i in range(4) :
    #        if i!=occupied1 and i!=occupied2 :
    #            probs[i] = rescaled_probs[i]+((1/max_)*(missed_prob1+missed_prob2))
    #if max_==1 :
    #    print('il numero è ', max_)
    #    for i in range(4) :
    #        if probs[i]!=0 :
    #            probs[i] = 1  # dovrebbe già esserlo per costruzione
    #if max_==0 and how_many==1 :
    #    print('il numero è ', max_)
    #    probs[4] = 1
    #if max_==0 and how_many==0 :
    #    print('Shit, how tha fuck is this even possibleeeeeeeeeeeeeee? Explain me, Bazzani.')
#
    #print('PROBS: ',probs[0],probs[1],probs[2],probs[3],probs[4])
    ##assert probs[0]+probs[1]+probs[2]+probs[3]+probs[4] == 1

    return spaces

def empty_probs_grav(ambient, spaces, which) :

    # Array filled with Indexes of Empty Spaces next to which
    #spaces = []
    probs = []
    how_many = 0

    ## Left Burden Management
    #if which%(glob.side)==0 :
    #    for j in [which-glob.side, which+glob.side-1, which+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
    #        if j<0 :
    #            j = j+glob.dimension
    #        if j>=glob.dimension :
    #            j = j-glob.dimension
    #        if j>=0 and j<glob.dimension :
    #            if ambient[j]!=-3 :
    #                #spaces.append(0)
    #                probs.append(0)
    #            if ambient[j]==-3 :
    #                #spaces.append(j)
    #                probs.append(1)
    #                how_many += 1
    #
    ## Right Burden Management
    #if (which+1)%(glob.side)==0 :
    #    for j in [which-glob.side, which-1, which-glob.side+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
    #        if j<0 :
    #            j = j+glob.dimension
    #        if j>=glob.dimension :
    #            j = j-glob.dimension
    #        if j>=0 and j<glob.dimension :
    #            if ambient[j]!=-3 :
    #                #spaces.append(0)
    #                probs.append(0)
    #            if ambient[j]==-3 :
    #                #spaces.append(j)
    #                probs.append(1)
    #                how_many += 1
    #
    ## General Case & High-Low Burden Management
    #if which%(glob.side)!=0 and (which+1)%(glob.side)!=0 :
    #    for j in [which-glob.side, which-1, which+1, which+glob.side, which] : #sotto,sinistra,destra,sopra
    #        if j<0 :
    #            j = j+glob.dimension
    #        if j>=glob.dimension :
    #            j = j-glob.dimension
    #        if j>=0 and j<glob.dimension :
    #            if ambient[j]!=-3 :
    #                #spaces.append(0)
    #                probs.append(0)
    #            if ambient[j]==-3 :
    #                #spaces.append(j)
    #                probs.append(1)
    #                how_many += 1
    print('SPACES: ',spaces)
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
        prob_left = 0.25*(1-(grav_x2/grav_modulus2))
        prob_right = 0.25*(1+(grav_x2/grav_modulus2))
    if grav_attraction[0]<0 : 
        prob_left = 0.25*(1+(grav_x2/grav_modulus2))
        prob_right = 0.25*(1-(grav_x2/grav_modulus2))
    if grav_attraction[1]>0 or (grav_attraction[1]==0 and grav_attraction[0]!=0) :
        prob_up = 0.25*(1+(grav_y2/grav_modulus2))
        prob_down = 0.25*(1-(grav_y2/grav_modulus2)) 
    if grav_attraction[1]<0 :
        prob_up = 0.25*(1-(grav_y2/grav_modulus2))   
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

    print('PROBS: ',probs[0],probs[1],probs[2],probs[3],probs[4])
    print('SUM: ',probs[0]+probs[1]+probs[2]+probs[3]+probs[4])
    #assert probs[0]+probs[1]+probs[2]+probs[3]+probs[4] == 1

    return probs

# THIS IS OK #########################################################
# Funcion that defines the Friends' Influence on the (which)-th Individual
# depending on their Inclusion (or not) in his Influence Zone 
def influence_norm(ambient, which) :

    neighs = 0
    opinions = []
    for d in range(1, glob.distance+1) :
        for j in range(which-d*glob.side-glob.distance, which-d*glob.side+glob.distance+1) :
            if j!=which and j>=0 and j<glob.dimension :
                if ambient[j]!=-3 and table_distance(ambient,which,j)==d :
                    opinions.append(ambient[j])
                    neighs += 1
    #print(opinions)

    # Influence as the Mean Opinion
    sum_opinions = 0
    for i in range(len(opinions)) :
        sum_opinions += opinions[i]   # Each of their Opinion with same Weight
    influence = 0
    if neighs==0 :
        influence = ambient[which]  # No Changements of Opinion in Absence of Friends
    if neighs!=0 :
        influence = sum_opinions/neighs
    return influence

# WORK IN PROGRESS #########################################################
# Funcion that defines the Friends' Influence on the (which)-th Individual
# depending on their Inclusion (or not) in his Influence Zone 
def influence_vis(ambient, which) :
    viewed_people = partial_vision(ambient, which)
    opinions = []
    for j in range(len(viewed_people)) :
        opinions.append(ambient[viewed_people[j]])
                    
    # Influence as the Mean Opinion
    sum_opinions = 0
    for i in range(len(opinions)) :
        sum_opinions += opinions[i]   # Each of their Opinion with same Weight
    influence = ambient[which]
    if len(viewed_people)>0 :   
        influence = sum_opinions/len(viewed_people)
    
    return influence

# WORK IN PROGRESS ##################################################
# Function that features the One-Step Time Evolution of the Population
# on the Ambient for the 1° Scenario
def evolve_norm(initial) :

    final = [-3]*glob.dimension
    eff_changes = 0
    people = 0
    for i in range(glob.dimension) :
        
        if initial[i]!=-3 :
            people += 1
            # if people==glob.npeople : print('beneeeeeee')
            mean = influence_norm(initial, i)
            
            prob_change = glob.np.random.uniform(0,1)
            #A = 0.5*np.floor(3*glob.np.tanh(initial[i])+0.5)
            #B = 0.5*np.floor(glob.np.exp(-0.25*(initial[i]*initial[i]))+1.5)
            #B_2 = 0.5*np.floor(5*glob.np.exp(-3*(initial[i]*initial[i]))+1.5)
            #changed_opinion = np.floor(A+B*glob.np.tanh(B_2*mean+0.5*np.sign(initial[i]))+0.5)
            A = 0.5*glob.np.floor(3*glob.np.tanh(initial[i])+0.5)
            B = 0.5*glob.np.floor(-0.1*(initial[i]*initial[i])+1.5)
            B_2 = 0.5*glob.np.floor(5*glob.np.exp(-3*(initial[i]*initial[i]))+1.5)
            changed_opinion = glob.np.floor(A+B*glob.np.tanh(mean)+0.5)
            
            #print('x =',mean,', y =',changed_opinion,', s =',initial[i])
            empty_spacez = empty_spaces(final, i)
            how_many = len(empty_spacez)
            step_4dir = glob.np.random.randint(0,4)
            step_3dir = glob.np.random.randint(0,3)
            step_2dir = glob.np.random.randint(0,2)
            

            # Event of Opinion Change
            #if initial[i]==0 :
            #    print(glob.neutral_prob-(glob.neutral_prob-0.5)*abs(initial[i]))
            if prob_change<=glob.neutral_prob-(glob.neutral_prob-0.5)*abs(initial[i]) : #da cambiare (per ora)
                if changed_opinion!=initial[i] :
                    eff_changes += 1
                    print('There have been ', eff_changes, ' changements of opinion.')
                match how_many:
                    case 1:
                        final[empty_spacez[0]] = changed_opinion 
                
                    case 2:
                        if empty_spacez[1]!=i :
                            final[empty_spacez[step_2dir]] = changed_opinion
     
                        if empty_spacez[1]==i :
                            final[empty_spacez[0]] = changed_opinion
         
                    case 3:
                        if empty_spacez[2]!=i :
                            final[empty_spacez[step_3dir]] = changed_opinion
  
                        if empty_spacez[2]==i :
                            final[empty_spacez[step_2dir]] = changed_opinion

                    case 4:
                        if empty_spacez[3]!=i :
                            final[empty_spacez[step_4dir]] = changed_opinion

                        if empty_spacez[3]==i :
                            final[empty_spacez[step_3dir]] = changed_opinion

                    case 5:
                        final[empty_spacez[step_4dir]] = changed_opinion
            
            # Event of Same Opinion as Before
            if prob_change>glob.neutral_prob-(glob.neutral_prob-0.5)*abs(initial[i]) :  #di nuovo per ora
       
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
    print('\n\n')             
    return final

# WORK IN PROGRESS ##################################################
# Function that features the One-Step Time Evolution of the Population 
# on the Ambient for the 2° Scenario
def evolve_grav(initial) :

    final = [-3]*glob.dimension
    eff_changes = 0
    people = 0
    for i in range(glob.dimension) :
        
        if initial[i]!=-3 :
            people += 1
            # if people==glob.npeople : print('beneeeeeee')
            mean = influence_norm(initial, i)
            
            
            #A = 0.5*np.floor(3*glob.np.tanh(initial[i])+0.5)
            #B = 0.5*np.floor(glob.np.exp(-0.25*(initial[i]*initial[i]))+1.5)
            #B_2 = 0.5*np.floor(5*glob.np.exp(-3*(initial[i]*initial[i]))+1.5)
            #changed_opinion = np.floor(A+B*glob.np.tanh(B_2*mean+0.5*np.sign(initial[i]))+0.5)
            A = 0.5*glob.np.floor(3*glob.np.tanh(initial[i])+0.5)
            B = 0.5*glob.np.floor(-0.1*(initial[i]*initial[i])+1.5)
            B_2 = 0.5*glob.np.floor(5*glob.np.exp(-3*(initial[i]*initial[i]))+1.5)
            changed_opinion = glob.np.floor(A+B*glob.np.tanh(mean)+0.5)
            
            #print('x =',mean,', y =',changed_opinion,', s =',initial[i])
            spaces = empty_spaces_grav(final, i)
            print('WHO: ', i)
            print('SPACES: ',spaces)
            probs = empty_probs_grav(initial, spaces, i)
            step_4dir = glob.np.random.randint(0,4)
            step_3dir = glob.np.random.randint(0,3)
            step_2dir = glob.np.random.randint(0,2)

            # Event of Opinion Change
            prob_change = glob.np.random.uniform(0,1)
            if prob_change<=glob.neutral_prob-(glob.neutral_prob-0.5)*abs(initial[i]) : #da cambiare (per ora)
                if changed_opinion!=initial[i] :
                    eff_changes += 1
                    print('There have been ', eff_changes, ' changements of opinion.')
                #match how_many:
                #    case 1:
                final[glob.np.random.choice(spaces, p=probs)] = changed_opinion 
                
                #    case 2:
                #        if empty_spacez[1]!=i :
                #            final[empty_spacez[step_2dir]] = changed_opinion
     #
                #        if empty_spacez[1]==i :
                #            final[empty_spacez[0]] = changed_opinion
         #
                #    case 3:
                #        if empty_spacez[2]!=i :
                #            final[empty_spacez[step_3dir]] = changed_opinion
  #
                #        if empty_spacez[2]==i :
                #            final[empty_spacez[step_2dir]] = changed_opinion
#
                #    case 4:
                #        if empty_spacez[3]!=i :
                #            final[empty_spacez[step_4dir]] = changed_opinion
#
                #        if empty_spacez[3]==i :
                #            final[empty_spacez[step_3dir]] = changed_opinion
#
                #    case 5:
                #        final[empty_spacez[step_4dir]] = changed_opinion
            
            # Event of Same Opinion as Before
            if prob_change>glob.neutral_prob-(glob.neutral_prob-0.5)*abs(initial[i]) :  #di nuovo per ora
       
                #match how_many:
                #    case 1:
                final[glob.np.random.choice(spaces, p=probs)] = initial[i]

                    #case 2:
                    #    if empty_spacez[1]!=i :
                    #        final[empty_spacez[step_2dir]] = initial[i]
#
                    #    if empty_spacez[1]==i :
                    #        final[empty_spacez[0]] = initial[i]
 #
                    #case 3:
                    #    if empty_spacez[2]!=i :
                    #        final[empty_spacez[step_3dir]] = initial[i]
#
                    #    if empty_spacez[2]==i :
                    #        final[empty_spacez[step_2dir]] = initial[i]
#
                    #case 4:
                    #    if empty_spacez[3]!=i :
                    #        final[empty_spacez[step_4dir]] = initial[i]
#
                    #    if empty_spacez[3]==i :
                    #        final[empty_spacez[step_3dir]] = initial[i]
#
                    #case 5:
                    #    final[empty_spacez[step_4dir]] = initial[i] 
    print('\n\n')             
    return final

# WORK IN PROGRESS ##################################################
# Function that features the One-Step Time Evolution of the Population 
# on the Ambient of the 3° Scenario
def evolve_vis(initial) :

    final = [-3]*glob.dimension
    eff_changes = 0
    people = 0
    for i in range(glob.dimension) :
        
        if initial[i]!=-3 :
            people += 1
            # if people==glob.npeople : print('beneeeeeee')
            mean = influence_vis(initial, i)
            
            prob_change = glob.np.random.uniform(0,1)
            #A = 0.5*np.floor(3*glob.np.tanh(initial[i])+0.5)
            #B = 0.5*np.floor(glob.np.exp(-0.25*(initial[i]*initial[i]))+1.5)
            #B_2 = 0.5*np.floor(5*glob.np.exp(-3*(initial[i]*initial[i]))+1.5)
            #changed_opinion = np.floor(A+B*glob.np.tanh(B_2*mean+0.5*np.sign(initial[i]))+0.5)
            A = 0.5*glob.np.floor(3*glob.np.tanh(initial[i])+0.5)
            B = 0.5*glob.np.floor(-0.1*(initial[i]*initial[i])+1.5)
            B_2 = 0.5*glob.np.floor(5*glob.np.exp(-3*(initial[i]*initial[i]))+1.5)
            changed_opinion = glob.np.floor(A+B*glob.np.tanh(mean)+0.5)
            
            #print('x =',mean,', y =',changed_opinion,', s =',initial[i])
            step_4dir = glob.np.random.randint(0,4)
            step_3dir = glob.np.random.randint(0,3)
            step_2dir = glob.np.random.randint(0,2)
            empty_spacez = empty_spaces(final, i)
            how_many = len(empty_spacez)

            # Event of Opinion Change
            #if initial[i]==0 :
            #    print(glob.neutral_prob-(glob.neutral_prob-0.5)*abs(initial[i]))
            if prob_change<=glob.neutral_prob-(glob.neutral_prob-0.5)*abs(initial[i]) : #da cambiare (per ora)
                if changed_opinion!=initial[i] :
                    eff_changes += 1
                    print('There have been ', eff_changes, ' changements of opinion.')
                match how_many:
                    case 1:
                        final[empty_spacez[0]] = changed_opinion 
                
                    case 2:
                        if empty_spacez[1]!=i :
                            final[empty_spacez[step_2dir]] = changed_opinion
     
                        if empty_spacez[1]==i :
                            final[empty_spacez[0]] = changed_opinion
         
                    case 3:
                        if empty_spacez[2]!=i :
                            final[empty_spacez[step_3dir]] = changed_opinion
  
                        if empty_spacez[2]==i :
                            final[empty_spacez[step_2dir]] = changed_opinion

                    case 4:
                        if empty_spacez[3]!=i :
                            final[empty_spacez[step_4dir]] = changed_opinion

                        if empty_spacez[3]==i :
                            final[empty_spacez[step_3dir]] = changed_opinion

                    case 5:
                        final[empty_spacez[step_4dir]] = changed_opinion
            
            # Event of Same Opinion as Before
            if prob_change>glob.neutral_prob-(glob.neutral_prob-0.5)*abs(initial[i]) :  #di nuovo per ora
       
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
    print('\n\n')             
    return final

# THIS IS OK ########################################################
# Function that collects the X and Y Positions for each Individual with Opinion
# corresponding to color in Two different Arrays
def xydata_scatter(ambient, color) :
    which_color = 0
    if color=='empty' :
        which_color = -3
    if color=='red' :
        which_color = -2
    if color=='orange' :
        which_color = -1
    if color=='white' :
        which_color = 0
    if color=='cyan' :
        which_color = +1
    if color=='blue' :
        which_color = +2
    
    # Fullfilling of the Position Arrays for each Color
    xdata_color = []
    ydata_color = []
    j = -1
    for i in range(glob.dimension) :
        j += 1
        ydata = abs(int((i/glob.side)+1))
        xdata = abs(int(i+1-(ydata-1)*glob.side))
        if ambient[i]==which_color : 
            xdata_color.append(xdata)
            ydata_color.append(ydata)

    return xdata_color, ydata_color 

# THIS IS OK ########################################################
# Function that saves on CSV File the Info about the i-th Individual
def data_extr(array, i, fout, t):
    empty = 0
    orange = 0
    red = 0
    white = 0
    cyan = 0
    blue = 0
    opinion_class = ['empty','red','orange','white','cyan','blue']
    if array[i]==-3 :
        empty = i
        fout.write(f'{opinion_class[0]}, {array[i]}, {empty}, {t}\n')
    if array[i]==-2 : 
        red = i
        fout.write(f'{opinion_class[1]}, {array[i]}, {red}, {t}\n')
    if array[i]==-1 :
        orange = i
        fout.write(f'{opinion_class[2]}, {array[i]}, {orange}, {t}\n')
    if array[i]==0 :
        white = i
        fout.write(f'{opinion_class[1]}, {array[i]}, {white}, {t}\n')
    if array[i]==1 :
        cyan = i
        fout.write(f'{opinion_class[3]}, {array[i]}, {cyan}, {t}\n')
    if array[i]==2 :
        blue = i
        fout.write(f'{opinion_class[4]}, {array[i]}, {blue}, {t}\n')

# THIS IS OK ########################################################
# Function that makes possible to view the Animation
def update_scatter(time) : 
    glob.ax.clear()
    glob.plt.title('Agent-Based Cellular Automata Simulation')
    glob.ax.grid(False) #False to not show 
    xempties, yempties = xydata_scatter(glob.ambient_evolution[time], 'empty')
    xred, yred = xydata_scatter(glob.ambient_evolution[time], 'red')
    xorange, yorange = xydata_scatter(glob.ambient_evolution[time], 'orange')
    xwhite, ywhite = xydata_scatter(glob.ambient_evolution[time], 'white')
    xcyan, ycyan = xydata_scatter(glob.ambient_evolution[time], 'cyan')
    xblue, yblue = xydata_scatter(glob.ambient_evolution[time], 'blue')
    glob.ax.scatter(xempties, yempties, s=200-0.15*glob.dimension, c='w', label= 'Time Step '+ str(time), alpha=0, edgecolors='k')
    glob.ax.scatter(xred, yred, s=200-0.15*glob.dimension, c='tab:red', label='Estremisti -', edgecolors='k')
    glob.ax.scatter(xorange, yorange, s=200-0.15*glob.dimension, c='tab:orange', label='Moderati -', alpha=0.6, edgecolors='k')
    glob.ax.scatter(xwhite, ywhite, s=200-0.15*glob.dimension, c='black', label='Ignavi', alpha=0.4, edgecolors='k')
    glob.ax.scatter(xcyan, ycyan, s=200-0.15*glob.dimension, c='tab:cyan', label='Moderati +', alpha=0.6, edgecolors='k')
    glob.ax.scatter(xblue, yblue, s=200-0.15*glob.dimension, c='tab:blue', label='Estremisti +', edgecolors='k')
    glob.ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

# THIS IS OK ########################################################
# Function that saves on CSV File the Info about the Friends of the i-th Individual
# Delimiter is ; not , otherwise it can be confused with commas of Arrays' Elements
#def friend_extr(fmatrix, i, fout) :
#
#    list_nthfriend=[]
#    for j in range (0, glob.npeople-1) :
#        list_nthfriend.append(fmatrix[i][j])
#    fout.write(f'{i}; {list_nthfriend}\n')

# THIS IS OK ########################################################
# Function that return how many people with a certain opinion can be seen by a person with that opinion in his range of influence
def local_density(opinion, ambient, distance) : #provo a scrivere una funzione che calcola la densità locale di una certa opinione (utile per il flocking)
    
    grav_interaction = [] #densità, posizione
    
    for i in range(0, glob.dimension) : #scorro ambient ricercando persone con l'opinione desiderata
        density = 0 #si riparte a contare da zero tra un individuo e l'altro
        counter_left = 0 #potrebbe non servire a un caZZ0
        known_box = []
        density_index = []
        
        if ambient[i]==opinion :   #oppure solo ambient[i] se togliamo gli amici
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
                                    if ambient[d]==opinion :
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
                                    if ambient[u]==opinion :
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
                                if ambient[b]==opinion :
                                    density = density+1
                                    if b!=i and density_index.count(b)<1 :
                                        density_index.append(b)
                        
                        if known_box.count(r)==0 and r!=i and r>=0 :
                            if r<glob.dimension :
                                known_box.append(r)
                                if ambient[r]==opinion :
                                        density = density+1
                                        if r!=i and density_index.count(r)<1 :
                                            density_index.append(r)
                                
                            else :
                                r = r-glob.dimension
                                if known_box.count(r)==0 :
                                    known_box.append(r)
                                    if ambient[r]==opinion :
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
                                if ambient[a]==opinion :
                                    density = density+1
                                    if a!=i and density_index.count(a)<1 :
                                        density_index.append(a)
                        
                        if l!=i and l>=0 :
                            if l<glob.dimension :
                                counter_left = counter_left+1
                                if known_box.count(l)==0 :
                                    known_box.append(l)
                                    if ambient[l]==opinion :
                                        density = density+1
                                        if l!=i and density_index.count(l)<1 :
                                            density_index.append(l)
                                
                            else :
                                l = l-glob.dimension
                                if known_box.count(l)==0 :
                                    known_box.append(l)
                                    if ambient[l]==opinion :
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
                            if ambient[k]==opinion :
                                        density = density+1
                                        if k!=i and density_index.count(k)<1 :
                                            density_index.append(k)

            known_box.sort()
            #print(known_box)
            assert len(known_box) == (2*distance+1)*(2*distance+1)-1, print('sticazzi')#assertion to ensure that the area of range is a constant
            for g in range(0, len(known_box)) :
                assert known_box.count(g) <= 1, print('stocazzo')

            #print("Density:", density," at position ", i)
            grav_interaction.append([density, i, density_index])

    #print("Gravition: ", grav_interaction)
                    
    # bada bene che density non misura il numero di persone che ci sono in un certo spazio, ma è un parametro che quantifica il numero di persone (che hanno una certa
    # opinione) percepite da un certo individuo che ha quella stessa opinione. In pratica dice quante persone vede un dato individuo, infatti esclude se stesso. è ovvio
    # che se ho 4 persone tutte ammassate, density aumenta molto perchè ogni individuo dei 4 ne vede 3 (quindi density = 12) ed è evidente che non quantifica il numero di 
    # individui ma è solo un parametro di ammassamento
    return grav_interaction

#SEEMS TO BE OK, mi serve una funzione simile a table distance ma che restituisca la distanza di x e di y
def xy_distance(ambient, first, second) :
    
    #salvo le coordinate in un array
    xy1 = []
    xy1.append(xydata(ambient, first)[0])
    xy1.append(xydata(ambient, first)[1])
    
    xy2 = []
    xy2.append(xydata(ambient, second)[0])
    xy2.append(xydata(ambient, second)[1])

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

    opinion = ambient[which]
    grav_int = local_density(opinion, ambient, int((glob.side-1)/2)) #passo il range massimo per renderla non locale (campo medio)
    nth = 0
    gravitation_x = 0
    gravitation_y = 0
    force_x = 0
    force_y = 0

    #if opinion==-3 : return False
    assert opinion != -3
    for k in range(0, glob.dimension) :
        if ambient[k]==opinion :
            nth += 1
            if k==which : break

    #print (grav_int[nth-1]) #la persona alla posizione i sente una forza pari a density/pos?? dalle persone di density index
    
    for j in range(0, grav_int[nth-1][0]) :
    
        #assert len(grav_int[nth-1][2]) == numero di persone di una data opinione - 1
        # x[0] normale, x[1] periodico
        x = [xy_distance(ambient, which, grav_int[nth-1][2][j])[0][0], xy_distance(ambient, which, grav_int[nth-1][2][j])[1][0]]
        y = [xy_distance(ambient, which, grav_int[nth-1][2][j])[0][1], xy_distance(ambient, which, grav_int[nth-1][2][j])[1][1]]
        
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

def partial_vision(ambient, which) : #ritorna un array delle posizioni che vede un certo individuo
    
    opinion = ambient[which]
    grav_int = local_density(opinion, ambient, glob.distance)
    nth = 0 # mi darà la posizione ordinale della persona i all'interno dell'array grav_int
    choosen = []
    choice = -1 #inizializzato con un valore a caso
    old_choice = -1
    if opinion==-3 : return False
    for k in range(0, glob.dimension) :
        if ambient[k]==opinion :
            nth = nth+1
            if k==which : break
    #numero di persone che vengono viste nel proprio range
    vision = glob.np.random.randint(0, (2*glob.distance+1)*(2*glob.distance+1)-1)
    #(2*glob.distance+1)*(2*glob.distance+1)-1 è il massimo valore plossibile di amici, è un parametro ovviamente grande su cui andare a giocare
    if vision>=len(grav_int[nth-1][2]) : 
        return grav_int[nth-1][2] # lo lascia inalterato

    if vision<len(grav_int[nth-1][2]) :
        for j in range(0, vision) :
            choice = glob.np.random.choice(grav_int[nth-1][2])
            choosen.append(choice)
            while choosen.count(choice)>1 : #genero una scelta non doppione
                old_choice = choice
                choice = glob.np.random.choice(grav_int[nth-1][2])

            if old_choice!=-1 : choosen.append(choice) #aggiungo la nuova sccelta non doppione
            if old_choice!=-1 : choosen.remove(old_choice) #rimuovo la vecchia scelta che avevo già
            if old_choice!=-1 : assert choosen.count(old_choice) == 1 #mi assicuro che la vecchia scelta fosse un doppione

        return choosen
                
