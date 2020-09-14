from item import Item


class Lightsource(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
        super().on_take()
        super().on_drop()
