#! /usr/bin/python3
from room import Room
from player import Player
from item import Item
from lightsource import Lightsource
from container import Container


def getUserInput():
    userInput = input("Input command: ").lower().split(" ")
    if len(userInput) == 1:
        return userInput[0]
    return userInput


def movePlayer(direction):
    global playerLocation
    direction = f"{direction[0]}_to"

    if hasattr(playerLocation, direction):
        """debug prints
        print(f"current room: {player.current_room}")
        print(f"playerLocation: {playerLocation}")
        print(f"input {direction}")
        """
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
    takeItem = worldItems[item]
    containerItem = isinstance(takeItem, Container)
    if takeItem in playerLocation.items and not containerItem:
        playerLocation.items.remove(takeItem)
        player.inventory.append(takeItem)
        print(takeItem.on_take())
        return
    if containerItem:
        print("You can not take that item")
        return
    print(f"There is no {takeItem.name} here")


def drop(item):
    dropItem = worldItems[item]
    if dropItem in player.inventory:
        playerLocation.items.append(dropItem)
        player.inventory.remove(dropItem)
        print(dropItem.on_drop())
        return
    print(f"You are not carrying a {dropItem.name}")


def look(item):
    lookItem = worldItems[item]
    if lookItem in player.inventory or lookItem in playerLocation.items:
        print(lookItem.description)
        return
    print(f"You do not see a {lookItem.name}")


def openContainer(item):
    openItem = worldItems[item]
    if openItem in playerLocation.items:
        isContainer = isinstance(openItem, Container)
        if isContainer:
            print(openItem)
            for insideItem in openItem.inside:
                openItem.inside.remove(insideItem)
                player.inventory.append(insideItem)
            return
        print(f"You can not open the {openItem.name}")
        return
    print(f"You do not see a {openItem.name}")


def inventory(unused):
    print(player.hasInventory())


def helpCommands(unused):
    print(
        "\nUse 'n', 's', 'e', or 'w' to move\nUse 'i' or 'inventory' to view inventory\nUse 'take', 'drop', 'look', 'open', to interact with items\n"
    )


def roomInfo(rm):
    """
    check if light is in the room
    """
    if (
        playerLocation.isLight == False
        and len(
            [item.name for item in player.inventory if isinstance(item, Lightsource)]
        )
        == 0
        and len(
            [
                item.name
                for item in playerLocation.items
                if isinstance(item, Lightsource)
            ]
        )
        == 0
    ):
        print(f"This room is too dark to see anything")
        print("=" * 5)
        return

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
    roomExits = ["n_to", "s_to", "e_to", "w_to", "u_to", "d_to"]

    exits = []
    for direction in roomExits:
        if hasattr(playerLocation, direction):
            # print(direction)
            exits.append(direction)

    for direction in exits:
        print(f"{direction.title()} the {getattr(playerLocation, direction)}")
    print("=" * 5)


def quitGame():
    print("Game Quit")


# Item creation

worldItems = {
    "torch": Lightsource("torch", "A lit torch that is able to provide some light"),
    "rope": Item("rope", "A rope that could be used to cross a large gap"),
    "treasureChest": Container(
        "chest", "A chest that contains a neatly coiled rope", []
    ),
}
# add items into Container instances
worldItems["treasureChest"].inside.append(worldItems["rope"])

# Declare all the rooms

room = {
    "outside": Room(
        "Outside Cave Entrance",
        "North of you, the cave mount beckons",
        [],
        True,
    ),
    "foyer": Room(
        "Foyer",
        """Dim light filters in from the south. Dusty passages run north and east.""",
        [worldItems["torch"]],
        True,
    ),
    "overlook": Room(
        "Grand Overlook",
        """A steep cliff appears before you, falling
    into the darkness. Ahead to the north, a light flickers in
    the far distance, but there is no way across the chasm.""",
        [],
    ),
    "narrow": Room(
        "Narrow Passage",
        "The narrow passage curves here from west to north.",
        [],
    ),
    "bottomTower": Room(
        "Tower Floor",
        "There is a old spiral staircase leading up toward the next floor. You are not sure when it was last used.",
        [],
    ),
    "midTower": Room(
        "Tower Stairs",
        "The winding stairs lead both up and down. The smell of gold permeates the air.",
        [],
    ),
    "treasure": Room(
        "Treasure Chamber",
        """You've found the long-lost treasure chamber!
        A lone chest covered in cobwebs sits against the far wall.
        The only exit is back down the stairs.""",
        [worldItems["treasureChest"]],
    ),
}


# Link rooms together

room["outside"].n_to = room["foyer"]
room["foyer"].s_to = room["outside"]
room["foyer"].n_to = room["overlook"]
room["foyer"].e_to = room["narrow"]
room["overlook"].s_to = room["foyer"]
room["narrow"].w_to = room["foyer"]
room["narrow"].n_to = room["bottomTower"]
room["bottomTower"].s_to = room["narrow"]
room["bottomTower"].u_to = room["midTower"]
room["midTower"].d_to = room["bottomTower"]
room["midTower"].u_to = room["treasure"]
room["treasure"].d_to = room["midTower"]


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
moveDir = {
    "n": movePlayer,
    "s": movePlayer,
    "e": movePlayer,
    "w": movePlayer,
    "u": movePlayer,
    "d": movePlayer,
    "north": movePlayer,
    "south": movePlayer,
    "east": movePlayer,
    "west": movePlayer,
    "up": movePlayer,
    "down": movePlayer,
    "i": inventory,
    "h": helpCommands,
}
commands = {
    "take": take,
    "get": take,
    "drop": drop,
    "look": look,
    "open": openContainer,
    "inventory": inventory,
    "move": movePlayer,
    "help": helpCommands,
}

#! GAME LOOP
roomInfo(playerLocation)
while True:
    # print(f"inv is {[item.name for item in player.inventory]}")
    cmdInput = getUserInput()
    if cmdInput == "q" or cmdInput == "quit":
        quitGame()
        break
    elif cmdInput[0] in moveDir:
        fnToCall = moveDir[cmdInput[0]]
        fnToCall(cmdInput[0])
        continue
    elif cmdInput[0] in commands:
        fnToCall = commands[cmdInput[0]]
        fnToCall(cmdInput[1])
        continue
    else:
        print("Unknown command. Type 'help' for a list of commands")
        continue
