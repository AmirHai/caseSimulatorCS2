from PyQt6.QtCore import Qt

from AllConstants import *
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QLabel
from casesWindow import CaseSelectionWindow, CasesWindow


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(*MAINMENUSIZE)
        self.move(500, 400)

        self.create_window()

    def create_window(self):
        self.main_grid_layout = QGridLayout()
        self.main_grid_layout.setSpacing(5)
        self.main_grid_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_grid_layout)

        placer = 0

        self.profile_name_lbl = QLabel()
        self.profile_name_lbl.setFont(BTNFONT)
        self.profile_name_lbl.setText("Profile Name")
        self.main_grid_layout.addWidget(self.profile_name_lbl, placer, 0, 1, 1)
        placer += 1

        self.money_lbl = QLabel("Money:")
        self.money_lbl.setFont(BTNFONT)
        self.main_grid_layout.addWidget(self.money_lbl, placer, 0, 1, 1)
        placer += 1

        self.cases_btn = QPushButton()
        self.cases_btn.setText("Cases")
        self.cases_btn.setFont(BTNFONT)
        self.cases_btn.clicked.connect(self.case_btn_clicked)
        self.main_grid_layout.addWidget(self.cases_btn, placer, 0, 1, 1)
        placer += 1

        self.inventory_btn = QPushButton()
        self.inventory_btn.setText("Inventory")
        self.inventory_btn.setFont(BTNFONT)
        self.main_grid_layout.addWidget(self.inventory_btn, placer, 0, 1, 1)
        placer += 1


        self.profile_btn = QPushButton()
        self.profile_btn.setText("Profile")
        self.profile_btn.setFont(BTNFONT)
        self.main_grid_layout.addWidget(self.profile_btn, placer, 0, 1, 1)
        placer += 1

        self.shop_btn = QPushButton()
        self.shop_btn.setText("Shop")
        self.shop_btn.setFont(BTNFONT)
        self.main_grid_layout.addWidget(self.shop_btn, placer, 0, 1, 1)
        placer += 1

        vertical_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.main_grid_layout.addItem(vertical_spacer, placer, 0, 1, 1)

    def case_btn_clicked(self):
        self.case_window = CasesWindow()
        self.case_window.show()
