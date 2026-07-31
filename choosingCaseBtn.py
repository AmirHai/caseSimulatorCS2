from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap

from scrollingSkinsWidget import ScrollingSkinsWidget


class CaseButtonWidget(QWidget):
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
        #self.iconLbl.setStyleSheet("background: transparent;")

        img_path = info_data.get('image_path', 'path_to_images/default.png')
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.scrollingWindow = ScrollingSkinsWidget(self.info_data, self.info_key)
            self.scrollingWindow.show()
            super().mousePressEvent(event)
