"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
#import codeskulptor

#codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """

    max_val = 0

    for value in hand:
        max_val = max(max_val, hand.count(value) * value)

    return max_val


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    all_sequences = gen_all_sequences(range(1,num_die_sides+1), num_free_dice)
    result = 0.0

    for sequence in all_sequences:
        full_hand = held_dice + sequence
        result += score(full_hand)

    return float(result) / float(len(all_sequences))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    all_ps = [()]
    last_p = [[]]

    for value in range(len(hand)):
        new_p = []
        for val in last_p:
            for val_k in range(len(hand)):
                j_mu = list(val)
                if val_k not in j_mu:
                    j_mu.append(val_k)
                    new_p.append(tuple(j_mu))
        all_ps.extend(new_p)
        last_p = new_p
    final = []
    for value in all_ps:
        this_tuple = []
        for val in value:
            this_tuple.append(hand[val])
        this_tuple.sort()
        this_tuple = tuple(this_tuple)
        if this_tuple not in final:
            final.append(this_tuple)
    return set(final)


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """

    all_holds = gen_all_holds(hand)

    max_exp = 0
    max_hold = ()

    for hold in all_holds:
        exp = expected_value(hold, num_die_sides, len(hand) - len(hold))
        if exp > max_exp:
            max_exp = exp
            max_hold = hold

    return max_exp, max_hold


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print("Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score)


#run_example()

print(expected_value((2, 2), 6, 2))