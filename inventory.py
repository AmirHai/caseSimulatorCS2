from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QScrollArea, QFrame, QGridLayout

from AllConstants import *
from choosingCaseBtn import SkinButtonWidget


class InventoryWidget(QWidget):
    player_money_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory")
        self.setFixedSize(*WINDOWSIZE)

        self.mainVLayout = QVBoxLayout()
        self.setLayout(self.mainVLayout)

        self.create_window()
        self.download_skins()

    def create_window(self):
        self.profile_name_ledit = QLineEdit()
        self.profile_name_ledit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.profile_name_ledit.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self.profile_name_ledit.setText('')
        self.profile_name_ledit.setDisabled(True)
        self.mainVLayout.addWidget(self.profile_name_ledit)

        self.player_money_lbl = QLabel()
        self.player_money_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.player_money_lbl.setText('')
        self.player_money_lbl.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self.mainVLayout.addWidget(self.player_money_lbl)

        self.Scroll_with_skins = QScrollArea()
        self.Scroll_with_skins.setWidgetResizable(True)
        self.Scroll_with_skins.setFrameShape(QFrame.Shape.Box)
        self.Scroll_with_skins.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.mainVLayout.addWidget(self.Scroll_with_skins)

        self.grid_with_skins = QGridLayout()
        self.grid_with_skins.setSpacing(10)
        self.grid_with_skins.setContentsMargins(10, 10, 10, 10)
        self.grid_with_skins.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.witget_for_scroll = QWidget()
        self.witget_for_scroll.setLayout(self.grid_with_skins)

        self.Scroll_with_skins.setWidget(self.witget_for_scroll)

    def clear_layout(self):
        if self.grid_with_skins is not None:
            # Идем с конца в начало, чтобы индексы не смещались при удалении
            while self.grid_with_skins.count():
                item = self.grid_with_skins.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def skin_was_sold(self):
        self.player_money_changed.emit()
        self.download_skins()

    def download_skins(self):
        self.clear_layout()
        info = get_info_about_player(get_player_id())
        self.profile_name_ledit.setText(info[1])
        self.player_money_lbl.setText(f'Money: {info[2]:.2f}$')

        allSkins = load_info_about_skins(get_player_id())
        pos_x, pos_y = 0, 0
        for skin in allSkins:
            skin_full_name = skin[2]
            if skin[5]:
                skin_full_name = 'StatTrak™ ' + skin_full_name
            skin_full_name += give_skin_floatname(skin[3])
            img = f'images/skins/{replace_symbols(skin[2])}'
            newWidget = SkinButtonWidget(skin_full_name, skin[2], skin[3], WINDOWSIZE[0] // 5, skin[0], img)
            newWidget.inventory_changed.connect(self.skin_was_sold)

            self.grid_with_skins.addWidget(newWidget, pos_y, pos_x)
            pos_x += 1
            if pos_x >= 5:
                pos_x = 0
                pos_y += 1

