import TabClasses as T
import persistant_data as P

class EncounterTab(T.Tab):
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
        self.save_button.clicked.connect(self.save_state)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Hypothetical state variables
        self.some_state_variable = ""
        self.another_state_variable = 0

class CombatTab():
    def __init__(self, combatants):
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
    def __init__(self):
        super().__init__()

        self.settings = T.QSettings("RainbowElephantGaming", "StargateTTRPG")
        self.setWindowTitle("StargateTTRPG App")
        self.setGeometry(100, 100, 800, 600)

        tab_widget = T.QTabWidget()
        self.planet_tab = T.PlanetGenerator()
        self.society_tab = T.SocietyGenerator()
        self.encounter_tab = EncounterTab()
        self.combat_tab = CombatTab()

        tab_widget.addTab(self.planet_tab, "Planet Generator")
        tab_widget.addTab(self.society_tab, "Society Generator")
        tab_widget.addTab(self.encounter_tab, "Encounters")
        tab_widget.addTab(self.combat_tab, "Combat")

        self.setCentralWidget(tab_widget)

def main():
    game_data = P.IDataPersistence()
    app = T.QApplication(T.sys.argv)
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(P.IDataPersistence.save())
    T.sys.exit(app.exec_())

if __name__ == '__main__':
    main()