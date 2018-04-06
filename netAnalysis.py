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
for i in range(0,len(d)-1):
    scores.append(d[i]['G'+str(i)][10])

genScoreAvg = []
for i in range(len(scores)):
    
