from random import randint, random
import threading
import time

import MancalaBoard
import slv398


def sortPlayers(players):
    print 'NEW ROUND'
    gamesWon = [0]*len(players)
    for p1 in range(len(players)):
        for p2 in range(len(players)):
            if p1 == p2:
                continue
            player_1 = slv398.slv398(1, slv398.Player.CUSTOM, 7, players[p1][:14], players[p1][14:])
            player_2 = slv398.slv398(2, slv398.Player.CUSTOM, 7, players[p2][:14], players[p2][14:])
            print time.strftime('%H:%M:%S')+': Starting', p1, 'v', p2
            # threading.Thread(target=runGame, args=(player_1, p1, player_2, p2, gamesWon)).start()
            runGame(player_1, p1, player_2, p2, gamesWon)
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    return sorted(zip(gamesWon, players), reverse=True)


def runGame(player_1, p1, player_2, p2, gamesWon):
    game = MancalaBoard.MancalaBoard()
    winner = game.hostGame(player_1, player_2)
    gamesWon[p1] += winner[0]
    gamesWon[p2] += winner[1]
    print time.strftime('%H:%M:%S')+': Finished', p1, 'v', p2


def evolve(pop, i_min, i_max, pop_size, retain=0.3, random_select=0.05, mutate=0.2):

    # If input population is skimpy, start with some crossover
    if len(pop) < pop_size:
        addChildren(pop, pop_size, mutate, i_min, i_max)

    sortedPlayers = sortPlayers(pop)
    graded = [item[1] for item in sortedPlayers]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]
    save(sortedPlayers)

    # randomly add other individuals to promote genetic diversity
    for i in graded[retain_length:]:
        if random_select > random():
            parents.append(i)

    # crossover and mutate
    addChildren(parents, pop_size, mutate, i_min, i_max)

    return parents


def addChildren(parents, pop_size, mutate, i_min, i_max):
    # crossover parents to create children
    parents_length = len(parents)
    desired_length = pop_size - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        if male != female:
            male = parents[male]
            female = parents[female]
            child = []
            for i in range(len(male)):
                if mutate > random():
                    child.append(randint(i_min, i_max))
                else:
                    weight = random()
                    child.append(weight*male[i]+(1-weight)*female[i])
            children.append(child)
    parents.extend(children)


def save(sortedPlayers):
    with open('genetic_history.txt', 'a') as f:
        f.write(time.strftime('%H:%M:%S')+'\n')
        for m in sortedPlayers:
            line = str(m[0]).rjust(3, ' ')+':  ['+', '.join([str(int(item)).zfill(2) for item in m[1]])+']'
            f.write(line+'\n')
        f.write('\n')


def main():
    p = [
        [86, 70, 32, 59, 28, 31, 72, 70, 46, 31, 92, 76, 77, 86, 78, 34, 30, 61, 57, 59, 84, 70, 59, 17, 41, 49, 43, 54],
        [96, 73, 33, 59, 21, 30, 93, 75, 63, 31, 90, 71, 77, 74, 51, 47, 19, 39, 56, 67, 85, 73, 58, 40, 21, 76, 43, 54],
        [85, 75, 37, 63, 25, 30, 71, 75, 64, 27, 79, 39, 85, 31, 16, 49, 19, 46, 55, 67, 56, 73, 58, 19, 27, 61, 43, 53],
        [78, 34, 30, 61, 57, 59, 84, 70, 59, 17, 41, 49, 43, 54, 86, 70, 32, 59, 28, 31, 72, 70, 46, 31, 92, 76, 77, 86],
        [70, 46, 31, 92, 76, 77, 86, 86, 70, 32, 59, 28, 31, 72, 70, 59, 17, 41, 49, 43, 54, 78, 34, 30, 61, 57, 59, 84],
        [75, 63, 31, 90, 71, 77, 74, 96, 73, 33, 59, 21, 30, 93, 73, 58, 40, 21, 76, 43, 54, 51, 47, 19, 39, 56, 67, 85]
    ]
    i_min = 0
    i_max = 99
    while True:
        p = evolve(p, i_min, i_max, 10)


if __name__ == '__main__':
    main()