import tabs as T

class ApplicationSettings:
    def __init__(self):
        # Initialize default settings here
        self.tab1_state = {}
        self.tab2_state = {}
        self.tab3_state = {}
        # ... add state attributes for each tab as needed ...

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