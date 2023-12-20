import sys
import os
import random
import string
from pathlib import Path
from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QLineEdit

GEO_FEATURES = ["Anticline", "Basin", "Butte", "Cave", "Cliff", "Canyon", "Valley", "Bay", "Archipelago"]
BIOMES = ["Arboreal", "Artificial", "Desert", "Grasslands", "Lunar", "Mountainous", "Oceanic", "Rainforest", "Starship", "Terraformed", "Toxic", "Tundra", "Subterranean", "Swamp", "Urban", "Volcanic"]
ALIEN_TYPES = ["Human", "Asgaridan", "Androids", "Aris bochs people", "Reol", "Nox", "Serrakin", "Mimetic aliens", "reetou", "replicators", "Goa'uld", "Jaffa", "Arturen", "Tok'ra", "Unas", "Unknown"]
GOV_TYPES = ["Democracy", "Dictatorship", "Theocracy", "Oligarchy", "Communist", "Monarchy", "Fascist", "Military"]
CULTURE_TYPES = ["National", "Religion", "Ethnic Group", "Social Class", "Generational", "Organizational", "Gender"]
RELIGION_TYPES = ["Goa'uld", "Asgardism", "Monotheism", "Polytheism, hard", "Polytheism soft", "Polytheism, henotheism", "Polytheism, Kathenotheism", "Polytheism, Monolatrism", "Pantheism", "Deism", "Autotheism", "Value-judgement theism, Eutheism", "Value-judgement theism, dystheism", "Value-judgement theism, maltheism", "Value-judgement theism, misotheism", "Spiritualism", "Atheism"]
SPECIALABIL = ["amphibious breath", "apex predator", "armoured", "beast of burden", "bioluminescent", "blind sight", "blood frenzy", "camouflage", "charge", "climb", "constrict", "crystalline", "dark vision", "echo location", "extra legs", "fast", "flight", "flightless", "hold breath", "improved ability", "improved attribute", "keen sense", "larger", "lumbering", "mimicry", "move by", "multiattack", "natural weapon", "pack tactics", "pounce", "powerful attack", "proficient", "relentless", "skilled", "spider climb", "standing leap", "superior natural attacks", "sure-footed", "swarm", "swimmer", "tough", "venomous", "webbing"]

FOLDER_PATH = "C:/Users/Michelle/Documents/Obsidian Notes/StargateTTRPG/Planets"
CURRENTALIABIL = []

class SocietyGeneratorTab(QWidget):
    def __init__(self):
        super().__init__()

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
    
    def generate_random_values(self):
        govNum = random.randint(1, 5)
        religNum = random.randint(1, 5)
        currentTechLvl = [random.randint(1, 5)]
        currentAlien = [self.choose_random_value(ALIEN_TYPES) if random.random() < 0.7 else ALIEN_TYPES[0]]
        currentGovType = [self.choose_random_value(GOV_TYPES) for _ in range(govNum)]
        currentCulture = [self.choose_random_value(CULTURE_TYPES) for _ in range(govNum)]
        currentRelig = [self.choose_random_value(RELIGION_TYPES) for _ in range(religNum)]

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

    def AlienSpeciesGenerator(self):
        num_values = random.randint(1, 2)
        chosen_values = random.sample(ALIEN_TYPES, num_values)
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
    
        existing_file_path = self.search_markdown_file(file_name, FOLDER_PATH)
    
        if existing_file_path is not None:
            self.append_to_markdown_file(existing_file_path, "contents")
            self.AlienSpeciesGenerator()
            if Alien[0] == "Unknown":
                self.AlienSpeciesGenerator()
            contents = f"\nThis planet is inhabited by: {Alien} \nThis planet's governments have ': {currentTechLvl} tech level\nThe government types are: {currentGovType}\nThe types of cultures are: {currentCulture}\nThe religions on this planet are: {currentRelig}"
            self.append_to_markdown_file(existing_file_path, contents)
            self.message_label.setText(f"the following has been appended '{existing_file_path}'")
        else:  
            self.message_label.setText(f"The file '{file_name}.md' could not be found in '{FOLDER_PATH}'.")

class PlanetGeneratorTab(QWidget):
    def __init__(self):
        super().__init__()

        self.geoFeatures = GEO_FEATURES
        self.biome = BIOMES

        layout = QVBoxLayout()
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
        return random.choice(self.biome)

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
        while not self.check_name_availability(name, FOLDER_PATH):  # Pass FOLDER_PATH as the second argument
            name = self.generate_name()

        unique_name = self.generate_unique_name(FOLDER_PATH)  # Pass FOLDER_PATH as an argument
        markdown_content = f"The new planet's biome is {currentBiome}\nThe nearby geological features are: {currentGeoFeatures}"
        file_name = self.create_planet_file(markdown_content, unique_name, FOLDER_PATH)  # Pass FOLDER_PATH as an argument

        # Update the QLabel with the message
        self.message_label.setText(f"Markdown file '{file_name}' created in '{FOLDER_PATH}'")

class ConvinceFunctionTab(QWidget):
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

class DiplomaticFunctionTab(QWidget):
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

class InfiltrationTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Slider Demo")
        self.setGeometry(100, 100, 400, 150)

        layout = QVBoxLayout()

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 4)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(QSlider.TicksBelow)

        self.slider.valueChanged.connect(self.slider_changed)

        self.label = QLabel("Oblivious")

        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        self.setLayout(layout)  # Set the layout for this specific tab

    def slider_changed(self):
        positions = ["Oblivious", "Suspicious", "Investigating", "Alarmed", "Chasing"]
        value = self.slider.value()
        self.label.setText(f"{positions[value]}")

class EncounterTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        nested_tab_widget = QTabWidget()

        diplomatic_tab = DiplomaticFunctionTab()
        nested_tab_widget.addTab(diplomatic_tab, "Diplomatic Function")

        convince_tab = ConvinceFunctionTab()
        nested_tab_widget.addTab(convince_tab, "Convince Encounter")

        infiltration_tab = InfiltrationTab()
        nested_tab_widget.addTab(infiltration_tab, "Infiltration Encounter")

        # interrogation_tab = InterrogationTab()
        # nested_tab_widget.addTab(interrogation_tab, "Interrogation Encounter")

        # randd_tab = RandDTab()
        # nested_tab_widget.addTab(randd_tab, "Research and Development")

        layout.addWidget(nested_tab_widget)
        self.setLayout(layout)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_state)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Hypothetical state variables
        self.some_state_variable = ""
        self.another_state_variable = 0

    def set_state(self, state):
        # Set the state of this tab based on the provided 'state' dictionary
        self.some_state_variable = state.get("some_state_variable", "")
        self.another_state_variable = state.get("another_state_variable", 0)

    def get_state(self):
        # Get the current state of this tab as a dictionary
        return {
            "some_state_variable": self.some_state_variable,
            "another_state_variable": self.another_state_variable,
        }
    def save_state(self):
        # When the Save button is clicked, save the state
        state = self.get_state()
        # You can save this state to a file or use it as needed
        print("State saved:", state)   