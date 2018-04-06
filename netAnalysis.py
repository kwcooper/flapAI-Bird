# data anaysis for flapAI

import pickle
import matplotlib.pyplot as plt


'''
Structure for data.p

| data
generation #
scores list | generation dict ('G1')
            | bird key ('B2') | scores
            | score | meta_data
                    | topo key ('topo') | net weights ('netWeights')


'''


d = pickle.load(open("data.p", "rb"))

print(len(d))

# grab the scores for each generation
# scores is a list of list with scores
scores = []
for i in range(0,len(d)):
    scores.append(d[i]['G'+str(i)][10])

# find average scores
genScoreAvg = []
for i in range(len(scores)):
    genScoreAvg.append(sum(scores[i])/len(scores[i]))

plt.plot(genScoreAvg)
plt.title('Average Score')
#plt.show()

print()
#Grab topos
topoPerGen = []
for i in range(0,len(d)): # num generations
    topoPerGen.append([])
    for j in range(0,9): # num birds
        topoPerGen[i].append(d[i]['G'+str(i)][j]['B'+str(j)][1]['topo'])

#
topos = []
for topo in topoPerGen:
    for j in range(0, len(topo)):
        if topo[j] not in topos:
            topos.append(topo[j])
print(topos)

# count each type of topology
counts = []
for i in range(0,len(topos)):
    counts.append(0)
    for topo in topoPerGen:
        for j in range(0, len(topo)):
            if topos[i] == topo[j]:
                counts[i] += 1
        
        
