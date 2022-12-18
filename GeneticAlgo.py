from collections import defaultdict
from heapq import nlargest
import time
import random
import numpy as np
from Graph_Creator import *

#producePopulation completed for part a
def producePopulation(popsize):
    colours = ("R", "G", "B")
    population = list()
    individual = list()
    for x in range(popsize):
        for y in range(50):
            individual += random.choice(colours)
        population.append(individual.copy())
        individual.clear()
    return population

#reproduce completed for part a
def reproduce(parent1, parent2):
    c = random.randint(0,50)
    child1 = list()
    child2 = list()
    for x in range(50):
        if(random.random() <= 0.08):
            child1 += parent1[0][x]
            child2 += parent2[0][x]
        else:
            child1 += parent2[0][x]
            child2 += parent1[0][x]
    return [child1, child2]

#mutate completed for part a
def mutate(child, adjlist):
    badness = list()
    count = 0
    for x in range(50):
        for y in range(len(adjlist[x])):
            if(child[x] == child[adjlist[x][y]]):
                count += 1
        badness.append(count)
        count = 0
    colours = {"R", "G", "B"}
    ind = random.choices(range(50), weights= [badness[x] + len(adjlist[x]) + 1 for x in range(50)], k = 1)
    ind = ind[0]
    colours.remove(child[ind])
    if(badness[ind] > len(adjlist)//2):
        child[ind] = random.choice(tuple(colours))
    else:
        for x in adjlist[ind]:
            if(child[x] == child[ind]):
                child[x] = random.choice(tuple(colours))
    return child

#fitness function completed.
def fitfunc(adj, alloc): 
    unfit_nodes = set()
    for x in range(50):
        for y in range(len(adj[x])):
            if(alloc[x] == alloc[adj[x][y]]):
                unfit_nodes.add(x)
                unfit_nodes.add(adj[x][y])
    val = 50 - len(unfit_nodes)
    return val

def main():
    t_start = time.time()
    gc = Graph_Creator()

#    ********* You can use the following two functions in your program

    edges = gc.CreateGraphWithRandomEdges(300) # Creates a random graph with 50 vertices and 200 edges
    # edges = gc.ReadGraphfromCSVfile("200") # Reads the edges of the graph from a given CSV file
    # print(len(edges))
    # print()
    # create an adjacency list to help simplify process
#    **********
#    Write your code for find the optimum state for the edges in test_case.csv file using Genetic algorithm
    adjlist = defaultdict(list)
    for x in edges:
        adjlist[x[0]].append(x[1])

    pop_size = 100
    generations = 50
    population = list()
    children = list()
    generation_best = list()

    temp = producePopulation(pop_size)

    # created the first population
    for x in temp:
        population.append([x, fitfunc(adjlist, x)])
    
    gen_no = 0
    # max_fit = 0
    stall_cnt = 0
    t_elapsed = time.time() - t_start
    t_end = time.time() + (44.8 - t_elapsed)
    while time.time() < t_end:
        gen_no += 1
        if(stall_cnt != 0 and stall_cnt % 50 == 0):
            npopulation = nlargest(10, population, key = lambda tup: tup[1])
            temp = producePopulation(40)
            for x in range(10):
                individual = npopulation[x]
                best = individual
                var1 = individual[0]
                var2 = individual[0]
                for z in range(50):
                    colours = {"R", "G", "B"}
                    colours.remove(individual[0][z])
                    var1[z] = random.choice(tuple(colours))
                    colours.remove(var1[z]) 
                    var2[z] = random.choice(tuple(colours))
                    var1_fit = fitfunc(adjlist, var1)
                    var2_fit = fitfunc(adjlist, var2)
                    if (var1_fit >= individual[1]):
                        best = [var1, var1_fit]
                    if (var2_fit >= individual[1]):
                        best = [var2, var2_fit]
                individual = best
                npopulation[x] = individual
        else:
            npopulation = nlargest(25, population, key = lambda tup: tup[1])
            temp = producePopulation(25)
        population = npopulation
        for x in temp:
            population.append([x, fitfunc(adjlist, x)])

        for x in range(50):
            parents = random.choices(population, weights = [1 for c in range(50)], k = 2)
            child = reproduce(parents[0], parents[1])
            if(random.random() < 0.1):
                mutate(child[random.randint(0,1)], adjlist)
            children.append([child[0], fitfunc(adjlist, child[0])])
            children.append([child[1], fitfunc(adjlist, child[1])])
        population = population + children
        if(len(generation_best) > 2 and generation_best[-1] > generation_best[-2]):
            stall_cnt = 0
        else:
            stall_cnt += 1
        generation_best.append(max(individual[1] for individual in population))
        if(generation_best[-1] == 50):
            break
        children.clear()
    best = nlargest(1, population, key = lambda tup: tup[1])

    print("Roll no : 2020A7PS1223G")
    print("Number of edges : {}".format(len(edges)))
    print("Best state :")
    for x in range(50):
        print("{}:{}".format(x, best[0][0][x]), end=", " if x < 49 else " ")
    print("\nFitness value of best state : {}".format(max(individual[1] for individual in population)))
    print("Time taken: {} seconds".format(time.time() - t_start))
    # print(population)



if __name__=='__main__':
    main()