import sys
from typing import List
import random
from enum import Enum

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
        if not self.events:
            return None
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
        self.parser: UserInputParser = parser
        # parse json file
        if data:
            self.primary = data.get('primary_attribute')
            self.secondary = data.get('secondary_attribute')
            self.prompt_text = data.get('prompt_text')
            self.pass_ = data.get('pass')
            self.fail = data.get('fail')
            self.partial_pass = data.get('partial_pass')
        else:
            self.primary = None
            self.secondary = None
            self.prompt_text = "A dragon appears, what will you do?"
            self.pass_ = self.default_pass_message
            self.fail = self.default_fail_message
            self.partial_pass = self.default_partial_pass_message

        self.status = EventStatus.UNKNOWN
        self.default_fail_message = {"message": "You failed."}
        self.default_pass_message = {"message": "You passed."}
        self.default_partial_pass_message = {"message": "You partially passed."}

        self.primary_statistic = None
        self.secondary_statistic = None

    def execute(self, party):
        if not party:
            print("There are no party members to choose from.")
            return

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
        self.wisdom = Wisdom(
