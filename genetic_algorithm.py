"""
# Example usage
from genetic import *
target = 371
p_count = 100
i_length = 6
i_min = 0
i_max = 100
p = population(p_count, i_length, i_min, i_max)
fitness_history = [grade(p, target),]
for i in xrange(100):
    p = evolve(p, target)
    fitness_history.append(grade(p, target))

for datum in fitness_history:
   print datum
"""
from random import randint, random
from operator import add

import MancalaBoard
import Player


def individual(length, min, max):
    """Create a member of the population."""
    return [randint(min, max) for x in xrange(length)]


def population(count, length, min, max):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the minimum possible value in an individual's list of values
    max: the maximum possible value in an individual's list of values

    """
    return [individual(length, min, max) for x in xrange(count)]


def sortPlayers(players):
    gamesWon = [0]*len(players)
    for p1 in range(len(players)):
        for p2 in range(p1+1, len(players)):
            game = MancalaBoard.MancalaBoard()
            player_1 = Player.MancalaPlayer(1, Player.Player.ABPRUNE, 6, players[p1])
            player_2 = Player.MancalaPlayer(2, Player.Player.ABPRUNE, 6, players[p2])
            winner = game.hostGame(player_1, player_2)
            if winner == 1:
                gamesWon[p1] += 1
            elif winner == 2:
                gamesWon[p2] += 1
            else:
                gamesWon[p1] += 0.5
                gamesWon[p2] += 0.5
    return [item[1] for item in sorted(zip(gamesWon, players), reverse=True)]


def evolve(pop, i_min, i_max, retain=0.3, random_select=0.05, mutate=0.1):
    graded = sortPlayers(pop)
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]
    save2(graded)

    # randomly add other individuals to promote genetic diversity
    for i in graded[retain_length:]:
        if random_select > random():
            parents.append(i)

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            child = []
            for i in range(len(male)):
                weight = random()
                child.append(weight*male[i]+(1-weight)*female[i])
            children.append(child)
    parents.extend(children)

    # mutate some individuals
    mutated_parents = []
    for i in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(i)-1)
            i[pos_to_mutate] = randint(i_min, i_max)
        mutated_parents.append(i)

    return mutated_parents


def save(parent):
    max_amount = max([abs(item) for item in parent])
    with open('genetic_history.txt', 'a') as f:
            f.write(str([int(item*100/max_amount) for item in parent])+'\n')


def save2(graded):
    total = str(len(graded))
    with open('genetic_history.txt', 'a') as f:
        for m in graded:
            line = str(m[0])+'/'+total+': '+str(m[1])
            f.write(line+'\n')
        f.write('\n')


def main():
    initial_pop = [
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    ]
    pop_num = 8
    i_length = 16
    i_min = -100
    i_max = 100
    evolutions = 10000
    # p = population(pop_num, i_length, i_min, i_max)
    p = initial_pop
    for i in xrange(evolutions):
        p = evolve(p, i_min, i_max)
        if i == evolutions-1:
            p = evolve(p, i_min, i_max, mutate=0)
            p = evolve(p, i_min, i_max, mutate=0)


if __name__ == '__main__':
    main()