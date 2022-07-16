import sys, math, json, os
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QLabel, QLineEdit, QScrollArea, QGroupBox
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
import requests

os.environ['QT_API'] = 'pyqt5'

class FlagsExplorer ():
    def __init__ (self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.groupbox_grid = QGridLayout()
        self.countries_data = []
        self.widgets = []


    def init (self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet())

        self.get_flags()


    def get_flags (self):
        with open('data.json') as data_file:
            self.countries_data = json.load(data_file)['data']

        self.create_window()


    def create_window (self):
        # App Logo
        logo = QLabel()
        logo.setPixmap(QPixmap('icon.png').scaledToWidth(40))
        logo.setContentsMargins(0, 0, 220, 0)

        # App Name
        text_edit = QLabel()
        text_edit.setText('Flags Explorer')
        text_edit.setFont(QFont('Arial', 19))
        
        # Search Input
        text_input = QLineEdit()
        text_input.setFont(QFont('Arial', 15))
        text_input.setContentsMargins(0, 10, 0, 10)
        text_input.textChanged.connect(self.search_flag)

        # Groupbox (flags container)
        groupbox = QGroupBox()

        # Add widgets to window
        grid = QGridLayout()
        grid.addWidget(logo, 0, 1, Qt.AlignCenter)
        grid.addWidget(text_edit, 0, 1, Qt.AlignCenter)
        grid.addWidget(text_input, 1, 1, Qt.AlignCenter)
            
        # Render flags
        self.render_flags(self.countries_data[0:12], self.groupbox_grid)
        
        # Set groupbox layout
        self.groupbox_grid.setRowStretch(0, 1)
        groupbox.setLayout(self.groupbox_grid)

        # Scrollarea (groupbox scroll)
        scroll = QScrollArea()
        scroll.setWidget(groupbox)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        grid.addWidget(scroll, 2, 1)

        # Window settings
        self.window.setLayout(grid)
        self.window.setFixedSize(600, 400)
        self.window.move(300, 300)
        self.window.setWindowIcon(QIcon('icon.png'))
        self.window.setWindowTitle('Flags Explorer')
        self.window.show()
        sys.exit(self.app.exec_())

    
    def search_flag (self, search_term):
        search_term_length = len(search_term)
        results = []
        
        # Search "algorithm"
        if search_term_length > 0:
            for country in self.countries_data:
                if country['name'][0:search_term_length] == search_term:
                    results.append(country)
        else:
            results = self.countries_data[0:12]
        
        self.render_flags(results, self.groupbox_grid)


    def render_flags (self, countries, container_layout):
        if len(self.widgets) > 0:
            for widget in self.widgets:
                container_layout.removeWidget(widget)

            self.widgets = []

        for index, country in enumerate(countries):
            country_flag = QLabel()
            country_name = QLabel()

            res = requests.get(country['flag'])

            with open('flag.png', 'wb') as fd:
                for chunk in res.iter_content(chunk_size=128):
                    fd.write(chunk)

            country_flag.setPixmap(QPixmap('flag.png').scaledToWidth(100))
            country_flag.setContentsMargins(0, 20, 0, 15)

            country_name.setText(country['name'])
            country_name.setFont(QFont('Arial', 10))

            self.widgets.append(country_flag)
            self.widgets.append(country_name)

            container_layout.addWidget(country_flag, math.floor(index / 3) + 2, 0 if str(index / 3)[-1] == '0' else 1 if str(index / 3)[-2] == '3' else 3, Qt.AlignTop | Qt.AlignHCenter)
            container_layout.addWidget(country_name, math.floor(index / 3) + 2, 0 if str(index / 3)[-1] == '0' else 1 if str(index / 3)[-2] == '3' else 3, Qt.AlignBottom | Qt.AlignHCenter)

    
if __name__ == '__main__':
    flags_explorer = FlagsExplorer()
    flags_explorer.init()

