import matplotlib.pyplot as plt
import numpy as np
import random
import os
import math


# Reads the file  of colours
# Returns the number of colours in the file and a list with the colours (RGB) values

def read_file(fname):
    with open(fname, 'r') as afile:
        lines = afile.readlines()
    n = int(lines[3])  # number of colours  in the file
    col = []
    lines = lines[4:]  # colors as rgb values
    for l in lines:
        rgb = l.split()
        for i in range(len(rgb)):
            rgb[i] = float(rgb[i])
        col.append(rgb)
    return n, col


# Display the colours in the order of the permutation in a pyplot window
# Input, list of colours, and ordering  of colours.
# They need to be of the same length

def plot_colours(col, perm):
    assert len(col) == len(perm)

    ratio = 10  # ratio of line height/width, e.g. colour lines will have height 10 and width 1
    img = np.zeros((ratio, len(col), 3))
    for i in range(0, len(col)):
        img[:, i, :] = colours[perm[i]]

    fig, axes = plt.subplots(1, figsize=(8, 4))  # figsize=(width,height) handles window dimensions
    axes.imshow(img, interpolation='nearest')
    axes.axis('off')
    return plt


#####_______main_____######


# Get the directory where the file is located
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = read_file('colours')  # Total number of colours and list of colours

test_size = 100  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

# permutation = random.sample(range(test_size), test_size)  # produces random pemutation of lenght test_size, from the numbers 0 to test_size -1
# plt = plot_colours(test_colours, permutation)
# plt.savefig('fig1')


####______Hill Climbing______#######


def hill_climbing():
    s = random_solution()                       # random array of colours
    # print("random solution s: ", s)
    plt = plot_colours(test_colours, s)         # random array is plotted for future comparison
    plt.savefig('fig1')                         # save fig1.png - optional
    plt.draw()                                  # use draw() not show() as program stops when show() is called
    best = s                                    # random array is stored as current best solution

    for i in range(test_size):                  # loop start
        dist1 = evaluate(best)                  # best array is evaluated and distance is stored
        print("Current best: ", dist1)          # current best is printed
        s2 = best.copy()                        # store a copy of s in s2 (copy means if s is changes s2 wont change)
        # print("s2: ", s2)
        r1 = random.randint(0, test_size - 1)   # random number is chose within test size
        # print("r1: ", r1)
        r2 = random.randint(0, test_size - 1)   # a second random number is chose within test size
        # print("r2: ", r2)
        if r1 < r2:                             # check they are in the correct order
            s2[r1:r2:+1] = reversed(s2[r1:r2:+1])# they are switched and anything between them is also switched
        else:
            s2[r2:r1:+1] = reversed(s2[r2:r1:+1])# if r2 is smaller then we begin there and end at position r1
        # print("s2 again: ", s2)
        dist2 = evaluate(s2)                    # second array is evaluated and distance is stored
        print("New distance: ", dist2)          # print new distance with the switched values

        if dist2 < dist1:                       # compares the total distances of both solutions
            dist1 = dist2                       # if distance 2 is the smallest, it is stored for the next loop
            print("NEW BEST DISTANCE: ", dist1, "\n") # print new best
            best = s2                           # the best solution is now the smallest
        else:                                   # s is still the best. We continue using s for next loop
            print("No new best distance\n", dist1, "\n")# print the best distance
    return best


# Selects random sample from colours file within the test size specifies
def random_solution():
    return random.sample(range(test_size), test_size)


# def calc_distance(col1, col2):  # receive colours from evaluate
#     r1, b1, g1 = colours[col1]  # separate colours into values
#     r2, b2, g2 = colours[col2]
#     distance = math.sqrt((r2-r1)**2 + (b2-b1)**2 + (g2-g1)**2)  # calculate euclidean distance between colours
#     return distance


# Calculates the total distance of solution s
def calc_distance(s, col1, col2, distance):     # receive solution and the index of the colours to calculate distance
    try:
       # print("s[col1]: ", s[col1])
       # print("s[col2]: ", s[col2])
        r1, b1, g1 = colours[s[col1]]           # separate colours into values
        r2, b2, g2 = colours[s[col2]]
       # calculate euclidean distance between colours
        distance = distance + math.sqrt((r2 - r1) ** 2 + (b2 - b1) ** 2 + (g2 - g1) ** 2)
    except:
        print("Evaluation Complete")            # print when there is no
    # print("New distance: ", distance)
    return distance                             # total distance is returned


def evaluate(s):
    dist = 0                                    # ensure dist starts as 0
    for i in range(test_size):                  # loop for full test size
        # dist = calc_distance(i, i+1) # calculate distance for each colour and its adjacent colour
        dist = calc_distance(s, i, i + 1, dist) # calculate the total of all the distances
    return dist                                 # euclidean distance array of colours and adjacent colours returned


s = hill_climbing()                             # the best distance is stored in s
dist = evaluate(s)                              # get best distance to output
plt = plot_colours(test_colours, s)             # The best distance is plotted
print("                                         Best solution: ", s)
print("                                         Best distance: ", dist)
plt.savefig('fig2')                             # saving the plotted image - optional
plt.show()                                      # show fig 1 and fig 2

