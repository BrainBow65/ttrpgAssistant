import TabClasses as T

class EncounterTab(T.CoreRulebookValues):
    def __init__(self):
        super().__init__()
        layout = T.QVBoxLayout()
        nested_tab_widget = T.QTabWidget()

        diplomatic_tab = T.DiplomaticEncounter()
        nested_tab_widget.addTab(diplomatic_tab, "Diplomatic Function")

        convince_tab = T.ConvinceEncounter()
        nested_tab_widget.addTab(convince_tab, "Convince Encounter")

        infiltration_tab = T.InfiltrationEncounter()
        nested_tab_widget.addTab(infiltration_tab, "Infiltration Encounter")

        # interrogation_tab = InterrogationTab()
        # nested_tab_widget.addTab(interrogation_tab, "Interrogation Encounter")

        # randd_tab = RandDTab()
        # nested_tab_widget.addTab(randd_tab, "Research and Development")

        layout.addWidget(nested_tab_widget)
        self.setLayout(layout)
        
        self.save_button = T.QPushButton("Save")
        #self.save_button.clicked.connect(self.save_state)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

class GeneratorTab(T.QWidget):
    def __init__(self):
        super().__init__()
        
        
        layout = T.QVBoxLayout()
        nested_tab_widget = T.QTabWidget()

        planet_tab = T.Planets()
        nested_tab_widget.addTab(planet_tab, "Planet Generator")
        society_tab = T.SocietyGenerator()
        nested_tab_widget.addTab(society_tab, "Society Generator")

        layout.addWidget(nested_tab_widget)
        self.setLayout(layout)

class CombatTab(T.QWidget):
    def __init__(self, combatants):
        super().__init__()
        self.combatants = combatants

    def initiative(self):
        pass #determine initiative order

    def run(self):
        while True:
            for combatant in self.combatants:
                if combatant.hp <= 0:
                    print(f"{combatant.name} is defeated.")
                    self.combatants.remove(combatant)
                else:
                    target = T.random.choice([c for c in self.combatants if c != combatant])
                    combatant.attack(target)
            if len(self.combatants) <= 1:
                break
        print(f"{self.combatants[0].name} is the winner!")

class MainWindow(T.QMainWindow):
    combat_objects = []
    def __init__(self):
        super().__init__()
        for folder_name in T.os.listdir(T.CoreRulebookValues.FOLDER_PATH):
            if T.os.path.isdir(T.os.path.join(T.CoreRulebookValues.FOLDER_PATH, folder_name)):
                T.CoreRulebookValues.ALIEN_TYPES.append(folder_name)
        self.settings = T.QSettings("RainbowElephantGaming", "StargateTTRPG")
        self.setWindowTitle("StargateTTRPG App")
        self.setGeometry(100, 100, 800, 600)

        self.generator_tab = GeneratorTab()
        self.encounter_tab = EncounterTab()
        self.combat_tab = CombatTab(MainWindow.combat_objects)
        
        tab_widget = T.QTabWidget()
        tab_widget.addTab(self.generator_tab, "Generator")
        tab_widget.addTab(self.encounter_tab, "Encounters")
        tab_widget.addTab(self.combat_tab, "Combat")

        self.setCentralWidget(tab_widget)

def main():
    T.Registry.load_instances(T.Registry.directory)
    app = T.QApplication(T.sys.argv)
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(T.Registry.save_instances(T.Registry.directory))
    T.sys.exit(app.exec())

if __name__ == '__main__':
    main()