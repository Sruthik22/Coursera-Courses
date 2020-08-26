"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """

    new_list = []

    for index in list1:
        if len(new_list) == 0:
            new_list.append(index)
            continue
        if new_list[-1] != index:
            new_list.append(index)

    return new_list


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """

    point1 = 0
    point2 = 0

    result = []

    while point1 < len(list1) and point2 < len(list2):
        if list1[point1] == list2[point2]:
            result.append(list1[point1])
            point1 += 1
            point2 += 1
        else:
            if list1[point1] < list2[point2]:
                point1 += 1
            else:
                point2 += 1

    return result


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """

    result = []

    pointer1 = 0
    pointer2 = 0
    while pointer1 < len(list1) and pointer2 < len(list2):
        if list1[pointer1] < list2[pointer2]:
            result.append(list1[pointer1])
            pointer1 += 1
        else:
            result.append(list2[pointer2])
            pointer2 += 1
    if pointer1 < len(list1):
        result.extend(list1[pointer1:])
    else:
        result.extend(list2[pointer2:])

    return result


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """

    if len(list1) <= 1:
        return list1

    mid = int(math.floor(len(list1) / 2))

    lower = [list1[i] for i in range(mid)]
    higher = [list1[i] for i in range(mid, len(list1))]

    return merge(merge_sort(lower), merge_sort(higher))


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """

    if len(word) == 0:
        return [""]

    char = word[0]

    all_strings = gen_all_strings(word[1:])

    result = []

    for index in all_strings:
        for pos_to_change in range(len(index) + 1):
            new_string = index[:]
            updated_string = new_string[:pos_to_change] + char + new_string[pos_to_change:]
            result.append(updated_string)
    return result + all_strings


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)


# Uncomment when you are ready to try the game
# run()