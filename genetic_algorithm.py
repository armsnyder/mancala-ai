from random import randint, random
import threading
import time

import MancalaBoard
import slv398


def sortPlayers(players):
    print 'NEW ROUND'
    gamesWon = [0]*len(players)
    for p1 in range(len(players)):
        for p2 in range(p1+1, len(players)):
            player_1 = slv398.slv398(1, slv398.Player.ABPRUNE, 6, players[p1])
            player_2 = slv398.slv398(2, slv398.Player.ABPRUNE, 6, players[p2])
            print time.strftime('%H:%M:%S')+': Starting', p1, 'v', p2
            threading.Thread(target=runGame, args=(player_1, p1, player_2, p2, gamesWon)).start()
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    return sorted(zip(gamesWon, players), reverse=True)


def runGame(player_1, p1, player_2, p2, gamesWon):
    game = MancalaBoard.MancalaBoard()
    winner = game.hostGame(player_1, player_2)
    if winner == 1:
        gamesWon[p1] += 1
    # elif winner == 2:
    #     gamesWon[p2] += 1
    # else:
    #     gamesWon[p1] += 0.5
    #     gamesWon[p2] += 0.5
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
            line = str(round(m[0], 1)).rjust(4, ' ')+':  ['+', '.join([str(int(item)).zfill(2) for item in m[1]])+']'
            f.write(line+'\n')
        f.write('\n')


def main():
    p = [
        [90, 33, 16, 97, 24, 47, 8, 65, 28, 64, 67, 23, 69, 32],
        [99, 48, 12, 49, 65, 43, 46, 97, 66, 43, 47, 69, 52, 45],
        [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    ]
    i_min = 0
    i_max = 99
    while True:
        p = evolve(p, i_min, i_max, 10)


if __name__ == '__main__':
    main()