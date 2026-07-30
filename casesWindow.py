from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap

from AllConstants import *
from choosingCaseBtn import CaseButtonWidget
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QSpacerItem, QSizePolicy, QLabel, QScrollArea, \
    QVBoxLayout, QTabWidget


class CasesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Cases')
        self.setFixedSize(*WINDOWSIZE)

        self.Allcollections = None
        self.list_with_buttons = []

        self.create_window()
        self.add_cases()


    def create_window(self):
        self.choosingTabWidget  = QTabWidget(self)
        self.choosingTabWidget.move(10, 10)
        self.choosingTabWidget.setFixedSize(WINDOWSIZE[0] - 20, WINDOWSIZE[1] - 20)
        self.choosingTabWidget.setFont(BTNFONT)

        self.casesVBoxLayout = QVBoxLayout()
        self.specialCollectionsVBox = QVBoxLayout()

        self.WidgetCase = QWidget()
        self.WidgetCase.setLayout(self.casesVBoxLayout)
        self.WidgetSpecial = QWidget()
        self.WidgetSpecial.setLayout(self.specialCollectionsVBox)

        self.choosingTabWidget.addTab(self.WidgetCase, 'Cases')
        self.choosingTabWidget.addTab(self.WidgetSpecial, 'Special Collections')

        self.scrollAreaCases = QScrollArea()
        self.scrollAreaCases.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollAreaSpecials = QScrollArea()
        self.scrollAreaSpecials.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.casesVBoxLayout.addWidget(self.scrollAreaCases)
        self.specialCollectionsVBox.addWidget(self.scrollAreaSpecials)

        self.contentWidgetCases = QWidget()

        self.gridLayoutCases = QGridLayout(self.contentWidgetCases)
        self.gridLayoutCases.setSpacing(10)
        self.gridLayoutCases.setContentsMargins(10, 10, 10, 10)

        self.contentWidgetSpecials = QWidget()

        self.gridLayoutSpecials = QGridLayout(self.contentWidgetSpecials)
        self.gridLayoutSpecials.setSpacing(10)
        self.gridLayoutSpecials.setContentsMargins(10, 10, 10, 10)

    def add_collection_btn(self, needed_scroll, pos, info):
        button_width = int((WINDOWSIZE[0] - 20 * 6) / 5)
        button_height = button_width + 20

        case_btn = CaseButtonWidget(
            info_data=self.Allcollections[info],
            info_key=info,
            button_width=button_width,
            button_height=button_height,
            font=BTNFONT
        )

        self.list_with_buttons.append(case_btn)
        needed_scroll.addWidget(case_btn, pos[0], pos[1])
        print(self.Allcollections[info]['case'])


    def add_cases(self):
        self.Allcollections = get_info_from_json('collections.json')
        pos_x, pos_y = 0, 0
        spec_pos_x, spec_pos_y = 0, 0
        for collect in self.Allcollections:
            if 'Case' in self.Allcollections[collect]['case'] or 'Terminal' in self.Allcollections[collect]['case']:
                self.add_collection_btn(self.gridLayoutCases, (pos_y, pos_x), collect)
                pos_x += 1
                if pos_x >= 5:
                    pos_y += 1
                    pos_x = 0
            else:
                self.add_collection_btn(self.gridLayoutSpecials, (spec_pos_y, spec_pos_x), collect)
                spec_pos_x += 1
                if spec_pos_x >= 5:
                    spec_pos_y += 1
                    spec_pos_x = 0

        self.scrollAreaCases.setWidget(self.contentWidgetCases)
        self.scrollAreaSpecials.setWidget(self.contentWidgetSpecials)


