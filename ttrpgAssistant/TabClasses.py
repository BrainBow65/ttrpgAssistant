import sys
import os
import random
import string
import glob
import yaml
import re
from pathlib import Path
from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QLineEdit, QTextEdit

class CoreRulebookValues(QWidget):
    FOLDER_PATH = "C:/Users/Michelle/Documents/Obsidian Notes/StargateTTRPG/Planets"
    GEO_FEATURES = ["Anticline", "Basin", "Butte", "Cave", "Cliff", "Canyon", "Valley", "Bay", "Archipelago"]
    BIOMES = ["Arboreal", "Artificial", "Desert", "Grasslands", "Lunar", "Mountainous", "Oceanic", "Rainforest", "Starship", "Terraformed", "Toxic", "Tundra", "Subterranean", "Swamp", "Urban", "Volcanic"]
    ALIEN_TYPES = ["Human", "Asgaridan", "Androids", "Aris bochs people", "Reol", "Nox", "Serrakin", "Mimetic aliens", "reetou", "replicators", "Goa'uld", "Jaffa", "Arturen", "Tok'ra", "Unas", "Unknown"]
    GOV_TYPES = ["Democracy", "Dictatorship", "Theocracy", "Oligarchy", "Communist", "Monarchy", "Fascist", "Military"]
    CULTURE_TYPES = ["National", "Religion", "Ethnic Group", "Social Class", "Generational", "Organizational", "Gender"]
    RELIGION_TYPES = ["Goa'uld", "Asgardism", "Monotheism", "Polytheism, hard", "Polytheism soft", "Polytheism, henotheism", "Polytheism, Kathenotheism", "Polytheism, Monolatrism", "Pantheism", "Deism", "Autotheism", "Value-judgement theism, Eutheism", "Value-judgement theism, dystheism", "Value-judgement theism, maltheism", "Value-judgement theism, misotheism", "Spiritualism", "Atheism"]
    SPECIALABIL = ["amphibious breath", "apex predator", "armoured", "beast of burden", "bioluminescent", "blind sight", "blood frenzy", "camouflage", "charge", "climb", "constrict", "crystalline", "dark vision", "echo location", "extra legs", "fast", "flight", "flightless", "hold breath", "improved ability", "improved attribute", "keen sense", "larger", "lumbering", "mimicry", "move by", "multiattack", "natural weapon", "pack tactics", "pounce", "powerful attack", "proficient", "relentless", "skilled", "spider climb", "standing leap", "superior natural attacks", "sure-footed", "swarm", "swimmer", "tough", "venomous", "webbing"]
    #stats organized {CR: [prof., size, str, dex, con, int, wis, cha, ac, hp, speed, dmg]}  
    BEAST_STATS_DICT = {0:[0, "Tiny", 2, 16, 6, 1, 10, 2, 12, 1, 4, "1d2"],
                  0.125:[1, 'Tiny', 3, 16, 6, 1, 10, 2, 12, 3, 4, '1d2'],
                  0.25:[1, 'Tiny', 4, 16, 6, 1, 10, 2, 12, 7, 4, '1d3'],
                  0.5:[1, 'Tiny', 5, 16, 6, 1, 10, 2, 12, 10, 4, '1d3'],
                  1:[2, 'Small', 6, 14, 8, 1, 10, 2, 12, 15, 6, '1d4'],
                  2:[],
                  3:[],
                  4:[],
                  5:[],
                  6:[],
                  7:[],
                  8:[],
                  9:[],
                  10:[],
                  11:[],
                  12:[],
                  13:[],
                  14:[],
                  15:[],
                  16:[],
                  17:[],
                  18:[],
                  19:[],
                  20:[]}
    BEAST_TYPES = ['amphibious', 'aquatic', 'avian', 'biped', 'crustacean', 'insect', 'quadruped', 'serpentine']
    #vehicle attributes dictionary structure: {'vehicle':[techlvl, handling, type, speed(kph), passengers, hp, ac, size]}
    VEHICLE_ATTRIBUTES = {'ATV':[2, 12, 'off-road', 100, 2, 60, 18, 'medium'],
                          'Apache':[],
                          'F-302':[],
                          'Fixed-Wing':[],
                          'F.R.E.D.':[],
                          'Inflatable Boat':[],
                          'Jeep':[],
                          'M1 Tank':[],
                          'M706':[],
                          'M.A.L.P.':[],
                          'Motorcycle':[],
                          'Passenger Sedan':[],
                          'U.A.V.':[]}
    #vehicle weapons dictionary structure: {'weapon':[techlvl, damage die, type, range, cpaacity, special]}
    VEHICLE_WEAPONS={'Autocannon':[2, '8d6', 'piercing', '100m/1km', 50, None],
                     'Bomb':[2, '20d6', 'explosive', '', 5, 'see text?'],
                     'Missile': [2, '20d6', 'explosive', '5km/200km', 4, 'guided'],
                     'Railgun':[3, '8d6', 'piercing', '5km/400km',100, None]}
    
    def __init__(self):
        super().__init__()

class Registry:
    instances = {}
    directory = 'c:/Users/Michelle/Documents/Obsidian Notes/StargateTTRPG/GameObjects' 
    
    @staticmethod
    def add_instance(instance):
        instance_class = type(instance).__name__
        if instance_class not in Registry.instances:
            Registry.instances[instance_class] = []
        Registry.instances[instance_class].append(instance)

    @staticmethod
    def save_instances(directory):
        for instance_class, instances in Registry.instances.items():
            class_directory = os.path.join(directory, instance_class)
            os.makedirs(class_directory, exist_ok=True)
            for instance in instances:
                filename = os.path.join(class_directory, f'{instance.name}.md')
                front_matter = {attr: value for attr, value in instance.__dict__.items() if attr != 'name'}
                # Read the existing content
                with open(filename, 'r') as file:
                    content = file.read()
                    match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
                    if match:
                        # Update the front matter
                        content = content.replace(match.group(0), f'---\n{yaml.dump(front_matter)}---\n')
                    else:
                        # Add the front matter if it doesn't exist
                        content = f'---\n{yaml.dump(front_matter)}---\n{content}'
                # Write the updated content back to the file
                with open(filename, 'w') as file:
                    file.write(content)

    @staticmethod
    def load_instances(directory):
        Registry.instances = {}
        for class_directory in glob.glob(os.path.join(directory, '*')):
            instance_class = os.path.basename(class_directory)
            Registry.instances[instance_class] = []
            for filename in glob.glob(os.path.join(class_directory, '*.md')):
                with open(filename, 'r') as file:
                    content = file.read()
                    match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
                    if match:
                        # Load the front matter
                        front_matter = yaml.load(match.group(1), Loader=yaml.FullLoader)
                        # Create an instance of the class
                        instance_class_obj = globals()[instance_class]
                        instance = instance_class_obj(**front_matter)
                        Registry.instances[instance_class].append(instance)

class SocietyGenerator(CoreRulebookValues):
    def __init__(self):
        super().__init__()
        CURRENTALIABIL = []
        layout = QVBoxLayout()
        self.generate_button = QPushButton("Generate Society")
        layout.addWidget(self.generate_button)
        
        self.file_name_input = QLineEdit()
        layout.addWidget(self.file_name_input)
        
        self.message_label = QLabel()
        layout.addWidget(self.message_label)

        self.setLayout(layout)
        self.generate_button.clicked.connect(self.generate_society)

    def choose_random_value(self, source_list):
        return random.choice(source_list)
    
    def generate_random_values(self, CURRENTALIABIL):
        govNum = random.randint(1, 5)
        religNum = random.randint(1, 5)
        currentTechLvl = [random.randint(1, 5)]
        currentAlien = [self.choose_random_value(CoreRulebookValues.ALIEN_TYPES) if random.random() < 0.7 else CoreRulebookValues.ALIEN_TYPES[0]]
        currentGovType = [self.choose_random_value(CoreRulebookValues.GOV_TYPES) for _ in range(govNum)]
        currentCulture = [self.choose_random_value(CoreRulebookValues.CULTURE_TYPES) for _ in range(govNum)]
        currentRelig = [self.choose_random_value(CoreRulebookValues.RELIGION_TYPES) for _ in range(religNum)]

        if "Unknown" in currentAlien:
            Alien = CURRENTALIABIL
        else:
            Alien = currentAlien

        while len(currentTechLvl) < govNum:
            last_value = currentTechLvl[-1]
            if random.random() < 0.8:
                currentTechLvl.append(last_value)
            else:
                currentTechLvl.append(random.randint(1, 5))

        return Alien, currentTechLvl, currentGovType, currentCulture, currentRelig

    def AlienSpeciesGenerator(self, CURRENTALIABIL):
        num_values = random.randint(1, 2)
        chosen_values = random.sample(CoreRulebookValues.ALIEN_TYPES, num_values)
        CURRENTALIABIL.extend(chosen_values)
        return CURRENTALIABIL
    
    def search_markdown_file(self, file_name, folder_path):
        for file in os.listdir(folder_path):
            if file.lower().startswith(file_name.lower()) and file.lower().endswith(".md"):
                return os.path.join(folder_path, file)
        return None
    def append_to_markdown_file(self, file_path, contents):
        with open(file_path, "a") as file:
            file.write(contents)
   
    def generate_society(self):
        Alien, currentTechLvl, currentGovType, currentCulture, currentRelig = self.generate_random_values()
        file_name = self.file_name_input.text()
    
        if not file_name:
            self.message_label.setText("Please enter a file name.")
            return
    
        file_name += ".md"
    
        existing_file_path = self.search_markdown_file(file_name, CoreRulebookValues.FOLDER_PATH)
    
        if existing_file_path is not None:
            self.append_to_markdown_file(existing_file_path, "contents")
            self.AlienSpeciesGenerator()
            if Alien[0] == "Unknown":
                self.AlienSpeciesGenerator()
            contents = f"\nThis planet is inhabited by: {', '.join(Alien)} \nThis planet's governments have ': {', '.join(currentTechLvl)} tech level\nThe government types are: {', '.join(currentGovType)}\nThe types of cultures are: {', '.join(currentCulture)}\nThe religions on this planet are: {', '.join(currentRelig)}"
            self.append_to_markdown_file(existing_file_path, contents)
            self.message_label.setText(f"the following has been appended '{existing_file_path}'")
        else:  
            self.message_label.setText(f"The file '{file_name}.md' could not be found in '{CoreRulebookValues.FOLDER_PATH}'.")

class PlanetGenerator(CoreRulebookValues):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        self.generate_button = QPushButton("Generate Planet")
        layout.addWidget(self.generate_button)

        # Create a QLabel to display the message
        self.message_label = QLabel()
        layout.addWidget(self.message_label)

        self.setLayout(layout)

        self.generate_button.clicked.connect(self.generate_planet)
    
    def choose_geography(self):
        num_values = random.randint(2, 6)
        currentGeoFeatures = random.sample(self.geoFeatures, num_values)
        return currentGeoFeatures
    
    def choose_biome(self):
        return random.choice(CoreRulebookValues.BIOMES)
    
    def generate_name(self):
        prefix = "P"
        middle = random.choices(string.ascii_uppercase + string.digits, k=2)
        suffix = str(random.randint(0, 999)).zfill(3)
        return f"{prefix}{middle[0]}{middle[1]}-{suffix}.md"
    
    def check_name_availability(self, name, folder_path):
        for filename in os.listdir(folder_path):
            if filename.startswith(name[:7]):
                return False
        return True
    
    def generate_unique_name(self, folder_path):
        while True:
            name = self.generate_name()
            if self.check_name_availability(name, folder_path):
                return name
    
    def create_planet_file(self, content, name, folder_path):
        file_name = name
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "a") as file:
            file.write(content)
        return file_name

    def generate_planet(self):
        currentGeoFeatures = self.choose_geography()
        currentBiome = self.choose_biome()

        name = self.generate_name()
        while not self.check_name_availability(name, CoreRulebookValues.FOLDER_PATH):  # Pass FOLDER_PATH as the second argument
            name = self.generate_name()

        unique_name = self.generate_unique_name(CoreRulebookValues.FOLDER_PATH)  # Pass FOLDER_PATH as an argument
        markdown_content = f"The new planet's biome is {currentBiome}\nThe nearby geological features are: {currentGeoFeatures}"
        file_name = self.create_planet_file(markdown_content, unique_name, CoreRulebookValues.FOLDER_PATH)  # Pass FOLDER_PATH as an argument

        with open('C:/Users/Michelle/Documents/Obsidian Notes/StargateTTRPG/Planets/PJL-369.md', 'r') as f:
            markdown_text = f.read()
        self.text_edit.setMarkdown(markdown_text)
        # Update the QLabel with the message
        self.message_label.setText(f"Markdown file '{file_name}' created in '{CoreRulebookValues.FOLDER_PATH}'")

class ConvinceEncounter(CoreRulebookValues):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.generate_button = QPushButton("Run Convince Encounter")
        layout.addWidget(self.generate_button)

        self.generate_button.clicked.connect(self.convince_encounter)

        self.setLayout(layout)
    
    def update_threshold(self, condition):
        if condition == "less":
            return 4
        elif condition == "equal":
            return 5
        elif condition == "greater":
            return 6
        
    def update_threshold_with_value(self, threshold, value):
        return threshold + value
    
    def update_determination_point_wager(self, determination_point_wager):
        return determination_point_wager + 1
    
    def calculate_round_result(self, threshold, determination_point_wager, num_players):
        successes = int(input("Enter the number of successes: "))
        failures = int(input("Enter the number of failures: "))

        threshold[0] -= successes

        if failures > 0:
            print(f"{failures} player(s) should lose {determination_point_wager} determination points")

        print("Current Determination Point Wager:", determination_point_wager)
        print("Current Threshold:", threshold[0])

        if threshold[0] <= 0:
            print("Success!")
            return True
        return False
    
    def convince_encounter(self):
        threshold = [0]
        determination_point_wager = 0

        condition = input("Is the CR less, equal, or greater than the PC's level? ")
        threshold[0] = self.update_threshold(condition)

        noteworthy = input("Is the foe noteworthy or the idea outrageous? (yes/no) ")
        if noteworthy.lower() == "yes":
            value = int(input("Enter a numerical value to add to the threshold level (1 or 2): "))
            threshold[0] = self.update_threshold_with_value(threshold[0], value)

        while True:
            determination_point_wager = self.update_determination_point_wager(determination_point_wager)

            num_players = int(input("Enter the number of players participating: "))

            total_successes = int(input("Enter the total number of critical successes: "))
            total_failures = int(input("Enter the total number of critical failures: "))

            threshold[0] -= (2 * total_successes)
            threshold[0] += total_failures

            if self.calculate_round_result(threshold, determination_point_wager, num_players):
                break

class DiplomaticEncounter(CoreRulebookValues):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        generate_button = QPushButton("Run Diplomatic Function")
        layout.addWidget(generate_button)
        generate_button.clicked.connect(self.diplomatic_function)

        self.setLayout(layout)

    def moxie_roll(self, name):
        return random.randint(1, 20)
    
    def choose_diplomatic_action(self, name):
        print(f"Possible diplomatic actions: ingratiate, assist, persuade, obfuscate, inquire, thwart")
        return input(f"Enter the diplomatic action for {name}: ")
    
    def choose_assisted_player(self, players):
        print("Choose a player to assist:")
        for i, player in enumerate(players):
            print(f"{i + 1}. {player}")
        while True:
            choice = input()
            for player in players:
                if player["name"] == choice:
                    return player
            print("Invalid choice. Please enter a valid player name.")
    
    def choose_thwarted_player(self, players, antagonists):
        print("Choose a player or antagonist to thwart:")
        all_participants = players + antagonists
        for i, participant in enumerate(all_participants):
            print(f"{i + 1}. {participant}")
        while True:
            choice = input()
            for participant in all_participants:
                if participant["name"] == choice:
                    return participant
            print("Invalid choice. Please enter a valid player name.")
    
    def resolve_round(self, players, antagonists):
        for participant in sorted(players + antagonists, key=lambda p: p["moxie"], reverse=True):
            print(f"Current participant: {participant['name']}")

            if participant.get("wagered_dp") and participant.get("diplomatic_action") == "thwart":
                continue

            if participant.get("wagered_dp") and participant.get("diplomatic_action") != "thwart":
                print("Player gains advantage on checks for the round")

            if participant.get("assisted"):
                print(f"{participant['name']} has advantage on checks for the round")

            if participant.get("thwarted"):
                print(f"{participant['name']} has disadvantage on checks for the round")

            diplomatic_action = participant["diplomatic_action"]
            if diplomatic_action == "ingratiate":
                print("Player gains 1 DP")
                continue
            elif diplomatic_action == "assist":
                continue
            elif diplomatic_action == "thwart":
                continue
    
            result = input("Did the participant succeed or fail? (success/fail): ")
            if result == "fail" and participant.get("wagered_dp") and diplomatic_action in ["persuade", "obfuscate", "inquire"]:
                print("Player loses a determination point")

            if result == "succeed":
                if diplomatic_action == "persuade":
                    print(f"You change {participant['name']}'s disposition, but strongly held beliefs are only changed for the duration of the encounter")
                elif diplomatic_action == "obfuscate":
                    print("All checks made to inquire about the chosen topic suffer disadvantage for the round")
                elif diplomatic_action == "inquire":
                    print("You learn the answer to a question with a discrete answer")

                if participant.get("thwarted"):
                    print(f"The participant who chose to thwart {participant['name']} should lose a DP")

    def diplomatic_function(self):
        num_players = int(input("Enter the number of players: "))
        players = []
        for _ in range(num_players):
            player_name = input("Enter the name of a player: ")
            players.append({"name": player_name, "moxie": 0})

        num_antagonists = int(input("Enter the number of antagonists: "))
        antagonists = []
        for _ in range(num_antagonists):
            antagonist_name = input("Enter the name of an antagonist: ")
            antagonists.append({"name": antagonist_name, "moxie": 0})

        while True:
            for player in players:
                player["moxie"] = self.moxie_roll(player["name"])

            for antagonist in antagonists:
                antagonist["moxie"] = self.moxie_roll(antagonist["name"])

            for participant in players + antagonists:
                participant["diplomatic_action"] = self.choose_diplomatic_action(participant["name"])

                if participant["diplomatic_action"] == "assist":
                    participant["assisted"] = self.choose_assisted_player(players)["name"]
                elif participant["diplomatic_action"] == "thwart":
                    has_dp = input("Does the participant have a DP? (yes/no): ")
                    if has_dp == "yes":
                        participant["wagered_dp"] = True
                    participant["thwarted"] = self.choose_thwarted_player(players, antagonists)["name"]

            self.resolve_round(players, antagonists)

            another_round = input("Do you want to play another round? (yes/no): ")
            if another_round == "no":
                break
    
class InfiltrationEncounter(CoreRulebookValues):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle("Slider Demo")
        self.setGeometry(100, 100, 400, 150)
        self.slider = QSlider(Qt.Vertical)
        self.slider.setRange(0, 4)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)

        self.slider.valueChanged.connect(self.slider_changed)

        self.label = QLabel("Oblivious")

        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        self.setLayout(layout)  # Set the layout for this specific CoreRulebookValues

    def slider_changed(self):
        positions = ["Oblivious", "Suspicious", "Investigating", "Alarmed", "Chasing"]
        value = self.slider.value()
        self.label.setText(f"{positions[value]}")
        return value # important for save state tracking

class Character:
    def __init__(self, name, race, npc_class, lvl, hp, ac, speed, str, dex, con, int, wis, cha, skills, proficiency_mod, saves, feats, field_hacks, gear, attacks):
        self.name = name
        self.race = race
        self.npc_class = npc_class
        self.lvl = lvl
        self.hp = hp
        self.ac = ac
        self.speed = speed
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha
        self.skills = skills
        self.saves = saves
        self.feats = feats
        self.field_hacks = field_hacks
        self.gear = gear
        self.attacks = attacks
        self.proficiency_mod = proficiency_mod

class NPC(Character):
    def __init__(self):
        super().__init__()



class Beast(CoreRulebookValues):
    
    def __init__(self, name, cr, size, type, hp, ac, str, dex, con, int, wis, cha, skills, proficiency_mod, saves, abilities, attacks):
        self.name = name
        self.cr = cr #challenge rating
        self.size = size
        self.type = type
        self.hp = hp
        self.ac = ac
        self.str = str
        self.dex = dex
        self.con = con
        self.int = int
        self.wis = wis
        self.cha = cha
        self.skills = skills
        self.proficiency_mod = proficiency_mod
        self.saves = saves
        self.abilities = abilities
        self.attacks = attacks

    
    def beak():
        dmg_type = 'slashing'
    
    def bite():
        dmg_type = 'piercing'
    
    def claw():
        dmg_type = 'slashing'
        quality = 'finesse'
    
    def hoof():
        dmg_type = 'bludgeoning'
    
    def horn():
        dmg_type = 'piercing'
    
    def slam():
        dmg_type = 'bludgeoning'
    
    def sting():
        dmg_type = 'piercing'
        quality = 'finesse'
    
    def tail():
        dmg_type = 'bludgeoning'
    
    def tusk():
        dmg_type = 'slashing'
    
    def wing():
        dmg_type = 'bludgeoning'
    #I need to define all of the atributes of beasts based on their generated markdown files

class Combatant:
    def __init__(self, name, hp, ac, attack_bonus, damage_bonus, initiative):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.ac = ac
        self.attack_bonus = attack_bonus
        self.damage_bonus = damage_bonus
        self.initiative = initiative


    def attack(self, target):
        roll = random.randint(1, 20) + self.attack_bonus
        if roll >= target.ac:
            damage = random.randint(1, 6) + self.damage_bonus
            target.hp -= damage
            print(f"{self.name} attacks {target.name} for {damage} damage.")
        else:
            print(f"{self.name}'s attack misses.")

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} heals for {amount} HP.")

class CombatGenerator:
    pass

class Equipment:
    def __init__(self, name, techlvl, bulk):
        self.name = name
        self.techlvl = techlvl
        self.bulk = bulk

class Weapons(Equipment):
    def __init__(self, dmg, type, capacity, reload, range, special):
        super().__init__()
        self.dmg = dmg
        self.type = type
        self.capacity = capacity
        self.reload = reload
        self.range = range
        self.special = special


class Armor(Equipment):
    def __init__(self, techlvl, type, ac, strength, stealth, bulk, special):
        super().__init__()
        self.techlvl = techlvl
        self.type = type
        self.ac = ac
        self.strength = strength
        self.stealth = stealth
        self.special = special


class Gear(Equipment):
    def __init__(self, techlvl, bulk, description):
        super().__init__()
        self.techlvl = techlvl
        self.description = description


class Facilities:
    def __init__(self, name, bonusrating, bonustype):
        self.name = name
        self.bonusrating = bonusrating
        self.bonustype = bonustype


class Vehicles:
    def __init__(self, name, size, handling, speed, passengers, type, weapons, hp, ac):
        self.name = name
        self.size = size
        self.handling = handling
        self.speed = speed
        self.passengers = passengers
        self.type = type
        self.weapons = weapons
        self.hp = hp
        self.ac = ac