import random

nato_number = {"rock": 0, "spock": 1, "paper": 2, "lizard": 3, "scissors": 4}
nuto_name = {0: "rock", 1: "spock", 2: "paper", 3: "lizard", 4: "scissors"}


def name_to_number(name):
    if name in nato_number.values():
        return nato_number[name.lower()]
    else:
        return "The name is not correct"


def number_to_name(number):
    if number in nuto_name.values():
        return nuto_name[number]
    else:
        return "The number is not correct"


def rpsls(player_choice):
    print("Player chooses " + player_choice)

    rep = name_to_number(player_choice)
    comp_number = random.randrange(0, 5)
    print("Computer chooses " + number_to_name(comp_number))
    diff = (comp_number - rep) % 5

    if diff == 0:
        print("Player and computer tie!")
    elif diff == 1 or diff == 2:
        print("Computer Wins!")
    else:
        print("Player Wins!")
    print()


rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
