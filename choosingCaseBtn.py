from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

from AllConstants import BTNFONT, get_info_from_json, sell_item, sell_skin_from_inventory
from scrollingSkinsWidget import ScrollingSkinsWidget
from SkinDialog import SkinInventoryDialog


class CaseButtonWidget(QWidget):
    item_sold = pyqtSignal()

    def __init__(self, info_data, info_key, button_width, button_height, font, parent=None):
        super().__init__()

        self.info_data = info_data
        self.info_key = info_key
        self.button_width = button_width
        self.button_height = button_height
        self.font = font
        self.parent = parent

        self.setFixedSize(self.button_width, self.button_height)

        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 6px;
            }
            QWidget:hover {
                background-color: #3d3d3d;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 5, 8, 5)
        self.layout.setSpacing(8)

        self.iconLbl = QLabel()
        icon_size = int(button_width * 0.8)
        self.iconLbl.setFixedSize(icon_size, icon_size)
        self.iconLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        img_path = f'images/cases/{info_data['case']}'
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            self.iconLbl.setPixmap(pixmap.scaled(
                icon_size, icon_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

        self.layout.addWidget(self.iconLbl, alignment=Qt.AlignmentFlag.AlignCenter)

        self.text_label = QLabel()
        self.text_label.setText(info_data['case'])
        self.text_label.setFont(font)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("color: white; background: transparent;")

        self.layout.addWidget(self.text_label, stretch=1)
        self.setLayout(self.layout)

    def sell_item_pressed(self):
        self.item_sold.emit()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.scrollingWindow = ScrollingSkinsWidget(self.info_data, self.info_key)
            self.scrollingWindow.show()
            self.scrollingWindow.item_sold.connect(self.sell_item_pressed)
            super().mousePressEvent(event)


class SkinButtonWidget(QWidget):
    inventory_changed = pyqtSignal()

    def __init__(self, skin_name, float_data, button_size, skin_id, parent=None):
        super().__init__()

        self.skin_name = skin_name
        self.float_data = float_data
        self.button_size = button_size
        self.skin_id = skin_id
        self.parent = parent


        self.setFixedSize(self.button_size, self.button_size)

        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 6px;
            }
            QWidget:hover {
                background-color: #3d3d3d;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(8, 5, 8, 5)
        self.layout.setSpacing(8)

        self.iconLbl = QLabel()
        icon_size = int(self.button_size * 0.7)
        self.iconLbl.setFixedSize(icon_size, icon_size)
        self.iconLbl.setFixedSize(icon_size, icon_size)
        self.iconLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.iconLbl.setStyleSheet("background: transparent;")

        img_path = ''
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            self.iconLbl.setPixmap(pixmap.scaled(
                icon_size, icon_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

        self.layout.addWidget(self.iconLbl, alignment=Qt.AlignmentFlag.AlignCenter)

        self.text_label = QLabel()
        self.text_label.setText(skin_name)
        self.text_label.setFont(BTNFONT)
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("color: white; background: transparent;")

        self.layout.addWidget(self.text_label, stretch=1)
        self.setLayout(self.layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.scrollingWindow = SkinInventoryDialog(self.skin_name, self.float_data, '')
            if self.scrollingWindow.exec() == QDialog.DialogCode.Accepted:
                if self.scrollingWindow.user_choice == "sell":
                    sell_skin_from_inventory(self.skin_id, self.skin_name)
                    self.inventory_changed.emit()
                elif self.scrollingWindow.user_choice == "save":
                    pass

            super().mousePressEvent(event)
