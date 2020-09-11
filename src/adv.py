#! /usr/bin/python3
from room import Room
from player import Player
from item import Item


def getUserInput():
    userInput = input("Direction to move: ").lower().split(" ")
    print(userInput)
    if len(userInput) == 1:
        return userInput[0]
    return userInput


def movePlayer(direction):
    global playerLocation
    direction += "_to"

    if hasattr(playerLocation, direction):
        """debug prints
        print(f"current room: {player.current_room}")
        print(f"playerLocation: {playerLocation}")
        print(f"input {direction}")
        """
        # player.current_room = getattr(playerLocation, direction)
        # player.current_room = room[playerLocation][direction]
        playerLocation = getattr(playerLocation, direction)
        """ more debug prints
        print(f"current room: {player.current_room}")
        print(f"playerLocation: {playerLocation}")
        """
        print("\n=== new room info ===\n")
        roomInfo(playerLocation)
    else:
        print("There is no path that way")

    """
    hint from hints file
    player.location = room['foyer'].s_to  # we were in the foyer, then went south
    """


def take(item):
    print(f"item {item.name} {item.description}")

    playerLocation.items.remove(item)
    player.inventory.append(item)
    print(f"player has: {player.inventory}")
    print(f"room has: {playerLocation.items}")
    return


def roomInfo(rm):
    # room name
    print(f"You are in the {playerLocation}")
    print("=" * 5)

    # room description
    print(playerLocation.description)
    print("=" * 5)

    # items in the room
    # roomItems = [item.name for item in playerLocation.items]
    print(playerLocation.itemList())
    print("=" * 5)

    # exits
    roomExits = ["n_to", "s_to", "e_to", "w_to"]

    exits = []
    for direction in roomExits:
        if hasattr(playerLocation, direction):
            # print(direction)
            exits.append(direction)

    for direction in exits:
        print(f"{direction.title()} the {getattr(playerLocation, direction)}")
    print("=" * 5)


def quitGame():
    return "game quit"


# Item creation

worldItems = {
    "torch": Item("torch", "A lit torch that is able to provide some light"),
    "key": Item("key", "Who knows what lock this might open?"),
}


# Declare all the rooms

room = {
    "outside": Room(
        "Outside Cave Entrance",
        "North of you, the cave mount beckons",
        [worldItems["torch"], worldItems["key"]],
    ),
    "foyer": Room(
        "Foyer",
        "Dim light filters in from the south. Dusty passages run north and east.",
    ),
    "overlook": Room(
        "Grand Overlook",
        """A steep cliff appears before you, falling
    into the darkness. Ahead to the north, a light flickers in
    the distance, but there is no way across the chasm.""",
    ),
    "narrow": Room(
        "Narrow Passage",
        """The narrow passage bends here from west
    to north. The smell of gold permeates the air.""",
    ),
    "treasure": Room(
        "Treasure Chamber",
        """You've found the long-lost treasure
    chamber! Sadly, it has already been completely emptied by
    earlier adventurers. The only exit is to the south.""",
    ),
}


# Link rooms together

room["outside"].n_to = room["foyer"]
room["foyer"].s_to = room["outside"]
room["foyer"].n_to = room["overlook"]
room["foyer"].e_to = room["narrow"]
room["overlook"].s_to = room["foyer"]
room["narrow"].w_to = room["foyer"]
room["narrow"].n_to = room["treasure"]
room["treasure"].s_to = room["narrow"]

# Make a new player object that is currently in the 'outside' room.

player = Player(room["outside"])
print(f"### initial room: {player.current_room} ###")
playerLocation = player.current_room


#
# Main
#


# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

# print(room["foyer"])
# print(userInput)
# print(room["foyer"])
# print(room["outside"])
# print(f"Connects to: {room[playerLocation].n_to.name}")
moveDir = ["n", "s", "e", "w"]
doCmds = ["get", "take", "drop", "look"]

#! GAME LOOP
roomInfo(playerLocation)
while True:
    print(f"inv is {player.inventory}")
    cmdInput = getUserInput()
    if cmdInput == "q" or cmdInput == "quit":
        break
    else:
        if cmdInput in moveDir:
            movePlayer(cmdInput)
            continue
        elif cmdInput[0] == "take":
            take(worldItems[cmdInput[1]])
            continue
        else:
            print("Unknown command")
