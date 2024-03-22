class Location:
    pass 
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.visited = False

    def __str__(self):
        return f"{self.name}: {self.description}"

    def visit(self):
        self.visited = True
        print(f"You have visited {self.name}.")

    def leave(self):
        self.visited = False
        print(f"You leave {self.name}.")


class WildWestLocation(Location):
    def __init__(self, name, description, inhabitants=[]):
        super().__init__(name, description)
        self.inhabitants = inhabitants

    def describe_inhabitants(self):
        if self.inhabitants:
            print(f"The {self.name} is populated by:")
            for inhabitant in self.inhabitants:
                print(f"- {inhabitant}")
        else:
            print(f"The {self.name} is deserted.")

class WildWestLocation(Location):
    def __init__(self, name, description, inhabitants=[]):
        super().__init__(name, description)
        self.inhabitants = inhabitants

    def describe_inhabitants(self):
        if self.inhabitants:
            print(f"The {self.name} is populated by:")
            for inhabitant in self.inhabitants:
                print(f"- {inhabitant}")
        else:
            print(f"The {self.name} is deserted.")

    def describe(self):
        print(f"You are in {self.name}. {self.description}")
        self.describe_inhabitants()


class Saloon(WildWestLocation):
    def __init__(self):
        name = "Saloon"
        description = "A lively saloon with swinging doors, poker tables, and the smell of whiskey."
        inhabitants = ["Bartender", "Card players", "Saloon girls"]
        super().__init__(name, description, inhabitants)

    def interact(self):
        print("You can order a drink, play some cards, or chat with the locals.")


class OutlawCamp(WildWestLocation):
    def __init__(self):
        name = "Outlaw Camp"
        description = "A makeshift campsite hidden in a rocky canyon, with tents and a campfire."
        inhabitants = ["Outlaws", "Horses", "Wanted posters"]
        super().__init__(name, description, inhabitants)

    def interact(self):
        print("You should be cautious here. Outlaws might not take kindly to strangers.")


class GhostTown(WildWestLocation):
    def __init__(self):
        name = "Ghost Town"
        description = "An abandoned town with dilapidated buildings, tumbleweeds rolling by, and an eerie silence."
        inhabitants = []
        super().__init__(name, description, inhabitants)

    def interact(self):
        print("The ghostly atmosphere sends shivers down your spine. There's an air of mystery here.")
