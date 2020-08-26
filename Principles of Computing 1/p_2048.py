"""
Merge function for 2048 game.
"""


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """

    orig_size = len(line)

    line = [i for i in line if i != 0]

    arr = []

    index = 0
    while index < len(line):
        if index == len(line) - 1:
            arr.append(line[index])
        else:
            if line[index] == line[index + 1]:
                arr.append(line[index] * 2)
                index += 1
            else:
                arr.append(line[index])
        index += 1
    arr += [0] * (orig_size - len(arr))
    return arr


print(merge([2, 0, 2, 4]))
print(merge([4, 4, 0, 0]))
print(merge([0, 0, 2, 2]))
print(merge([2, 2, 0, 0]))
print(merge([2, 2, 2, 2, 2]))
print(merge([8, 16, 16, 8]))
