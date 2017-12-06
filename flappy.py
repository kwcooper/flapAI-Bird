from itertools import cycle
import random
import sys
from copy import deepcopy
import csv

import pygame
from pygame.locals import *
import math
#import networkx as nx

from bird import Bird
from neural import Net


FPS = 55
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PIPEGAPSIZE  = 105 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79 # amount by which base can maximum shift to left
PIPEDETERMINTISIC = False
DISPLAYSCREEN = True
SOUNDS = False
DISPLAYWELCOME = True
GAMEOVERSCREEN = False
NUMBERBIRDS = 10
FIRST = True
PRINT = False #k added optional print to the mainGame function for speedup 

HIGHSCORE = 0
GENERATION = 0

# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)


try:
    xrange
except NameError:
    xrange = range

# main function to run game
def main():
    global SCREEN, FPSCLOCK, PAUSE
    pygame.init()
    PAUSE = False;
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    IMAGES['generation'] = pygame.image.load('assets/sprites/gene3.png').convert_alpha()
    IMAGES['high'] = pygame.image.load('assets/sprites/high.png').convert_alpha()
    IMAGES['high'] = pygame.transform.scale(IMAGES['high'], (165, 40))
    IMAGES['generation'] = pygame.transform.scale(IMAGES['generation'], (160, 37))

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()

    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)
    birds = {}
    highscore = 0
    generation = 0
    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        for i in range(NUMBERBIRDS):
            randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
            IMAGES['Bird '+str(i)] = (
                pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
                pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
            )
        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.rotate(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), 180),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hitmask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        for i in range(NUMBERBIRDS):
            HITMASKS['Bird '+str(i)] = (
                getHitmask(IMAGES['Bird '+str(i)][0]),
                getHitmask(IMAGES['Bird '+str(i)][1]),
                getHitmask(IMAGES['Bird '+str(i)][2]),
            )
#5787
#6649
            
        movementInfo = showWelcomeAnimation()
        birds_m, highscore = mainGame(movementInfo, birds, highscore, generation, PRINT)
        birds = showGameOverScreen(birds_m)
        generation += 1
        



def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    birdIndex = 0
    # Cycles the birds wings
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['Bird '+str(birdIndex)][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 2, 'dir': 1}

    while True:
        if DISPLAYSCREEN:
            SOUNDS['wing'].play()
            return {
                'playery': playery + playerShmVals['val'],
                'basex': 80,
                'playerIndexGen': playerIndexGen,
            }
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)):
                # make first flap sound and return values for mainGame
                #SOUNDS['wing'].play()
                return {
                    'playery': playery,
                    'basex': 80,
                    'playerIndexGen': playerIndexGen,
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            birdIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['Bird ' + str(0)][birdIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def pause():
    PAUSE = True

    while PAUSE:
        for event in pygame.event.get():
            if event.type == KEYDOWN and (event.key == K_p):
                PAUSE = False

    
def mainGame(movementInfo, birds, highscore, generation, PRINT):
    score = birdIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    initx, inity = int(SCREENWIDTH * 0.2), int(SCREENHEIGHT *.4)
    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH/2 +50, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH/2 +50+ (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH/2+50, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH/2+50 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]
    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    initVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    initMaxVelY =  10   # max vel along Y, max descend speed
    initMinVelY =  -8   # min vel along Y, max ascend speed
    initAccY    =   1   # players downward accleration
    initRot     =  45   # player's rotation
    initVelRot  =   3   # angular speed
    initRotThr  =  20   # rotation threshold
    initFlapAcc =  -9   # players speed on flapping
    birdFlapped = False # True when player flaps
    birdHeight = IMAGES['Bird 0'][0].get_height()
    crashedBirds = 0    # Number of birds crashed so far
    if len(birds) == 0:
        birds = generateBirds({}, {}, FIRST, initx, inity, birdIndex, initVelY,initAccY,initRot)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                for bird in birds:
                    bird = birds[bird]
                    if bird.y > -2 * IMAGES[bird.key][0].get_height():
                        bird.velY = bird.flapAcc
                        bird.flapped = True
                        SOUNDS['wing'].play()
            if event.type == KEYDOWN and (event.key == K_p):
                pause()

        bird_passed = False
        for bird in birds:
            bird = birds[bird]
            if bird.moving:
                crashTest = checkCrash(bird, upperPipes, lowerPipes)
            if crashTest[0] and bird.moving:
                if PRINT:
                    print(bird.key, "tuned off")
                SOUNDS['die'].play()
                bird.moving = False
                bird.distFromOpen = abs((lowerPipes[0]['y'] - PIPEGAPSIZE / 2) - bird.y)
                crashedBirds += 1

            if crashedBirds == len(birds):
                fitness = rankBirdsFitness(birds)
                if score > 0:
                    birds = generateBirds(birds, fitness, False, initx, inity, birdIndex, initVelY, initAccY,initRot)
                else:
                    birds = generateBirds({}, {}, FIRST, initx, inity, birdIndex, initVelY, initAccY, initRot)
                return birds, highscore

            if bird.moving:
                birdMidPos = bird.x + IMAGES[bird.key][0].get_width() / 2
                neural_input_x = (lowerPipes[0]['x'] + (IMAGES['pipe'][0].get_width() /2)) - birdMidPos
                neural_input_y = (lowerPipes[0]['y'] - PIPEGAPSIZE / 2) - (bird.y + birdHeight / 2)
                if neural_input_x < 0:
                    neural_input_x = (lowerPipes[1]['x'] + (IMAGES['pipe'][0].get_width() /2)) - birdMidPos
                    neural_input_y = (lowerPipes[1]['y'] - PIPEGAPSIZE / 2) - (bird.y + birdHeight / 2)


                if bird.flaps(neural_input_x, neural_input_y) and bird.y > -2 * IMAGES[bird.key][0].get_height():
                    bird.velY = bird.flapAcc
                    bird.flapped = True
                    SOUNDS['wing'].play()

                bird.distTraveled -= pipeVelX
            else:
                bird.x += pipeVelX

            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
                if pipeMidPos <= birdMidPos < pipeMidPos + 4:
                    if not bird_passed:
                        score += 1
                        bird_passed = True
                        SOUNDS['point'].play()
                    if bird.moving: #k need this so that all the birds don't update
                        bird.score += 1
            if score > highscore:
                highscore = score
            if bird.moving:
                if bird.rot > -90:
                    bird.rot -= bird.velRot
                if bird.velY < bird.maxVelY and not bird.flapped:
                    bird.velY += bird.accY
                if bird.flapped:
                    bird.flapped = False
                    bird.rot = 45

                # more rotation to cover the threshold (calculated in visible rotation)
                #playerRot = 45
                #bird.rot = 45

                bird.height = IMAGES[bird.key][bird.index].get_height()
                bird.y += min(bird.velY, BASEY - bird.y - bird.height)
        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            for bird in birds:
                bird = birds[bird]
                bird.index = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print score so player overlaps the score
        showScore(score)
        showInfo(highscore, generation)

        for bird in birds:
            bird = birds[bird]
        # Player rotation has a threshold
            visibleRot = bird.rotThr
            if bird.rot <= bird.rotThr:
                visibleRot = bird.rot
        
            playerSurface = pygame.transform.rotate(IMAGES[bird.key][bird.index], visibleRot)
            SCREEN.blit(playerSurface, (bird.x, bird.y))

        if DISPLAYSCREEN:
            pygame.display.update()
            
        # when score hits a threshold, check for the bird with the highest score
        # then report its network. 
        if score > 2:
            print("getting net")
            bird = None
            for bird in birds:
                testBird = birds[bird]
                print(testBird.score, end=" ")
                if testBird.score == score:
                    bestBird = testBird
            print()
            print("bestBird:", bestBird)
            print("best bird was ", bestBird.key)
            print("best Bird Score:", bestBird.score)
            print("best Bird Generation:", generation)
            print()
            bestNet = bestBird.network.network
            print(bestNet)
            print()
            for i in bestNet:
                print()
                for j in i:
                    print(j)

##            with open('birdNet.csv', 'w') as csvfile:
##                writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL) 
##
##                writer.writerow([neural_input_x, neural_input_y, playerFlapped, score, playerVelY])
##            
            break

        
        FPSCLOCK.tick(FPS)


def showGameOverScreen(birds):
    """crashes the player down ans shows gameover image"""
    # score = crashInfo['score']
    # playerx = SCREENWIDTH * 0.2
    # playery = crashInfo['y']
    # playerHeight = IMAGES['Bird 0'][0].get_height()
    # playerVelY = crashInfo['VelY']
    # playerAccY = 2
    # playerRot = crashInfo['Rot']
    # playerVelRot = 7
    #
    # basex = crashInfo['basex']
    #
    # upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']
    #
    # # play hit and die sounds
    # SOUNDS['hit'].play()
    # if not crashInfo['groundCrash']:
    #     SOUNDS['die'].play()

    while True:
        if not GAMEOVERSCREEN:
            return birds
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or True:
                return birds

def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    if not PIPEDETERMINTISIC:
        gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
        gapY += int(BASEY * 0.2)
    else:
        gapY = int(BASEY * 0.2) + 50
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]

def showInfo(highscore, generation):
    highDigits = [int(x) for x in list(str(highscore))]
    highWidth = 0  # total width of all numbers to be printed
    geneDigits = [int(x) for x in list(str(generation))]
    geneWidth = 0  # total width of all numbers to be printed
    for digit in highDigits:
        highWidth += IMAGES['numbers'][digit].get_width()
    for digit in geneDigits:
        geneWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = 5
    SCREEN.blit(IMAGES['high'], (Xoffset, SCREENHEIGHT * .840))
    SCREEN.blit(IMAGES['generation'], (Xoffset, SCREENHEIGHT * .917))
    XoffsetHigh = (SCREENWIDTH - highWidth) / 4 * 3 + 15
    for digit in highDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (XoffsetHigh, SCREENHEIGHT * .840))
        XoffsetHigh += IMAGES['numbers'][digit].get_width()
    XoffsetGene = (SCREENWIDTH - geneWidth) / 4 * 3 + 15
    for digit in geneDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (XoffsetGene, SCREENHEIGHT * .917))
        XoffsetGene += IMAGES['numbers'][digit].get_width()


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(bird, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    bi = bird.index
    bird.width = IMAGES[bird.key][0].get_width()
    bird.height = IMAGES[bird.key][0].get_height()

    # if player crashes into ground
    if bird.y + bird.height >= BASEY - 1:
        return [True, True]
    else:

        birdRect = pygame.Rect(bird.x, bird.y,
                      bird.width, bird.height)

        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS[bird.key][bi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(birdRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(birdRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False


def generateBirds(birds, fitness,  FIRST, initx, inity, birdIndex, initVelY,initAccY,initRot):
    '''Generates birds for the genetic algorithm'''
    if FIRST:
        for i in range(NUMBERBIRDS):
            yplus = 0 # random.randint(5,15)
            birds["Bird " + str(i)] = Bird(initx, inity + yplus, birdIndex, "Bird " + str(i), initVelY, initAccY,
                                           initRot, 0)
    else:
        newGeneration = {}
        winners = fitness[-4:]
        winners = winners[::-1]
        first = birds[winners[0][0]]
        second = birds[winners[1][0]]
        third = birds[winners[2][0]]
        fourth = birds[winners[3][0]]
        selection = [first, second, third, fourth]
        numInputs = first.network.inputs
        numOutputs = first.network.outputs
        newGeneration['Bird 0'] = Bird(initx, inity, first.index, "Bird " + str(0), initVelY, initAccY,
                                       initRot, Net(numInputs, numOutputs, deepcopy(first.network.network),
                                                             deepcopy(first.network.bias)))
        newGeneration['Bird 1'] = Bird(initx, inity, second.index, "Bird " + str(1), initVelY, initAccY,
                                       initRot, mutation(Net(numInputs, numOutputs, deepcopy(first.network.network),
                                                             deepcopy(first.network.bias),.05)))
        newGeneration['Bird 2'] = Bird(initx, inity, third.index, "Bird " + str(2), initVelY, initAccY,
                                       initRot, mutation(Net(numInputs, numOutputs, deepcopy(first.network.network),
                                                             deepcopy(first.network.bias)), .10))
        newGeneration['Bird 3'] = Bird(initx, inity, fourth.index, "Bird " + str(3), initVelY, initAccY,
                                       initRot, mutation(Net(numInputs, numOutputs, deepcopy(first.network.network),
                                                             deepcopy(second.network.bias)), .15))
        newGeneration['Bird 4'] = Bird(initx, inity, fourth.index, "Bird " + str(4), initVelY, initAccY,
                                       initRot, mutation(Net(numInputs, numOutputs, deepcopy(first.network.network),
                                                             deepcopy(second.network.bias)), .15))
        newGeneration['Bird 5'] = Bird(initx, inity, fourth.index, "Bird " + str(5), initVelY, initAccY,
                                       initRot, mutation(Net(numInputs, numOutputs, deepcopy(first.network.network),
                                                             deepcopy(third.network.bias)), .1))
        newGeneration['Bird 6'] = Bird(initx, inity, first.index, "Bird " + str(6), initVelY, initAccY,
                                       initRot, crossOver(first, second))
        newGeneration['Bird 7'] = Bird(initx, inity, second.index, "Bird " + str(7), initVelY, initAccY,
                                       initRot, crossOver(second, third))
        birdOne = random.choice(selection)
        birdTwo = random.choice(selection)
        newGeneration['Bird 8'] = Bird(initx, inity, third.index, "Bird " + str(8), initVelY, initAccY,
                                       initRot, crossOver(birdOne, birdTwo))
        birdOne = random.choice(list(birds.values()))
        birdTwo = random.choice(list(birds.values()))
        newGeneration['Bird 9'] = Bird(initx, inity, fourth.index, "Bird " + str(9), initVelY, initAccY,
                                       initRot, crossOver(birdOne, birdTwo))
        birds = newGeneration

        # This will print out the network for each bird
        for bird in birds:
            print()
            bird = birds[bird]
            print(bird.key)
            for i in bird.network.network:
                print()
                for j in i:
                    print(j)
                        

    return birds

def mutation(network, MUT_RATE=.2):
    for index in range(len(network.network[0])):
        for i in range(len(network.network[0][index]['weights'])):
            if random.random() < MUT_RATE:
                network.network[0][index]['weights'][i] += random.triangular(-1, 1) * network.network[0][index]['weights'][i]
                #print(network.network[0][index]['weights'][i])
    return network

# Cross over is a genetic concepts and this creates new offspring from two parents
def crossOver(bird1, bird2, MUT_RATE=0.2):
    network1 = deepcopy(bird1.network)              # Bird 1's neural network
    network2 = deepcopy(bird2.network)              # Bird 2's neural network
    numberHidden = int(network1.hidden)             # Number of Hidden Neurons
    numberInputs = network1.inputs                  # Number of Inputs Neurons
    mumberOutputs = network1.outputs                # Number of Outputs Neurons
    crossHiddenNum = math.ceil(numberHidden / 2)    # This is the number of elements selected for crossover
    crossIndex = list(range(0, numberHidden))       # This is used for selecting crossover weights in hidden layer
    crossIndex2 = list(range(0, numberHidden))      # This is used for selecting crossover weights in output layer
    corssIndex3 = list(range(0, numberHidden))
    newBias = []
    for i in range(int(crossHiddenNum)):
        selectionIndex = random.choice(crossIndex)
        crossIndex.remove(selectionIndex)
        temp = network1.network[0][selectionIndex]['weights']
        network1.network[0][selectionIndex]['weights'] = network2.network[0][selectionIndex]['weights']
        network2.network[0][selectionIndex]['weights'] = temp
        selectionIndex = random.choice(crossIndex2)
        crossIndex2.remove(selectionIndex)
        temp = network1.network[1][0]['weights'][selectionIndex]
        network1.network[1][0]['weights'][selectionIndex] = network2.network[1][0]['weights'][selectionIndex]
        network2.network[1][0]['weights'][selectionIndex] = temp
        
    return mutation(random.choice([network1, network2]))



def rankBirdsFitness(birds):
    fitness = []
    for bird in birds:
        bird = birds[bird]
        if len(fitness) == 0:
            fitness.append((bird.key, bird.calculate_fitness(), bird))
        else:
            inserted = False
            birdFitness = (bird.key, bird.calculate_fitness(), bird)
            for i in range(len(fitness)):
                if fitness[i][1] > birdFitness[1]:
                    fitness.insert(i, birdFitness)
                    inserted = True
                    break
            if not inserted:
                fitness.append(birdFitness)
    return fitness

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask







if __name__ == '__main__':
    main()
