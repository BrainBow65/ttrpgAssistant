import json
from abc import ABC, abstractmethod

class GameData:
    def __init__(self):
        self.tabs = []

    def add_tab(self, tab):
        self.tabs.append(tab)

    def remove_tab(self, tab):
        self.tabs.remove(tab)

class IDataPersistence(ABC):
    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def load(self):
        pass

class JsonDataPersistence(IDataPersistence):
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data.__dict__, f)

    def load(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        game_data = GameData()
        game_data.__dict__.update(data)
        return game_data