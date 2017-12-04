

# Flap(AI) Bird

Artificial intelligence playing a Python Port of the famous Flappy Bird game. We used genetic algorithms to train neural networks for each bird, which quickly learns how to jump, even on non deterministic pipes, after about 30 generations, the bird can play as well as the average human. After a few hundred, the bird quickly becomes superhuman. 
Also included is a supervised neural network and training data pulled from a hardcoded bird (70 pipe average).

## Video
<img src="videos/output.gif"> 

## Motivation 

Neural networks can be tricky business. With all sorts of hyperparameters (number of neurons, number of layers, connections) and weights to worry about, it's no wonder why our supervised net didn't work out. Thus, but using a genetic algorithm to train the neural network, we could evolve birds to play much quicker and with more variable maps compared to any supervised network.
This work shows the power of unsupervised learning and features an algorithm which could be used in many other applications.


## Installing
This code should run on any machine, with pygame being the biggest bottleneck on that front.
As always with python, we recommend using pip to install packages. 

1. Install Python 2.7.X or 3.5.x from [here](https://www.python.org/download/releases/)

2. Install PyGame 1.9.X from [here](http://www.pygame.org/download.shtml)

3. Grab this repo


End with an example of getting some data out of the system or using it for a little demo

## Use

Run `python flappy.py` from the repo's directory. This will open up a pygame window. The simulation should begin automatically and will only stop if exited. 

At the top of the same file exist other 


use <kbd>p;</kbd> key to pause and <kbd>Esc</kbd> to close the game.



## Authors

* **Keiland Cooper** - *data collection, supervised net, neural network, network analysis* - [website](https://www.kwcooper.xyz)
* **Christopher East** - *Game editing and genetic algorithm work* - [github](https://github.com/ceastIU)
* **Kirk Harlow** - *Game editing and data collection* - [github](https://github.com/jkharlow)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under an edited MIT License. 

## Acknowledgments

* This implementation borrows and modifies a PyGame Version of flappy bird found at https://github.com/sourabhv/FlapPyBird, by Sourabh Verma (sourabhv)



