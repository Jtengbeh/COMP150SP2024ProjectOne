from enum import Enum
from typing import List
import random
import sys


class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.events = []
        self.events_we_have_seen = []

    def add_event(self, event):
        self.events.append(event)

    def describe_location(self):
        print(f"{self.name}: {self.description}")

    def get_event(self):
        event = self.events.pop(0)
        self.events_we_have_seen.append(event)
        return event


class WildWestLocation(Location):
    def __init__(self, name, description, inhabitants=None):
        super().__init__(name, description)
        if inhabitants is None:
            inhabitants = []
        self.inhabitants = inhabitants
        self.visited = True  # Marking the location as visited to show the welcome message

    def describe_location(self):
        print("Welcome to the Wild West!")
        print(f"{self.name}: {self.description}")

    def describe_inhabitants(self):
        if self.inhabitants:
            print(f"The {self.name} is populated by:")
            for inhabitant in self.inhabitants:
                print(f"- {inhabitant}")
        else:
            print(f"The {self.name} is deserted.")


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Event:
    def __init__(self, parser, data: dict = None):
        self.parser = parser
        # parse json file
        if data:
            self.primary = data.get('primary_attribute')
            self.secondary = data.get('secondary_attribute')
            self.prompt_text = data.get('prompt_text')
            self.pass_ = data.get('pass')
            self.fail = data.get('fail')
            self.partial_pass = data.get('partial_pass')

        self.status = EventStatus.UNKNOWN
        self.default_fail_message = {"message": "You failed."}
        self.default_pass_message = {"message": "You passed."}
        self.default_partial_pass_message = {"message": "You partially passed."}
        self.prompt_text = "A dragon appears, what will you do?"

        self.primary_statistic = Attribute(0)
        self.secondary_statistic = Attribute(0)

    def execute(self, party):
        chosen_one = self.parser.select_party_member(party)
        chosen_skill = self.parser.select_skill(chosen_one)

        self.resolve_choice(party, chosen_one, chosen_skill)

    def set_status(self, status: EventStatus = EventStatus.UNKNOWN):
        self.status = status

    def resolve_choice(self, party, character, chosen_skill):
        if self.primary == chosen_skill.__class__.__name__ and self.secondary == chosen_skill.__class__.__name__:
            self.set_status(EventStatus.PASS)
            print(self.pass_)
        elif self.primary == chosen_skill.__class__.__name__ or self.secondary == chosen_skill.__class__.__name__:
            self.set_status(EventStatus.PARTIAL_PASS)
            print(self.partial_pass)
        else:
            self.set_status(EventStatus.FAIL)
            print(self.fail)


class Character:
    def __init__(self, name: str = None):
        """
        Core Stats: Everyone has these attributes.
        - Strength: How much you can lift. How strong you are. How hard you punch, etc.
        - Dexterity: How quick your limbs can perform intricate tasks. How adept you are at avoiding blows you anticipate. Impacts speed.
        - Constitution: The body's natural armor. Characters may have unique positive or negative constitutions that provide additional capabilities.
        - Vitality: A measure of how lively you feel. How many Hit Points you have. An indirect measure of age.
        - Endurance: How fast you recover from injuries. How quickly you recover from fatigue.
        - Intelligence: How smart you are. How quickly you can connect the dots to solve problems. How fast you can think.
        - Wisdom: How effectively you can make choices under pressure. Generally low in younger people.
        - Knowledge: How much you know? This is a raw score for all knowledge. Characters may have specific areas of expertise with a bonus or deficit in some areas.
        - Willpower: How quickly or effectively the character can overcome natural urges. How susceptible they are to mind control.
        - Spirit: Catchall for ability to perform otherworldly acts. High spirit is rare. Different skills have different resource pools they might use like mana, stamina, etc. These are unaffected by spirit.
        Instead, spirit is a measure of how hard it is to learn new otherworldly skills and/or master general skills.
        """
        self.name = self._generate_name() if name is None else name
        self.strength = Strength(0)
        self.dexterity = Dexterity(0)
        self.constitution = Constitution(0)
        self.vitality = Vitality(0)
        self.endurance = Endurance(0)
        self.intelligence = Intelligence(0)
        self.wisdom = Wisdom(0)
        self.knowledge = Knowledge(0)
        self.willpower = Willpower(0)
        self.spirit = Spirit(0)

    def _generate_name(self):
        return "Unnamed Character"


class Sheriff(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(90)
        self.dexterity = Dexterity(90)
        self.constitution = Constitution(90)
        self.vitality = Vitality(75)
        self.endurance = Endurance(85)
        self.intelligence = Intelligence(60)
        self.wisdom = Wisdom(60)
        self.knowledge = Knowledge(60)
        self.willpower = Willpower(90)
        self.spirit = Spirit(90)


class Outlaw(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(90)
        self.dexterity = Dexterity(90)
        self.constitution = Constitution(100)
        self.vitality = Vitality(50)
        self.endurance = Endurance(75)
        self.intelligence = Intelligence(70)
        self.wisdom = Wisdom(50)
        self.knowledge = Knowledge(70)
        self.willpower = Willpower(50)
        self.spirit = Spirit(50)


class Bartender(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(80)
        self.dexterity = Dexterity(90)
        self.constitution = Constitution(85)
        self.vitality = Vitality(75)
        self.endurance = Endurance(75)
        self.intelligence = Intelligence(90)
        self.wisdom = Wisdom(80)
        self.knowledge = Knowledge(90)
        self.willpower = Willpower(75)
        self.spirit = Spirit(80)


class Snake(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(80)
        self.dexterity = Dexterity(60)
        self.constitution = Constitution(90)
        self.vitality = Vitality(50)
        self.endurance = Endurance(30)
        self.intelligence = Intelligence(20)
        self.wisdom = Wisdom(5)
        self.knowledge = Knowledge(5)
        self.willpower = Willpower(50)
        self.spirit = Spirit(50)


class Bandit(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(65)
        self.dexterity = Dexterity(90)
        self.constitution = Constitution(100)
        self.vitality = Vitality(50)
        self.endurance = Endurance(75)
        self.intelligence = Intelligence(30)
        self.wisdom = Wisdom(50)
        self.knowledge = Knowledge(30)
        self.willpower = Willpower(50)
        self.spirit = Spirit(50)


class Doctor(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(40)
        self.dexterity = Dexterity(90)
        self.constitution = Constitution(60)
        self.vitality = Vitality(50)
        self.endurance = Endurance(75)
        self.intelligence = Intelligence(90)
        self.wisdom = Wisdom(75)
        self.knowledge = Knowledge(90)
        self.willpower = Willpower(50)
        self.spirit = Spirit(90)


class Mayor(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(95)
        self.dexterity = Dexterity(90)
        self.constitution = Constitution(100)
        self.vitality = Vitality(85)
        self.endurance = Endurance(75)
        self.intelligence = Intelligence(90)
        self.wisdom = Wisdom(80)
        self.knowledge = Knowledge(90)
        self.willpower = Willpower(50)
        self.spirit = Spirit(50)


class Deputy(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(65)
        self.intelligence = Intelligence(90)
        self.charisma = Charisma(90)
        self.knowledge = Knowledge(90)
        self.endurance = Endurance(75)
        self.dexterity = Dexterity(80)
        self.willpower = Willpower(60)
        self.spirit = Spirit(80)
        self.wisdom = Wisdom(60)
        self.constitution = Constitution(75)
        self.vitality = Vitality(80)


class Horse(Character):
    def __init__(self, name: str = None):
        super().__init__(name)
        self.strength = Strength(80)
        self.intelligence = Intelligence(5)
        self.charisma = Charisma(90)
        self.knowledge = Knowledge(5)
        self.endurance = Endurance(90)
        self.dexterity = Dexterity(80)
        self.willpower = Willpower(60)
        self.spirit = Spirit(80)
        self.wisdom = Wisdom(5)
        self.constitution = Constitution(90)
        self.vitality = Vitality(80)


class Game:
    def __init__(self, parser):
        self.parser = parser
        self.characters: List[Character] = []
        self.locations: List[Location] = []
        self.events: List[Event] = []
        self.party: List[Character] = []
        self.current_location = None
        self.current_event = None
        self.continue_playing = True

        self._initialize_game()

    def add_character(self, character: Character):
        """Add a character to the game."""
        self.characters.append(character)

    def add_location(self, location: Location):
        """Add a location to the game."""
        self.locations.append(location)

    def add_event(self, event: Event):
        """Add an event to the game."""
        self.events.append(event)

    def _initialize_game(self):
        sheriff = Sheriff()
        outlaw = Outlaw()
        bartender = Bartender()
        snake = Snake()
        bandit = Bandit()
        doctor = Doctor()
        mayor = Mayor()
        deputy = Deputy()
        horse = Horse()

        self.add_character(sheriff)
        self.add_character(outlaw)
        self.add_character(bartender)
        self.add_character(snake)
        self.add_character(bandit)
        self.add_character(doctor)
        self.add_character(mayor)
        self.add_character(deputy)
        self.add_character(horse)

        saloon = WildWestLocation("Saloon", "A lively saloon filled with patrons and music.")
        jail = WildWestLocation("Jail", "A dusty jail with empty cells.")

        self.add_location(saloon)
        self.add_location(jail)

        event1 = Event(self.parser, {"primary_attribute": "Strength", "secondary_attribute": "Dexterity",
                                     "prompt_text": "A bar fight breaks out. What do you do?",
                                     "pass": "You successfully break up the fight.",
                                     "fail": "You get caught in the middle of the fight.",
                                     "partial_pass": "You manage to dodge the punches but fail to stop the fight."})
        event2 = Event(self.parser, {"primary_attribute": "Intelligence", "secondary_attribute": "Wisdom",
                                     "prompt_text": "A mysterious stranger offers you a secret job. What do you do?",
                                     "pass": "You wisely decline the offer, sensing something isn't right.",
                                     "fail": "You accept the job, not realizing it's a setup.",
                                     "partial_pass": "You hesitate, asking for more information before deciding."})

        saloon.add_event(event1)
        jail.add_event(event2)

        self.party = [sheriff, outlaw, bartender]

    def start_game(self):
        return self._main_game_loop()

    def _main_game_loop(self):
        """The main game loop."""
        print("Welcome to the Wild West Adventure Game!")
        print("You are the sheriff in town. Your job is to keep peace and order.")
        print("Type 'help' at any time to see available commands.\n")

        while self.continue_playing:
            self._check_current_state()
            self._get_user_input()

    def _check_current_state(self):
        """Check the current state of the game."""
        if not self.current_location:
            self.current_location = random.choice(self.locations)

        if not self.current_event:
            self.current_event = self.current_location.get_event()

        if not self.party:
            print("Game over. Your party has been defeated.")
            self.continue_playing = False

    def _get_user_input(self):
        """Get user input."""
        user_input = input(f"\nWhat would you like to do? ").strip().lower()

        if user_input == 'help':
            self._show_help()
        elif user_input == 'quit':
            self._quit_game()
        elif user_input == 'status':
            self._show_status()
        elif user_input == 'look':
            self._look_around()
        elif user_input == 'event':
            self._show_event()
        elif user_input == 'execute':
            self._execute_event()
        else:
            print("Unknown command. Type 'help' to see available commands.")

    def _show_help(self):
        """Display help information."""
        print("Available commands:")
        print("- help: Show available commands")
        print("- quit: Quit the game")
        print("- status: Show party status")
        print("- look: Look around the current location")
        print("- event: Show details of the current event")
        print("- execute: Execute the current event")

    def _quit_game(self):
        """Quit the game."""
        print("Quitting the game.")
        sys.exit()

    def _show_status(self):
        """Show party status."""
        print("\nParty Status:")
        for character in self.party:
            print(f"- {character.name}")

    def _look_around(self):
        """Look around the current location."""
        print("\nYou look around...")
        self.current_location.describe_location()

    def _show_event(self):
        """Show details of the current event."""
        print("\nCurrent Event:")
        print(self.current_event.prompt_text)

    def _execute_event(self):
        """Execute the current event."""
        print("\nExecuting event...")
        self.current_event.execute(self.party)
        if self.current_event.status == EventStatus.PASS:
            print(self.current_event.default_pass_message)
        elif self.current_event.status == EventStatus.FAIL:
            print(self.current_event.default_fail_message)
        elif self.current_event.status == EventStatus.PARTIAL_PASS:
            print(self.current_event.default_partial_pass_message)
        self.current_event = None


class Attribute:
    def __init__(self, value: int):
        self.value = value


class Strength(Attribute):
    pass


class Dexterity(Attribute):
    pass


class Constitution(Attribute):
    pass


class Vitality(Attribute):
    pass


class Endurance(Attribute):
    pass


class Intelligence(Attribute):
    pass


class Wisdom(Attribute):
    pass


class Knowledge(Attribute):
    pass


class Willpower(Attribute):
    pass


class Spirit(Attribute):
    pass


class Charisma(Attribute):
    pass


class CommandParser:
    @staticmethod
    def select_party_member(party):
        return random.choice(party)

    @staticmethod
    def select_skill(character):
        return random.choice([attribute for attribute in character.__dict__.values() if isinstance(attribute, Attribute)])


if __name__ == "__main__":
    game = Game(CommandParser())
    game.start_game()

