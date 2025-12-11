import json
from typing import Dict, List, Tuple

# Ref: Chapter Four - Abilities
class Character:
    """
    Represents a character in the Special Circumstances RPG.
    This class holds all data and logic related to a character's sheet.
    """

    def __init__(self):
        # Basic Info
        self.name: str = "New Agent"
        self.pronouns: str = ""
        self.concept: str = ""

        # Ref: Chapter Four - Abilities
        self.abilities: Dict[str, int] = {
            "Will": 3,
            "Health": 5,
            "Resources": 1,
            "Circles": 1,
            "Mindchip": 1,
        }

        # Ref: Chapter Five - Skills
        self.skills: Dict[str, int] = {
            # Crafting & Technical
            "Electronics": 0, "Mechanics": 0, "Engineering": 0, "Computer": 0,
            "Comms": 0, "Gravitics": 0, "Demolitions": 0, "Screens": 0,
            # Exploration & Survival
            "Athletics": 0, "Zero-G": 0, "Survival": 0, "Recon": 0, "Navigation": 0,
            "Grav Vehicle": 0, "Wheeled Vehicle": 0, "Tracked Vehicle": 0, "Riding": 0,
            "Winged Aircraft": 0, "Rotor Aircraft": 0, "Motorboats": 0, "Ocean Ships": 0,
            "Sailing Ships": 0, "Submarine": 0, "Mole": 0,
            # Social & Interpersonal
            "Leadership": 0, "Instruction": 0, "Barter": 0, "Diplomacy": 0, "Etiquette": 0,
            "Streetwise": 0, "Intimidation": 0, "Deception": 0, "Seduction": 0,
            "Performance": 0, "Empathy": 0, "Willpower": 0,
            # Lore & Knowledge
            "Ecology": 0, "Genetics": 0, "Botanics": 0, "Zoology": 0, "Mathematics": 0,
            "Chemistry": 0, "Geology":-1, "Physics": 0, "History": 0, "Psychology": 0,
            "Economics": 0, "Sociology": 0, "Astronomy": 0, "First Aid": 0, "Surgery": 0,
            "Pharmacology": 0, "Linguistics": 0, "Military Strategy": 0, "Combat Tactics": 0,
            "Veterinary Medicine": 0,
            # Combat
            "Archery": 0, "Bludgeoning Weapons": 0, "Natural Weapons": 0, "Piercing Weapons": 0,
            "Slashing Weapons": 0, "Shotgun": 0, "Slug Pistol": 0, "Slug Rifle": 0,
            "Energy Pistol": 0, "Energy Rifle": 0, "Heavy Weapons": 0, "Mounted Weapons": 0,
            "Battle Dress": 0,
        }

        # For tracking skill advancement
        self.skill_tests: Dict[str, Dict[str, int]] = {}

        # Ref: Chapter Two - Trait Pairs
        self.trait_pairs: List[Dict[str, str]] = []

        # Meta-Currency
        self.intervention_tokens: int = 0
        self.hero_tokens: int = 0

        # Ref: Chapter Eight - Conditions
        self.conditions: Dict[str, bool] = {
            "Hungry / Thirsty": False,
            "Tired": False,
            "Sad": False,
            "Angry": False,
            "Afraid": False,
            "Sick": False,
            "Hurt": False,
            "Mentally Fractured": False,
            "Severely Injured": False,
        }
        
        self.homeworld: str = ""
        self.upbringing: str = ""
        self.lifepaths: List[str] = []
        self.beliefs: str = ""
        self.instincts: str = ""
        self.goals: str = ""
        
        self.inventory: List[str] = []
        self.notes: str = ""


    def to_json(self) -> str:
        """Serializes the character data to a JSON string."""
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    @classmethod
    def from_json(cls, json_string: str):
        """Deserializes a character from a JSON string."""
        data = json.loads(json_string)
        char = cls()
        char.__dict__.update(data)
        
        # Ensure skill_tests exists and migrate format if necessary
        if not hasattr(char, 'skill_tests'):
            char.skill_tests = {}
        
        for skill, tests in list(char.skill_tests.items()):
            if isinstance(tests, int):
                char.skill_tests[skill] = {"successes": tests, "failures": 0}
            elif not isinstance(tests, dict) or "successes" not in tests:
                 char.skill_tests[skill] = {"successes": 0, "failures": 0}
            
        return char

    def get_skill_value(self, skill_name: str) -> int:
        """Returns the value of a skill, returns 0 if not found."""
        return self.skills.get(skill_name, 0)

    def get_ability_value(self, ability_name: str) -> int:
        """Returns the value of an ability, returns 0 if not found."""
        return self.abilities.get(ability_name, 0)