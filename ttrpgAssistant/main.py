import TabClasses as T

class ApplicationSettings:
    def __init__(self):
        # Initialize default settings here
        self.tab1_state = {}
        self.tab2_state = {}
        self.tab3_state = {}
        # ... add state attributes for each tab as needed ...

class EncounterTab(Tab):
    def __init__(self):
        super().__init__()

        nested_tab_widget = QTabWidget()

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

        T.layout.addWidget(nested_tab_widget)
        self.setLayout(T.layout)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_state)
        T.layout.addWidget(self.save_button)

        self.setLayout(T.layout)

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

class MainWindow(T.QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = T.QSettings("RainbowElephantGaming", "StargateTTRPG")
        self.setWindowTitle("StargateTTRPG App")
        self.setGeometry(100, 100, 800, 600)

        tab_widget = T.QTabWidget()
        self.planet_tab = T.PlanetGeneratorTab()
        self.society_tab = T.SocietyGeneratorTab()
        self.encounter_tab = T.EncounterTab()

        tab_widget.addTab(self.planet_tab, "Planet Generator")
        tab_widget.addTab(self.society_tab, "Society Generator")
        tab_widget.addTab(self.encounter_tab, "Encounters")

        self.setCentralWidget(tab_widget)

def main():
    app = T.QApplication(T.sys.argv)
    window = MainWindow()
    window.show()
    T.sys.exit(app.exec_())

if __name__ == '__main__':
    main()