
Julia Vendemiatti

Aditya Khant

Daphne Poon

About Our Project:

Picobot is a simple programing language that controls a robot in an
enclosed environment. A program can control where the robot travels 
using states and directions. Once it has visited a certain cell in the
environment, the cell becomes shaded. (More about Picobot here:
https://www.cs.hmc.edu/csforall/Introduction/Introduction.html)

The goal of our final project was to create and "evolve" randomly generated
Picobot programs in a Picobot environment simmulated with Python.

Run the file and use the method GA(popSize, numgens) to simmulate numgens
generations each consisting of popSize Picobot programs. The first 
generation consists of programs that are completely randomly generated.
Each program's "fitness" is then assesed by simmulating it in the Picobot
environment, and calculating the percentage of the environment that
the robot visited, or was shaded. 

The following generations are created by "breeding" only the  "fittest" 
programs (highest percentage of environment covered). The universal variable
CREAMOFTHECROP determines how many programs make it to breeding in each 
generagion. The "breeding" isdone by the method crossover(self, other). 
There are also occasional "mutations" in the "breeding". 

For each generation, the method GA prints the average fitness of the
programs in that generation, the fitness of the best program, and 
saves a text file containing the top program. 

Running GA with a higher population size and more generations yields 
better programs over time -- but it can take a while. We've been able
to produce a program that fills 100% of the Picobot environment every time
by running GA with popSize = 100 and numgens = 20. It shouldn't take more
than 5 minutes.

Feel free to eail me, jvendemiatti@hmc.edu, if you have any questions 
or comments!





