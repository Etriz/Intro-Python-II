# Implement a class to hold room information. This should have name and
# description attributes.


class Room:
    def __init__(self, name, description, items=[]):
        self.name = name
        self.description = description
        self.item = items

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return "Room (%s)" % (self.name)