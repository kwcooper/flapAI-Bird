import math
from random import seed
from random import random
import random
import numpy as np

class Net:
    def __init__(self, n_inputs, n_outputs, n_net=False, n_bias=False, n_hidden=6):
        self.height = 190
        self.distance = 142
        self.inputs = n_inputs
        self.hidden = n_hidden
        self.outputs = n_outputs
        self.network = list()
        #self.weights = weights
        if not n_bias:
            self.bias = []
        else:
            self.bias = n_bias
        if not n_net:
            self.init_net()
        else:
            self.network = n_net


    # Initialize a network
    def init_net(self):
        self.network = list()
        # Add first bias for inputs
        self.bias.append(self.genWeights(self.hidden))

        # Initialize and append the hidden layer to the network
        hidden_layer = [{'weights': self.genWeights(self.inputs)} for i in range(self.hidden)]
        self.network.append(hidden_layer)

        # Add second bias for outputs
        self.bias.append(self.genWeights(self.outputs))

        # Initialize and append the output layer to the network
        output_layer = [{'weights': self.genWeights(self.hidden)} for i in range(self.outputs)]
        self.network.append(output_layer)


    # Generates a numpy array of random  numbers from a uniform distribution from -1,1 of length n
    def genWeights(self, n):
        weights = []
        for x in range(n):
            weights.append(random.uniform(-1, 1))
        return np.array(weights)

    # Calculate neuron activation for an input
    def activate(self, weights, inputs, bias):
        return weights.dot(inputs) + bias

    # Transfer neuron activation
    def transfer(self, gamma):
        if gamma < 0:
            return 1 - 1 / (1 + math.exp(gamma))
        return 1 / (1 + math.exp(-gamma))

    # Forward propagate input to a network output
    def propagate(self, inputs):
        inputs = np.array([inputs[0], inputs[1]])
        index = 0
        for layer in self.network:
            new_inputs = []
            bias = self.bias[index]
            index += 1
            index2 = 0
            for neuron in layer:
                activation = self.activate(neuron['weights'], inputs, bias[index2])
                index2 += 1
                neuron['output'] = self.transfer(activation)
                new_inputs.append(neuron['output'])
            inputs = new_inputs
        return inputs

    def get_net(self):
        return self.network

