# data anaysis for flapAI

import pickle


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

