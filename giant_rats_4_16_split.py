# This is a project using genetic algorithms to simulate breeding rats to a size
# of over 100 lbs

# Import packages
import  time # Record run time of algorythm
import random # for stochastic needs of algorythm
import statistics # get the mean values of the runs

# INITIALIZE STARTING CONSTANTS FOR PROGRAMME CONSTANTS ARE UPPER CASE
GOAL = 5000
NUM_RATS = 20
INITIAL_MIN_WT = 200
INITIAL_MAX_WT = 600
INITIAL_MODE_WT = 300
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
LITTER_SIZE = 8
LITTERS_PER_YEAR = 10
GENERATION_LIMIT = 500

# MAKE SURE THERE ARE ALWAYS AN EVEN NUMBER OF RATS FOR BREEDING
if NUM_RATS % 2 != 0:
    NUM_RATS += 1

# INITIALIZE THE RAT POPULATION
## 4 arguments in the function to define the rats used by Random module
## triangular dist used to control min/max weight and model skewness
def populate(num_rats, min_wt, max_wt, mode_wt):
    return [int(random.triangular(min_wt, max_wt, mode_wt)) \
            for i in range(num_rats)]

# DEFINE THE FITNESS AND SELECTION FUNCTIONS TO ASSESS MEASUREMENT OF POPULATION
## this function uses the statistical mean to judge when the ave wt = goal wt
def fitness(population, goal):
    ave = statistics.mean(population)
    return  ave / goal

 # male - female 4-16 split

def select(population, to_retain):
    # Sort the entire population
    sorted_population = sorted(population)

    # Split the population into two equal halves
    members_per_sex = len(sorted_population) // 2
    to_retain_by_sex = to_retain//2

    males = sorted_population[members_per_sex:]
    females = sorted_population[:members_per_sex]

    # Select the top 4 males from the top half
    selected_males = males[-4:]

    # Select the top 16 females from the bottom half
    selected_females = females[-16:]

    return selected_males, selected_females


# This function generates the next generation
# The assumption is that offspring weight is between/equal to mother and father
# The males and females are shuffled so any size male can breed with any size female

def breed(males, females, litter_size):
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        for child in range(litter_size):
            child = random.randint(female, male)
            children.append(child)
    return children

# Mutation function to recognize probability of runts and supersizes
# take the list of children and loop through list of children applying mutation
# scalars to each using enumerate to generate an index
# if the mutation odds are greater than the randomly generated value 0-1 that index
# is mutated and apply the mutation scalar

def mutate(children, mutate_odds, mutate_min, mutate_max):
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))
    return children

# This is the main function
# First initialize the population and go through cycles and display results
def main():
    generations = 0
    parents = populate(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT)
    print('Initial population weights = {}'.format(parents))
    popl_fitness = fitness(parents, GOAL)
    print('Initial population fitness = {}'.format(popl_fitness))
    print('Number to retain = {}'.format(NUM_RATS))

    ave_wt = []  # list to hold a list of rat weights through generations

    # The while loop starts generations with stop at weight or max gens
    # Add children to parents to make new list
    # print the fitness of each generation and print results of generation
    while popl_fitness < 1 and generations < GENERATION_LIMIT:
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_males + selected_females + children
        popl_fitness = fitness(parents, GOAL)
        print('Generation {} fitness = {:.4f}'.format(generations, popl_fitness))
        ave_wt.append((int(statistics.mean(parents))))
        generations += 1

    print('Average weight per generation = {}'.format(ave_wt))
    print('\nNumber of generations = {}'.format(generations))
    print('number of years = {}'.format(int(generations / LITTERS_PER_YEAR)))


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print('\nRuntime for this program was {} seconds.'.format(duration))