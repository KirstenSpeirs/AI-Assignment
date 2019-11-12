from statistics import stdev

import matplotlib.pyplot as plt
import numpy as np
import random
import os
import math
import time
# start_time = time.time()


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


# Selects random sample from colours file within the test size specifies
def random_solution():
    return random.sample(range(test_size), test_size)


# Calculates the total distance of solution s
def calc_distance(index_list, col1, col2):     # receive solution and the index of the colours to calculate distance
    distance = 0
    try:
        r1, b1, g1 = col1          # separate colours into values
        r2, b2, g2 = colours[index_list[col2]]
       # calculate euclidean distance between colours
        distance = math.sqrt((r2 - r1) ** 2 + (b2 - b1) ** 2 + (g2 - g1) ** 2)
    except:
        print("Evaluation Complete")            # print when there is no more colours
    return distance                             # total distance is returned

#####_______Greedy Constructive_____######

def lowest(index_list, placeholder):
    # print("placeholder START", placeholder)
    # print(colours[index_list[0]])
    smallest_distance = 1000                   # set large starting distance for the first new distance to replace
    index = -1                                 # set starting index as -1 to be replaced by new index pointing to shortest distance
    for i in range(len(index_list)):           # list gets smaller as indexes are removed so we loop 1 less each time
        dist = calc_distance(index_list, placeholder, i)# the distance between the first
        # print(i)
        # try:
        #     print("distance calculated between placeholder", placeholder, "and next colour", colours[index_list[i]], "=", dist)
        # except:
        #     print()

        if dist < smallest_distance:            # check if new distance is smallest
            smallest_distance = dist            #  new smallest
            # print("Smallest distance", smallest_distance)
            index = i                           # take note of position of the index with the smallest distance
        # print("Smallest distance out", smallest_distance)
    # print("FINAL index of closest neighbour", index)

    try:
        placeholder = colours[index_list[index]]# new colour is saved for the next round of comparisons. This is also the index of the colour stored at index of index list
        # print("new placeholder colour:", colours[index_list[index]])
    except:
        print("no new placeholder")             # colours compared so there is none left in the list
    # print("placeholder END", placeholder, "\n")
    # print("index of index", index_list[index])
    return index_list[index], placeholder       # return the new index tho be added to sorted[] and removed from index_list[]. Return placeholder for next round of comparisons


def greedy_constructive():
    sorted = []                                 # create list for indexes to be sorted into
    index_list = random_solution()              # create array of indexes to be sorted
    placeholder = colours[index_list[0]]        # new starting point after loop
    sorted.append(index_list[0])                # add the starting point to the new list
    # print("index", (index_list[0]))

    plt = plot_colours(test_colours, index_list)# plot random starting list
    plt.savefig("1")                            # save image

    del index_list[0]                           # delete the starting point so distance does not = 0
    print("starting list", index_list)
    for i in range(test_size-1):                # loop for all items in list
        new_index, placeholder = lowest(index_list, placeholder)# find the lowest distance index to be added to the list
        sorted.append(new_index)                # add the new index to the list
        try:
            index_list.remove(new_index)        # while there are items in the list, remove the new index
            # print("deleted value. new list", index_list)
        except:
            print("end of list")
        # print("SORTED" ,sorted, "\n")

    return sorted                               # return the sorted list

#####_______main_____######


# Get the directory where the file is located
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = read_file('colours')  # Total number of colours and list of colours

test_size = 100  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing


sorted = greedy_constructive()                  # store sorted list of indexes to be plotted
print("end list", sorted)
plt = plot_colours(test_colours, sorted)        # plot list
plt.savefig("2")                                # save sorted plot
