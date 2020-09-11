# Implement a class to hold room information. This should have name and
# description attributes.


class Room:
    def __init__(self, name, description, items=[]):
        self.name = name
        self.description = description
        self.items = items

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return "Room (%s)" % (self.name)

    def itemList(self):
        if len(self.items) == 0:
            return f"You don't see anything of interest in this room"

        ret = f"In this room you see: "
        for i, v in enumerate(self.items):
            if i == 0:
                ret += f"a {v.name}"
            else:
                ret += f", and a {v.name} "
        return ret
