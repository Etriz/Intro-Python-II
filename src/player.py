# Write a class to hold player information, e.g. what room they are in
# currently.


class Player:
    def __init__(self, current_room, inventory=[]):
        self.current_room = current_room
        self.inventory = inventory

    def __str__(self):
        return f"You are in the {self.current_room} room"

    def __repr__(self):
        return f"This is the {self.current_room}"

    def hasInventory(self):
        if len(self.inventory) == 0:
            return f"You have nothing in your inventory"

        ret = f"You are carrying "
        for i, v in enumerate(self.inventory):
            if i == 0:
                ret += f"a {v.name}"
            else:
                ret += f", and a {v.name} "
        return ret