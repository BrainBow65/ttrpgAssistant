import sys
import os
import random
import string
import glob
import yaml
import re
import saveandload as S
from pathlib import Path
from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QLineEdit, QTextEdit, QComboBox, QCheckBox, QGridLayout, QSizePolicy

class CoreRulebookValues(QWidget):
    FOLDER_PATH = "C:/Users/Michelle/Documents/Obsidian Notes/StargateTTRPG/GameObjects"
    PLANETS = []
    GEO_FEATURES = ["Anticline", "Basin", "Butte", "Cave", "Cliff", "Canyon", "Valley", "Bay", "Archipelago"]
    BIOMES = ["Arboreal", "Artificial", "Desert", "Grasslands", "Lunar", "Mountainous", "Oceanic", "Rainforest", "Starship", "Terraformed", "Toxic", "Tundra", "Subterranean", "Swamp", "Urban", "Volcanic"]
    ALIEN_TYPES = []
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
                  2:[2, 'Small', 7, 14, 8, 1, 10, 2, 12, 20, 6, '1d4'],
                  3:[2, 'Small', 8, 14, 8, 1, 10, 2, 13, 25, 6, '1d6'],
                  4:[2, 'Small', 9, 14, 8, 1, 10, 2, 13, 30, 6, '1d6'],
                  5:[3, 'Medium', 10, 12, 10, 1, 10, 2, 14, 37, 6, '1d6'],
                  6:[3, 'Medium', 10, 12, 10, 1, 10, 2, 14, 44, 6, '1d6'],
                  7:[3, 'Medium', 11, 12, 10, 1, 10, 2, 15, 55, 6, '1d8'],
                  8:[3, 'Medium', 12, 12, 11, 1, 10, 2, 15, 58, 6, '1d8'],
                  9:[4, 'Medium', 13, 12, 11, 1, 10, 2, 16, 65, 6, '1d8'],
                  10:[4, 'Medium', 14, 12, 12, 1, 10, 2, 16, 74, 6, '1d8'],
                  11:[4, 'Medium', 15, 10, 13, 1, 10, 2, 16, 83, 6, '1d10'],
                  12:[4, 'Medium', 16, 10, 14, 1, 10, 2, 17, 92, 6, '1d10'],
                  13:[5, 'Large', 17, 10, 14, 1, 10, 2, 17, 101, 6, '2d6'],
                  14:[5, 'Large', 18, 10, 14, 1, 10, 2, 18, 110, 6, '2d6'],
                  15:[5, 'Large', 18, 10, 14, 1, 10, 2, 18, 121, 6, '2d6'],
                  16:[5, 'Large', 18, 8, 15, 1, 10, 2, 19, 132, 6, '2d8'],
                  17:[6, 'Large', 19, 8, 15, 1, 10, 2, 19, 143, 6, '2d8'],
                  18:[6, 'Huge', 20, 8, 15, 1, 10, 2, 20, 154, 6, '3d6'],
                  19:[6, 'Huge', 21, 8, 15, 1, 10, 2, 21, 165, 6, '3d6'],
                  20:[6, 'Huge', 22, 8, 5, 1, 10, 2, 22, 176, 6, '4d6']}
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
    #dictionary structure: {cr:[proficience, hit dice, str, dex, con, int, wis, cha AC, HP, speed (m), special]}
    JAFFA_STATS:{1:[2, 3, 14, 12, 14, 8, 10, 14, 14, 20, 6, None],
                      2:[2, 4, 14, 12, 15, 8, 10, 14, 14, 25, 6, None],
                      3:[2, 5, 15, 12, 15, 8, 10, 14, 14, 30, 6, None],
                      4:[2, 6, 15, 12, 15, 8, 10, 14, 14, 35, 6, None],
                      5:[3, 7, 15, 13, 16, 8, 10, 14, 14, 45, 6, 'Attack Specialist'],
                      6:[3, 8, 16, 13, 16, 8, 10, 14, 14, 50, 6, None],
                      7:[3, 9, 16, 13, 16, 8, 10, 14, 14, 55, 6, None],
                      8:[3, 10, 16, 14, 17, 8, 10, 14, 15, 60, 6, None],
                      9:[4, 11, 17, 14, 17, 8, 10, 14, 15, 65, 6, None],
                      10:[4, 12, 17, 14, 17, 8, 10, 14, 15, 70, 6, None],
                      11:[4, 13, 17, 15, 18, 8, 10, 14, 15, 80, 6, 'Attack Veteran'],
                      12:[4, 14, 18, 15, 18, 8, 10, 14, 15, 85, 6, None],
                      13:[5, 15, 18, 15, 18, 8, 10, 14, 22, 90, 6, None],
                      14:[5, 16, 18, 16, 19, 8, 10, 14, 22, 95, 6, None],
                      15:[5, 17, 19, 16, 19, 8, 10, 14, 22, 100, 6, None],
                      16:[5, 18, 19, 16, 19, 8, 10, 14, 22, 105, 6, None],
                      17:[6, 19, 19, 17, 20, 8, 10, 14, 22, 110, 6, 'Attack Ace'],
                      18:[6, 20, 20, 17, 20, 8, 10, 14, 22, 115, 6, None],
                      19:[6, 20, 20, 17, 20, 8, 10, 14, 22, 120, 6, None],
                      20:[6, 20, 20, 17, 20, 8, 10, 14, 22, 125, 6, None]}
    #NPC stat dictionary structure: {class:{CR:[lvl, ac, hp, speed(m), str, dex, con, int, wis, cha, proficiency modifier, {skills}, {saves}, [feats], [inspirations], [armor], [weapons]]}}
    NPC_STATS_DICT = {'diplomat':{0.5:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                #this is where I'm at
                                1:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  2:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  3:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  4:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  5:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  6:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  7:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  8:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  9:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  10:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  11:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  12:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  13:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  14:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  15:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  16:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  17:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  18:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']},
                                  19:{'lvl':1, 'ac':10, 'hp':18,'speed':6, 'str':9, 'dex':10, 'con':10, 'int':13, 'wis':14, 'cha':16, 'proficiency_mod':2, 'skills':{'culture':4, 'deception':5, 'insight':4, 'persuasion':5}, 'saves':{'wisdom':4, 'charisma':5}, 'feats':['Inspire'],'Inspirations':['Calm & Collected'], 'field_hacks':None, 'armor':['Dress Uniform'], 'weapons':['Sidearm']}},
                        'engineer':{0.5:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    1:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    2:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    3:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    4:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    5:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    6:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    7:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    8:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    9:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    10:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    11:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    12:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    13:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    14:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    15:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    16:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    17:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    18:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']},
                                    19:{'lvl':1,'ac':16, 'hp':18, 'speed':6, 'str':13, 'dex':14, 'con':10,'int':16,'wis':10, 'cha':9, 'proficiency_mod':2, 'skills':{'Engineering':5, 'Pilot':4, 'Perception':2}, 'saves':{'Dexterity':4, 'Intelligence':5}, 'feats':['jury rig'], 'Modifications':['Armorer'], 'Gear':['Bullet resistant vest'], 'weapons':['longarm']}},
                        'medic':{0.5:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 1:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 2:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 3:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 4:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 5:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 6:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 7:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 8:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 9:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 10:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 11:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 12:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 13:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 14:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 15:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 16:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 17:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 18:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']},
                                 19:{'lvl':1,'ac':15, 'hp':18, 'speed':6, 'str':10, 'dex':13, 'con':10,'int':10,'wis':16, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':2, 'Insight':5, 'Medicine':5, 'Science':2}, 'saves':{'Dexterity':3, 'Wisdom':5}, 'feats':['First Aid'], 'Procedures':['Urgent Care'], 'Gear':['Bullet resistant vest'], 'weapons':['shotgun']}},
                        'scientist':{0.5:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     1:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     2:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     3:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     4:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     5:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     6:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     7:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     8:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     9:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     10:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     11:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     12:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     13:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     14:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     15:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     16:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     17:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     18:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']},
                                     19:{'lvl':1,'ac':10, 'hp':17, 'speed':6, 'str':10, 'dex':10, 'con':9,'int':16,'wis':14, 'cha':13, 'proficiency_mod':2, 'skills':{'Culture':4, 'Investigation':5, 'Nature':5, 'Science':5}, 'saves':{'Intelligence':5, 'Wisdom':4}, 'feats':['Eureka'], 'Discoveries':['Hyper-focus'], 'Gear':['common local attire'], 'weapons':['Shortblade']}},
                        'scout':{0.5:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 1:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 2:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 3:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 4:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 5:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 6:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 7:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 8:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 9:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 10:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 11:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 12:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 13:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 14:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 15:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 16:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 17:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 18:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']},
                                 19:{'lvl':1,'ac':13, 'hp':21, 'speed':6, 'str':14, 'dex':14, 'con':12,'int':10,'wis':12, 'cha':10, 'proficiency_mod':2, 'skills':{'Perception':3, 'Stealth':4, 'Survival':3}, 'saves':{'constitution':3, 'Dexterity':4}, 'feats':['Survivalist'], 'Field Hacks':['Ranger Tricks'], 'Gear':['Furs'], 'weapons':['Bow']}},
                        'soldier':{0.5:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   1:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   2:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   3:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   4:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   5:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   6:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   7:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   8:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   9:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   10:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   11:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   12:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   13:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   14:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   15:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   16:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   17:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   18:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']},
                                   19:{'lvl':1,'ac':16, 'hp':22, 'speed':6, 'str':16, 'dex':13, 'con':14,'int':9,'wis':10, 'cha':10, 'proficiency_mod':2, 'skills':{'Athletics':5, 'Intimidation':2, 'Pilot':3}, 'saves':{'Strength':5, 'Constitution':4}, 'feats':['Tactical flexibility'], 'Tactics':['Defensive Posture'], 'Gear':['Chainmail'], 'weapons':['bludgeon']}}}

    def __init__(self):
        super().__init__()

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
        currentAlien = [self.choose_random_value(CoreRulebookValues.ALIEN_TYPES) if random.random() < 0.7 else CoreRulebookValues.ALIEN_TYPES['Human']]
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

class Planets:
    def __init__(self, name=None, type = "Planets", biome=None):
        self.name = name
        self.biome = biome
        self.type = type
       
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
    def __init__(self, name=None, type="Aliens", race=None, npc_class=None, lvl=None, hp=None, ac=None, speed=None, str=None, dex=None, con=None, int=None, wis=None, cha=None, skills=None, proficiency_mod=None, saves=None, feats=None, field_hacks=None, armor=None, weapons=None, gear=None, attacks=None):
        super().__init__()
        self.name = name
        self.type = type
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
        self.armor = armor
        self.weapons = weapons

class NPC(Character):
    def __init__(self, cr = None):
        super().__init__()
        self.cr = cr

class PC(Character):
    def __init__(self):
        super().__init__()

class CharacterCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.input_fields = {}  # Initialize input_fields here
        layout = QGridLayout(self)

        # Input field for Class
        class_label = QLabel("Class")
        layout.addWidget(class_label, 0, 0, 1, 1, Qt.AlignLeft)
        self.class_input = QLineEdit()
        layout.addWidget(self.class_input, 0, 1)

        # Input field for Challenge Rating
        cr_label = QLabel("Challenge Rating")
        layout.addWidget(cr_label, 0, 2, 1, 1, Qt.AlignLeft)
        self.cr_input = QLineEdit()
        layout.addWidget(self.cr_input, 0, 3)

        row = 1
        col = 0
        self.input_fields = {}
        for attr_name, attr_value in vars(NPC()).items():
            if not callable(attr_value) and not attr_name.startswith("__"):
                if attr_name == "npc_class" or attr_name == "race" or attr_name == "type" or attr_name == "cr":
                    continue
                label = QLabel(attr_name.capitalize())
                input_field = QLineEdit(str(attr_value))  # Convert to string for display
                layout.addWidget(label, row, col, 1, 1, Qt.AlignRight)
                layout.addWidget(input_field, row, col + 1, 1, 1)
                self.input_fields[attr_name] = input_field

                col += 2
                if col >= 6:  # Start a new row after every 3 pairs of attributes
                    row += 1
                    col = 0
        row+=1
        self.text_box = QTextEdit("Description")
        self.text_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.text_box, row, 0, 1, 8)
        
        row+=1
        species_label = QLabel("Species")
        layout.addWidget(species_label, row, 0, 1, 2)  # Left-align the Species label

        # Checkbox for custom race
        row+=1
        custom_checkbox = QCheckBox("Custom")
        custom_checkbox.stateChanged.connect(self.toggle_custom_race)
        layout.addWidget(custom_checkbox, row, 0, 1, 2)

        # Combobox for Alien Types
        self.alien_type_combobox = QComboBox()
        self.alien_type_combobox.addItems([alien_type for alien_type in CoreRulebookValues.ALIEN_TYPES])
        layout.addWidget(self.alien_type_combobox, row + 2, 2, 1, 2)

        # Input field for custom race
        self.custom_race_input = QLineEdit()
        self.custom_race_input.setMaxLength(20)  # Set maximum length to 20 characters
        self.custom_race_input.setVisible(False)  # Initially not visible
        layout.addWidget(self.custom_race_input, row + 2, 4, 1, 2)

        # Button to create NPC instance
        create_button = QPushButton("Create")
        create_button.setEnabled(True)
        
        layout.addWidget(create_button, row + 2, 6, 1, 2)

        self.setLayout(layout)

        # Connect signals for dynamic updating
        self.class_input.textChanged.connect(self.update_attribute_values)
        self.cr_input.textChanged.connect(self.update_attribute_values)
        create_button.clicked.connect(self.create_npc_instance)

    def toggle_custom_race(self, state):
        is_custom_race = state == 2  # 2 corresponds to Qt.Checked
        self.alien_type_combobox.setVisible(not is_custom_race)
        self.custom_race_input.setVisible(is_custom_race)

    def update_attribute_values(self):
        selected_class = self.class_input.text().lower()
        selected_cr = self.cr_input.text()

        try:
            selected_cr = float(selected_cr)
        except ValueError:
            selected_cr = None

        if selected_class and selected_cr is not None:
            npc_stats = CoreRulebookValues.NPC_STATS_DICT.get(selected_class, {}).get(selected_cr, {})

            if npc_stats:
                for attr_name, input_field in self.input_fields.items():
                    if attr_name in npc_stats:
                        value = npc_stats[attr_name]

                        # Check if the value is a dictionary
                        if isinstance(value, dict):
                            # Handle dictionary values by converting them to a string representation
                            input_field.setText(str(value))
                        else:
                            # For other types, directly set the text
                            input_field.setText(str(value))
                    else:
                        input_field.clear()
            
    def create_npc_instance(self):
        registry = S.Registry()
        new_npc = NPC()
        if self.cr_input.text() and self.class_input.text() and self.input_fields['name']:
            print('Need to enter challenge rating, name, and class')
        for attr_name, input_field in self.input_fields.items():
            setattr(new_npc, attr_name, input_field.text())
        new_npc.npc_class = self.class_input.text()
        new_npc.cr = self.cr_input.text()
        if self.custom_race_input.isVisible():
            new_npc.race = self.custom_race_input.text()
        else:
            new_npc.race = self.alien_type_combobox.currentText()
        registry.add_instance(new_npc)

class Beast(CoreRulebookValues):
    def __init__(self, name=None, cr=None, size=None, type = "Beasts", hp=None, ac=None, str=None, dex=None, con=None, int=None, wis=None, cha=None, skills=None, proficiency_mod=None, saves=None, abilities=None, attacks=None):
        super().__init__()
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
    def __init__(self, name=None,type="Equipment", techlvl=None, bulk=None):
        self.name = name
        self.techlvl = techlvl
        self.type = type
        self.bulk = bulk

class Weapons(Equipment):
    def __init__(self, dmg, capacity, reload, range, special):
        super().__init__()
        self.dmg = dmg
        self.capacity = capacity
        self.reload = reload
        self.range = range
        self.special = special
        
class Armor(Equipment):
    def __init__(self, ac, strength, stealth, special):
        super().__init__()
        self.ac = ac
        self.strength = strength
        self.stealth = stealth
        self.special = special
        
class Gear(Equipment):
    def __init__(self, description):
        super().__init__()
        self.description = description
        
class Facilities:
    def __init__(self, name=None, type="Facilities", bonusrating=None, bonustype=None):
        self.name = name
        self.bonusrating = bonusrating
        self.bonustype = bonustype
        
class Vehicles:
    def __init__(self, name=None, type="Vehicles", size=None, handling=None, speed=None, passengers=None, weapons=None, hp=None, ac=None):
        self.name = name
        self.size = size
        self.handling = handling
        self.speed = speed
        self.passengers = passengers
        self.type = type
        self.weapons = weapons
        self.hp = hp
        self.ac = ac