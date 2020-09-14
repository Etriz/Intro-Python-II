from item import Item


class Container(Item):
    def __init__(self, name, description, inside):
        super().__init__(name, description)
        self.inside = inside

    def __str__(self):
        if len(self.inside) == 0:
            return f"There is nothing inside"
        ret = ""
        for item in self.inside:
            ret += f"a {item.name}"
        return f"Inside you see {ret}, you take everything from inside the {self.name}"
