# The Evolution of Picobot

# Khant, Aditiya
# Poon, Daphne
# Vendemiatti, Julia

import random

HEIGHT = 25 # outer height of the picobot board
INNERHEIGHT = 23 # inner height of the picobot board
WIDTH = 25 # outer width of the picobot board
INNERWIDTH = 23 # inner width of the picobot board
NUMSTATES = 5 # number of states a picobot program will have
CREAMOFTHECROP = .50 # how many picobot programs will move on to the next generation
MUTATERANGE = 4 # 1/6 of the first parents in the GA function will be mutated
TRIALS_FOR_GA = 20 # how many trials are used to evaluate a program's fitness in the GA function
STEPS_FOR_GA = 1200 # how many steps are used to evaluate a program's fitness in the GA function
WHITE = '\x1b[5;30;47m' + '  ' + '\x1b[0m' # prints a white square
GREEN = '\x1b[6;30;42m' + '  ' + '\x1b[0m' # prints a green square
BLUE = '\x1b[5;30;44m' + '  ' + '\x1b[0m' # pritns a blue square
YELLOW = '\x1b[5;30;43m' + '  ' + '\x1b[0m' # prints a yellow square

POSSIBLE_SURROUNDINGS = ['xxxx', 'Nxxx', 'NExx', 'NxWx' , 'xxxS' , 'xExS' ,'xxWS' , 'xExx', 'xxWx' ] # possible surroundings the picobot can encounter, edges, sides, and middle
POSSIBLE_MOVES = {} # possible moves the picobot can take -- we add stuff in this dictionary later
DIRECTIONS = ['N', 'S', 'E', 'W'] # directions the picobot can move in 

class  Program:
    """ represents a single Picobot program """
    def __init__(self):
        self.rules = {} # the rules of the program will be a dictionary
    
    def __repr__(self):
        """
        returns the picobot rules associated with an object of type Program
        """
        Keys = list( self.rules.keys() ) # gets the keys of the rules of a picobot program and puts them in a list
        SortedKeys = sorted( Keys )   # sorts the list of keys so that current state will be from 0 to numstates
        s = "" # starter string
        for x in SortedKeys:
            s += str(x[0]) + " " + str(x[1]) + " -> " + str(self.rules[x][0]) + " " + str(self.rules[x][1]) +"\n" # add the rules to the string
        return s # return the list of rules as a string

    def randomize(self):
        """
        Takes in an object of type Program and returns a randomized set of rules
        for that picobot program. It covers all the states in the number of states
        and all of the possible surroundings in each state.
        """
        for i in range(NUMSTATES): # for each possible state
            for j in POSSIBLE_SURROUNDINGS: # for each possible surrounding
                currentState = i 
                currentPosition = j
                nextDirection = random.choice(DIRECTIONS) # choose a random direction to travel to
                while nextDirection in currentPosition: # while there's a wall in the next direction, pick a different direction to go to
                    nextDirection = random.choice(DIRECTIONS)
                nextState = random.choice(range(NUMSTATES))  # go to a random next state
                self.rules[(currentState, currentPosition)] = (nextDirection, nextState) # add the rule to self.rules

    def getMove(self, state, surroundings):
        """
        Takes in an object of class Program, an integer state, and sorroundings.abs
        Returns the move in the rules corresponding to that state/sorrounding.
        """
        return self.rules[ (state, surroundings) ]


    def mutate(self):
        """
        Takes in an object of class Program and changes the move corresponding
        to a single state/surrounding.
        """
        random_key = random.choice(list(self.rules.keys())) # picks a random key to mutate the rules of
        random_rule = self.rules[random_key] # the rule of the random key that was chosen 
        current_surroundings = random_key[1] # the current surrounding of the picobot
        new_rule = random_rule # sets the new rule equal to the random rule in preparation for the while loop
        possible_moves = [] # by the end of the if statements this will be a list of all the possible moves given the current surroundings
        if current_surroundings[0] == 'x':
            possible_moves+= 'N'
        if current_surroundings[1] == 'x':
            possible_moves+= 'E'
        if current_surroundings[2] == 'x':
            possible_moves+= 'W'
        if current_surroundings[3] == 'x':
            possible_moves+= 'S'
        while random_rule == new_rule: # will keep running until the rule is mutated unless the if statement is true
            new_move = random.choice(possible_moves) # pick a new random direction
            new_state = random.choice(range(NUMSTATES)) # pick a new random state
            new_rule = (new_move,new_state)
        self.rules[random_key] = (new_rule)
        

    def crossover(self, other):
        """
        Takes in two objects of class Program and returns a mix the picobot rules of each.
        The rules in each state of the new program still must cover the 8 possible surroundings.
        """
        crossover_state = random.choice(range(1,NUMSTATES-1)) # picks a random state that is going to be the point where parent 1 and parent 2 cross 
        offspring = Program() # creates a new object of type Program for offspring
        self_keys = list(self.rules.keys()) # gets the keys from one of the parents
        other_keys = list(other.rules.keys()) # gets the keys from the other parent
        for e in self_keys: # for each of one of the parents keys
            if e[0]<= crossover_state: # if the state is less than or equal to the crossover state
                offspring.rules[e] = self.rules[e] # then the offspring's rules will be the same as that parent's for that key
        for e in other_keys: # for each key of the other parent
            if e[0] > crossover_state: # if the state of the key is greater than the crossover state
                offspring.rules[e] = other.rules[e] # then the offspring's rules for that key will be the same as that paren'ts
        return offspring  # returns the offspring program


    def __gt__(self,other):
            """ greater than operator - works randomly, but works! """
            return random.choice( [ True, False ] )

    def __lt__(self,other):
            """ less than operator - works randomly, but works! """
            return random.choice( [ True, False ] )

class World:
    """ represents a single Picobot WORLD! """
    def __init__(self, initial_row, initial_col, program):
        self.prow = initial_row # picobot row is the initial row 
        self.pcol = initial_col # picobot colum is the initial column
        self.state = 0 # initial state is 0
        self.program = program # the program is the given program
        #all cells are white!!!!
        self.room = [ [WHITE]*WIDTH for row in range(HEIGHT) ] 
        #sets picobot cell as green
        self.room[self.prow][self.pcol] = GREEN
        #sets top and bottom blue walls (these won't change)
        for col in range(WIDTH):
            self.room[0][col] = BLUE
            self.room[24][col] = BLUE
        #makes left and right walls
        for row in range(1,(HEIGHT)):
            self.room[row][0] = BLUE
            self.room[row][24] = BLUE
        
        
    def __repr__(self):
        """ prints the data
        """
        s = ''   # the string to return
        # prints the colors
        for row in range(0,HEIGHT):
            for col in range(0,WIDTH):
                s += self.room[row][col]
            s += '\n'
        return s       # the board is complete, return it
    
    def getCurrentSurroundings(self):
        """Returns the wall surroundings
        """
        surround = ""
        row = self.prow
        col = self.pcol
        # if there is a wall to the North
        if self.room[row-1][col] == BLUE: 
            surround += "N"
        else:
            surround += "x"
        # if there is a wall to the East
        if self.room[row][col+1] == BLUE: 
            surround += "E"
        else:
            surround += "x"
        # if there is a wall to the West
        if self.room[row][col-1] == BLUE: 
            surround += "W"
        else:
            surround += "x"
        # if there is a wall to the South
        if self.room[row+1][col] == BLUE: 
            surround += "S"
        else:
            surround += "x"
        return surround
        
    def step(self):
        """
        Takes in an object of class World and moves the picobot one step
        according to the picobot program. Does not return anything.
        """
        current_surroundings = self.getCurrentSurroundings() # gets the current surroundings
        next_move = self.program.rules[self.state, current_surroundings] # determines what the next move is based on the state and hte current surroundings
        room = self.room # gets what the current room is
        self.room[self.prow][self.pcol] = YELLOW # makes the picobots current position yellow
        self.state = next_move[1] # sets the picobots state as the next state
        # depending on what the next move direction is, moves the picobots row or column
        if next_move[0] == 'N': 
            self.prow -= 1
        elif next_move[0] == 'S':
            self.prow += 1
        elif next_move[0] == 'W':
            self.pcol -= 1
        elif next_move[0] == 'E':
            self.pcol += 1
        self.room[self.prow][self.pcol] = GREEN # sets the picobots new position as green
            

    def run(self, steps):
        """ runs a certain number of steps
        """
        for x in range(steps): # for the number of steps
            self.step() # run a step
    
    def fractionVisitedCells(self):
        """ calculates and returns how many unique cells have already been visited
        """
        counter = 0 # sets the counter to 0 in preparation for the for loop
        row = self.prow
        col = self.pcol
        for row in range(0,HEIGHT): # for each row
            for col in range(0,WIDTH): # for each column
                if self.room[row][col] == YELLOW or self.room[row][col] == GREEN : #if it is yellow(visited) or green (currently there)
                    counter += 1 # add one to the counter
        return float(counter/(INNERHEIGHT*INNERWIDTH)) # counter divided by total possible

## following programs are outside of class World

def returnPop(popsize):
    """takes as input a population size and returns a population (a Python list) of that many random Picobot programs.
    """
    p=Program() # make p an object of type program
    LC = [] #start with an empty list
    for i in range(popsize):
        p.randomize() # makes a random program
        LC += [p] # adds it to the list of programs
    return LC # return the list of random programs


def evaluateFitness(program, trials, steps):
    """ takes as input a Picobot program, a positive integer trials that indicates the number  
        of random starting points that are to be tested, and a positive integer steps that 
        indicates how many steps of the simulation each trial should be allowed to take. The 
        function returns a fitness (a floating point number between 0.0 and 1.0) that is the 
        fraction of the cells visited by this Picobot program, averaged over the given number 
        of trials
    """
    p = program 
    List  = []
        
    for i in range(trials):
        w = World(random.choice(range(1,INNERHEIGHT)),random.choice(range(1, INNERWIDTH)),p)
        w.run(steps)
        List += [w.fractionVisitedCells()]

    return sum(List)/trials

def GA(popsize, numgens):
    """The genetic algorithm
    """
    programs = returnPop(popsize)
    Lofitness = []

   
    for i in range(numgens): # for each generation
        for j in range(popsize): # for each member of the population
            Lofitness += [(evaluateFitness(programs[j], TRIALS_FOR_GA, STEPS_FOR_GA),programs[j])] # makes a list of tuples with the evaluated fitness of each program and the program
        SL = sorted(Lofitness) # sort by evaluated fitness
        NL = SL[int(CREAMOFTHECROP*popsize): ] # choose only the best programs for the next parents
        bestprogram = max(SL)
        saveToFile("generation"+str(i)+".txt", bestprogram)
        #finding average of the generation
        s = 0
        for e in SL:
            s+=e[0] #sum each fitness
        average = s/popsize #divide by number of programs
        print("Generation", i)
        print("Average fitness is", average)
        print("Best fitness is", bestprogram[0], "\n\n")

        #makes the next population
        for z in range(popsize): 
            parent1 = random.choice(NL)[1]
            parent2 = random.choice(NL)[1]
            if random.choice(range(MUTATERANGE)) == 0:
                parent1.mutate()
            offspring = parent1.crossover(parent2)
            programs[z] = offspring
        Lofitness = []

        # print("gen", str(i), " done")
        # # print("Average Fitness: ", str(Average))
        # print("Best fitness: ",str(Best))
        # filename = "gen" + str(i)+".txt"
        # saveToFile(filename , bestprogram)
    # bestprogram = max(SL)[1]
    # return bestprogram


def saveToFile( filename, p ):
   """ saves the data from Program p
       to a file named filename """
   f = open( filename, "w" )
   print(p, file=f)        # prints Picobot program from __repr__
   f.close()
