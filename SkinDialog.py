import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, pyqtSignal
from AllConstants import *
from styles import dropped_skin_style, red_button_style, green_button_style


class SkinDropDialog(QDialog):
    def __init__(self, skin_name, float_value, rarity, image_path):
        super().__init__()

        # Настройки главного окна
        self.setWindowTitle("Новый скин!")
        self.setFixedSize(350, 450)  # Фиксированный размер, чтобы окно не прыгало
        # Убираем кнопку закрытия "?" и оставляем окно поверх остальных
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self.setStyleSheet(dropped_skin_style(rarity))
        # Главный вертикальный лейаут
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # 1. Заголовок
        title_label = QLabel("New Item Obtained!")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #FFFFFF;")  # Золотистый цвет
        main_layout.addWidget(title_label)

        # 2. Фотография скина
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background: transparent; border: none;")
        pixmap = QPixmap(image_path)
        # Масштабируем картинку под размер окна с сохранением пропорций
        scaled_pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        main_layout.addWidget(self.image_label)

        # 3. Название скина
        name_label = QLabel(skin_name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        main_layout.addWidget(name_label)

        # 4. Float-значение
        float_label = QLabel(f"Float: {float_value:.10f}")
        float_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        float_label.setFont(QFont("Courier New", 12))  # Моноширинный шрифт для цифр
        main_layout.addWidget(float_label)

        # 5. Блок с кнопками (горизонтальный лейаут)
        buttons_layout = QHBoxLayout()

        self.sell_button = QPushButton("Продать")
        self.sell_button.setStyleSheet(red_button_style())
        self.sell_button.clicked.connect(self.on_sell_clicked)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setStyleSheet(green_button_style())
        self.save_button.clicked.connect(self.on_save_clicked)

        buttons_layout.addWidget(self.sell_button)
        buttons_layout.addWidget(self.save_button)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

        # Переменная для хранения выбора игрока
        self.user_choice = None

    def on_sell_clicked(self):
        self.user_choice = "sell"
        self.accept()  # Закрывает окно и возвращает код успешного завершения

    def on_save_clicked(self):
        self.user_choice = "save"
        self.accept()


class SkinInventoryDialog(QDialog):
    def __init__(self, skin_name, float_value, image_path):
        super().__init__()

        # Настройки главного окна
        self.setWindowTitle("Информация о скине")
        self.setFixedSize(350, 450)  # Фиксированный размер, чтобы окно не прыгало
        # Убираем кнопку закрытия "?" и оставляем окно поверх остальных
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Главный вертикальный лейаут
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # 1. Заголовок
        title_label = QLabel(skin_name)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #FFFFFF;")
        main_layout.addWidget(title_label)

        # 2. Фотография скина
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(image_path)
        # Масштабируем картинку под размер окна с сохранением пропорций
        scaled_pixmap = pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        main_layout.addWidget(self.image_label)

        # 3. Float-значение
        float_lbl = QLabel(f"Float: {float_value:.10f}")
        float_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        float_lbl.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        main_layout.addWidget(float_lbl)

        # 4. цена
        cost = get_info_from_json('prices.json')[skin_name]
        cost_lbl = QLabel(f"Cost: {cost:.2f}$")
        cost_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cost_lbl.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        main_layout.addWidget(cost_lbl)

        # 5. Блок с кнопками (горизонтальный лейаут)
        buttons_layout = QHBoxLayout()

        self.sell_button = QPushButton("Продать")
        self.sell_button.setStyleSheet("background-color: #d9534f; color: white; padding: 10px; font-weight: bold;")
        self.sell_button.clicked.connect(self.on_sell_clicked)

        self.save_button = QPushButton("Выйти")
        self.save_button.setStyleSheet("background-color: #5cb85c; color: white; padding: 10px; font-weight: bold;")
        self.save_button.clicked.connect(self.on_save_clicked)

        buttons_layout.addWidget(self.sell_button)
        buttons_layout.addWidget(self.save_button)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

        # Переменная для хранения выбора игрока
        self.user_choice = None

    def on_sell_clicked(self):
        self.user_choice = "sell"
        self.accept()  # Закрывает окно и возвращает код успешного завершения

    def on_save_clicked(self):
        self.user_choice = "exit"
        self.accept()