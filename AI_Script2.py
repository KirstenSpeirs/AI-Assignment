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
            rgb[i]= float(rgb[i])
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
    plt.show()

#####_______main_____######

# Get the directory where the file is located
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)  # Change the working directory so we can read the file

test_size, colours = read_file('colours')  # Total number of colours and list of colours

test_size = 100  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

permutation = random.sample(range(test_size),
                            test_size)  # produces random pemutation of lenght test_size, from the numbers 0 to test_size -1
plot_colours(test_colours, permutation)

# Selects random sample from colours file within the test size specifies


def random_solution():
    return random.sample(range(test_size),test_size)


def calc_distance(col1, col2):
   r1, b1, g1 = colours[col1]
   r2, b2, g2 = colours[col2]
   distance = math.sqrt((r2-r1)**2 + (b2-b1)**2 + (g2-g1)**2)
   return distance


def evaluate(s):
    dist = 0
    for i in range(test_size):
        dist = calc_distance(i, i+1)
    return dist


s = random_solution()


####______Hill Climbing______#######


def hill_climbing():
    best = s
    for i in range(10000):
        best_dist = evaluate(s)
        s2 = s.copy()
        r1 = random.randint(0, test_size - 1)
        r2 = random.randint(0, test_size - 1)
        if r1 < r2:
            s2 = s2[r1:r2:-1]
        else:
            s2 = s2[r2:r1:-1]


            # index = s2.index(r1)
            # index2 = s2.index(r2)
            # s2.pop(r1)
            # s2.pop(r2)
            # s2.insert(index, r2)
            # s2.insert(index2, r1)

        dist2 = evaluate(s2)
        if dist2 < best_dist:
            best = dist2
    return best


s = hill_climbing()
dist = evaluate(s)
plot_colours(test_colours, s)
print("Distance: ", dist)


####______Greedy______#######


# s is the random solution provided, start is the index of the starting location
def greedy_constructive(s, start):
    s = random_solution()
    path = [start]
    #shape returns demensions of colours
    n = s.shape[0]
    mask = np.ones(n, dtype=bool)  # boolean values of location haven't been visited
    mask[start] = False

    for i in range(n - 1):
        last = path[-1]
        next_ind = np.argmin(s[last][mask])  # minimum of remaining locations
        # print('Next index: ', next_ind, ', Last: ', last, ', Mask: ', mask)
        next_loc = np.arange(n)[mask][next_ind]  # convert to original location
        # print('Next Loc: ', next_loc)
        path.append(next_loc)
        mask[next_loc] = False

    return path


plot_colours(test_colours,random_solution())
s = greedy_constructive(s, 0)
plot_colours(test_colours, s)
distance = evaluate(s)
print('Distance: ', distance)
