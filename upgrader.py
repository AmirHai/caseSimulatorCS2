import math
import random

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QResizeEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy

from styles import green_button_style, set_inventory_skin_style
from upgraderRoulette import UpgraderRouletteWidget
from upgraderSkinsScroll import SkinsScroll
from AllConstants import *


class Upgrader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Upgrader')
        self.setFixedSize(WINDOWSIZE[0], WINDOWSIZE[0])

        self.inventory_skin_rarity = '#000000'
        self.upgraded_skin_rarity = '#000000'

        self.disableBtns = []

        self.inventory_skin_info = None
        self.upgraded_skin_info = None

        self.create_window()

    def create_window(self):
        self.mainVLayout = QVBoxLayout()
        self.setLayout(self.mainVLayout)

        self.HorizontalUpperLayout = QHBoxLayout()
        self.HorizontalUpperLayout.setContentsMargins(10, 10, 10, 10)
        self.HorizontalUpperLayout.setSpacing(10)
        self.mainVLayout.addLayout(self.HorizontalUpperLayout, stretch=5)

        self.create_skin_icons()

        self.HorizontalCentralLayout = QHBoxLayout()
        self.HorizontalCentralLayout.setContentsMargins(10, 10, 10, 10)
        self.HorizontalCentralLayout.setSpacing(10)
        self.mainVLayout.addLayout(self.HorizontalCentralLayout, stretch=2)

        self.VerticalLeftLayout = QVBoxLayout()
        self.VerticalLeftLayout.setContentsMargins(10, 10, 10, 10)
        self.VerticalLeftLayout.setSpacing(10)
        self.HorizontalCentralLayout.addLayout(self.VerticalLeftLayout, stretch=1)

        self.upbgradeBtn = QPushButton('Upgrade')
        self.upbgradeBtn.setMinimumSize(200, 50)
        self.upbgradeBtn.setStyleSheet(green_button_style())
        self.upbgradeBtn.setFont(create_Font(12, True))
        self.upbgradeBtn.clicked.connect(self.upgrade_btn_clicked)
        self.disableBtns.append(self.upbgradeBtn)
        self.HorizontalCentralLayout.addWidget(self.upbgradeBtn)

        self.VerticalRightLayout = QVBoxLayout()
        self.VerticalRightLayout.setContentsMargins(10, 10, 10, 10)
        self.VerticalRightLayout.setSpacing(10)
        self.HorizontalCentralLayout.addLayout(self.VerticalRightLayout, stretch=1)

        self.create_grade_widgets()
        self.create_cost_widgets()

        self.HorizontalSkinsLayout = QHBoxLayout()
        self.HorizontalSkinsLayout.setContentsMargins(10, 10, 10, 10)
        self.HorizontalSkinsLayout.setSpacing(10)
        self.mainVLayout.addLayout(self.HorizontalSkinsLayout, stretch=5)

        self.inventorySkins = SkinsScroll(True)
        self.inventorySkins.item_selected.connect(self.inventory_skin_clicked)
        self.HorizontalSkinsLayout.addWidget(self.inventorySkins)

        self.skinVariants = SkinsScroll(False)
        self.skinVariants.item_selected.connect(self.upgraded_skin_clicked)
        self.HorizontalSkinsLayout.addWidget(self.skinVariants)

    def create_grade_widgets(self):
        self.persentLayout = QHBoxLayout()

        self.persentButtons = []
        persents = get_persents_from_db(1)
        for button in range(4):
            db_index = button + 1  # Индексы: 1, 2, 3, 4
            current_percent = persents[db_index]

            btn = QPushButton(f'{current_percent}%')
            btn.setMinimumHeight(40)
            btn.setFont(create_Font(12, True))

            # Явно передаем уже готовое число процентов в аргумент lambda
            btn.clicked.connect(lambda checked, p=current_percent: self.chance_changed_with_skin(p))
            self.disableBtns.append(btn)
            self.persentLayout.addWidget(btn)
            self.persentButtons.append(btn)

        self.gradeLayout = QHBoxLayout()
        self.gradeButtons = []
        for button in range(4):
            db_index = button + 5  # Индексы: 5, 6, 7, 8
            multiplier = persents[db_index]

            btn = QPushButton(f'x{multiplier}')
            btn.setMinimumHeight(40)
            btn.setFont(create_Font(12, True))

            # Рассчитываем точный процент для этого множителя прямо на текущем шаге цикла
            calculated_chance = 100.0 / multiplier

            # Передаем готовый вычисленный шанс в lambda
            btn.clicked.connect(lambda checked, c=calculated_chance: self.chance_changed_with_skin(c))
            btn.setFont(create_Font(12, True))
            self.disableBtns.append(btn)
            self.gradeLayout.addWidget(btn)
            self.gradeButtons.append(btn)

        self.VerticalLeftLayout.addLayout(self.persentLayout, stretch=1)
        self.VerticalRightLayout.addLayout(self.gradeLayout, stretch=1)

    def create_cost_widgets(self):
        self.inventoryWidgets = QHBoxLayout()

        self.inventory_min_cost_ledit = QLineEdit()
        self.inventory_min_cost_ledit.setPlaceholderText("Min cost")
        self.inventory_min_cost_ledit.setMinimumHeight(40)
        self.inventory_min_cost_ledit.setFont(create_Font(12, True))
        self.inventory_min_cost_ledit.textChanged.connect(self.inventory_ledit_changed)
        self.inventoryWidgets.addWidget(self.inventory_min_cost_ledit)

        self.inventory_max_cost_ledit = QLineEdit()
        self.inventory_max_cost_ledit.setPlaceholderText("Max cost")
        self.inventory_max_cost_ledit.setMinimumHeight(40)
        self.inventory_max_cost_ledit.setFont(create_Font(12, True))
        self.inventory_max_cost_ledit.textChanged.connect(self.inventory_ledit_changed)
        self.inventoryWidgets.addWidget(self.inventory_max_cost_ledit)

        self.inventory_search_ledit = QLineEdit()
        self.inventory_search_ledit.setPlaceholderText("Search")
        self.inventory_search_ledit.setFont(create_Font(12, True))
        self.inventory_search_ledit.setMinimumHeight(40)
        self.inventoryWidgets.addWidget(self.inventory_search_ledit)

        self.inventoryMinMaxBtn = QPushButton("")
        self.inventoryMinMaxBtn.setMinimumSize(40,40)
        self.inventoryWidgets.addWidget(self.inventoryMinMaxBtn)

        self.upgraderWidgets = QHBoxLayout()

        self.upgrader_min_cost_ledit = QLineEdit()
        self.upgrader_min_cost_ledit.setPlaceholderText("Min cost")
        self.upgrader_min_cost_ledit.setMinimumHeight(40)
        self.upgrader_min_cost_ledit.setFont(create_Font(12, True))
        self.upgrader_min_cost_ledit.textChanged.connect(self.upgrading_ledit_changed)
        self.upgraderWidgets.addWidget(self.upgrader_min_cost_ledit)

        self.upgrader_max_cost_ledit = QLineEdit()
        self.upgrader_max_cost_ledit.setPlaceholderText("Max cost")
        self.upgrader_max_cost_ledit.setMinimumHeight(40)
        self.upgrader_max_cost_ledit.setFont(create_Font(12, True))
        self.upgrader_max_cost_ledit.textChanged.connect(self.upgrading_ledit_changed)
        self.upgraderWidgets.addWidget(self.upgrader_max_cost_ledit)

        self.upgrader_search_ledit = QLineEdit()
        self.upgrader_search_ledit.setPlaceholderText("Search")
        self.upgrader_search_ledit.setFont(create_Font(12, True))
        self.upgrader_search_ledit.setMinimumHeight(40)
        self.upgraderWidgets.addWidget(self.upgrader_search_ledit)

        self.upgraderMinMaxBtn = QPushButton("")
        self.upgraderMinMaxBtn.setMinimumSize(40, 40)
        self.upgraderWidgets.addWidget(self.upgraderMinMaxBtn)

        self.VerticalRightLayout.addLayout(self.upgraderWidgets, stretch=1)
        self.VerticalLeftLayout.addLayout(self.inventoryWidgets, stretch=1)

    def create_skin_icons(self):
        self.LeftSkinLayout = QVBoxLayout()

        self.inventorySkinIconLabel = QLabel()
        self.inventorySkinIconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inventorySkinIconLabel.setMouseTracking(True)
        self.inventorySkinIconLabel.setScaledContents(False)
        self.inventorySkinIconLabel.setMinimumSize(250, 250)
        self.inventorySkinIconLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)  # И сюда тоже
        self.inventorySkinIconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inventorySkinIconLabel.setStyleSheet(set_inventory_skin_style(self.inventory_skin_rarity))

        img_path = ''
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            padding = 15
            target_width = self.inventorySkinIconLabel.minimumWidth() - padding
            target_height = self.inventorySkinIconLabel.minimumHeight() - padding

            self.inventorySkinIconLabel.setPixmap(pixmap.scaled(
                target_width, target_height,
                Qt.AspectRatioMode.KeepAspectRatio,  # Сохраняем пропорции оружия
                Qt.TransformationMode.SmoothTransformation  # Включаем качественное сглаживание
            ))

        self.LeftSkinLayout.addWidget(self.inventorySkinIconLabel,stretch=5)

        self.inventorySkinNameLabel = QLabel('Выберите Скин')
        self.inventorySkinNameLabel.setMinimumSize(200, 20)
        self.inventorySkinNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inventorySkinNameLabel.setFont(create_Font(12, True))
        self.inventorySkinNameLabel.setWordWrap(True)
        self.inventorySkinNameLabel.setStyleSheet("color: white; background: transparent;")

        self.inventorySkinCostLabel = QLabel('Цена:')
        self.inventorySkinCostLabel.setMinimumSize(200, 20)
        self.inventorySkinCostLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.inventorySkinCostLabel.setFont(create_Font(12, True))
        self.inventorySkinCostLabel.setWordWrap(True)
        self.inventorySkinCostLabel.setStyleSheet("color: white; background: transparent;")

        self.LeftSkinLayout.addWidget(self.inventorySkinNameLabel, stretch=1)
        self.LeftSkinLayout.addWidget(self.inventorySkinCostLabel, stretch=1)
        self.HorizontalUpperLayout.addLayout(self.LeftSkinLayout, stretch=3)

        self.roulette = UpgraderRouletteWidget()
        self.roulette.animation_ended.connect(self.animation_ended_event)
        self.HorizontalUpperLayout.addWidget(self.roulette, stretch=3)

        # правое окно со скином
        self.RightSkinLayout = QVBoxLayout()

        self.upgradedSkinIconLabel = QLabel()
        self.upgradedSkinIconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upgradedSkinIconLabel.setMouseTracking(True)
        self.upgradedSkinIconLabel.setScaledContents(False)
        self.upgradedSkinIconLabel.setMinimumSize(250, 250)
        self.upgradedSkinIconLabel.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)  # И сюда тоже
        self.upgradedSkinIconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upgradedSkinIconLabel.setStyleSheet(set_inventory_skin_style(self.inventory_skin_rarity))

        self.RightSkinLayout.addWidget(self.upgradedSkinIconLabel, stretch=5)

        self.upgradedSkinNameLabel = QLabel('Выберите Скин')
        self.upgradedSkinNameLabel.setMinimumSize(200, 30)
        self.upgradedSkinNameLabel.setFont(create_Font(12, True))
        self.upgradedSkinNameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upgradedSkinNameLabel.setWordWrap(True)
        self.upgradedSkinNameLabel.setStyleSheet("color: white; background: transparent;")

        self.upgradedSkinCostLabel = QLabel('Цена:')
        self.upgradedSkinCostLabel.setMinimumSize(200, 30)
        self.upgradedSkinCostLabel.setFont(create_Font(12, True))
        self.upgradedSkinCostLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upgradedSkinCostLabel.setWordWrap(True)
        self.upgradedSkinCostLabel.setStyleSheet("color: white; background: transparent;")

        self.RightSkinLayout.addWidget(self.upgradedSkinNameLabel, stretch=1)
        self.RightSkinLayout.addWidget(self.upgradedSkinCostLabel, stretch=1)
        self.HorizontalUpperLayout.addLayout(self.RightSkinLayout, stretch=3)

    def inventory_skin_clicked(self):
        self.inventory_skin_info = self.inventorySkins.upgrading_skin

        self.inventorySkinIconLabel.setStyleSheet(set_inventory_skin_style(self.inventory_skin_info[4]))
        skin_full_name = get_full_name(self.inventory_skin_info[2],
                                       self.inventory_skin_info[3], self.inventory_skin_info[5])
        self.inventorySkinNameLabel.setText(skin_full_name)
        self.inventorySkinCostLabel.setText(f'Cost: {self.inventory_skin_info[6]}$')

        img_path = f'images/skins/{replace_symbols(self.inventory_skin_info[2])}'
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            if not pixmap.isNull():
                padding = 20
                target_w = self.inventorySkinIconLabel.width() - padding
                target_h = self.inventorySkinIconLabel.height() - padding

                scaled_pixmap = pixmap.scaled(
                    target_w, target_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.inventorySkinIconLabel.setPixmap(scaled_pixmap)
        self.info_about_skins_changed()

    def delete_inventory_skin_image(self):
        self.inventorySkinIconLabel.setStyleSheet(set_inventory_skin_style(self.inventory_skin_rarity))
        self.inventorySkinNameLabel.setText('Выберите скин')
        self.inventorySkinCostLabel.setText('Cost: $')

        self.inventorySkinIconLabel.clear()
        self.info_about_skins_changed()

    def upgraded_skin_clicked(self):
        self.upgraded_skin_info = self.skinVariants.upgrading_skin

        self.upgradedSkinIconLabel.setStyleSheet(set_inventory_skin_style(self.upgraded_skin_info[-1]))

        self.upgradedSkinNameLabel.setText(self.upgraded_skin_info[1])
        self.upgradedSkinCostLabel.setText(f'Cost: {self.upgraded_skin_info[2]}$')

        img_path = f'images/skins/{replace_symbols(self.upgraded_skin_info[0])}'
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            padding = 40
            target_w = self.upgradedSkinIconLabel.width() - padding
            target_h = self.upgradedSkinIconLabel.height() - padding

            scaled_pixmap = pixmap.scaled(
                target_w, target_h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.upgradedSkinIconLabel.setPixmap(scaled_pixmap)
        self.info_about_skins_changed()

    def info_about_skins_changed(self):
        invent_skin_cost = None
        upgraded_skin_cost = None
        new_persent = None
        if self.inventory_skin_info is not None:
            invent_skin_cost = self.inventory_skin_info[6]
        if self.upgraded_skin_info is not None:
            upgraded_skin_cost = self.upgraded_skin_info[2]
        if invent_skin_cost is not None and upgraded_skin_cost is not None:
            new_persent = round((invent_skin_cost / upgraded_skin_cost) * 100, 2)
            self.chance_changed(new_persent)


    def chance_changed_with_skin(self, point):
        self.roulette.animate_chance_change(point)
        if self.inventory_skin_info is not None:
            cost = self.inventory_skin_info[6]
            min_cost = round(cost / (point * 0.0105), 2)
            max_cost = round(cost / (point * 0.0095), 2)
            self.upgrader_min_cost_ledit.setText(f'{min_cost:.2f}')
            self.upgrader_max_cost_ledit.setText(f'{max_cost:.2f}')
            self.upgrading_ledit_changed()
            self.skinVariants.choosing_upgraded_item(self.skinVariants.saved_skins[0])
            self.info_about_skins_changed()


    def chance_changed(self, point):
        self.roulette.animate_chance_change(point)

    def inventory_ledit_changed(self):
        cost_min = self.inventory_min_cost_ledit.text()
        cost_max = self.inventory_max_cost_ledit.text()
        if cost_min is None or not is_float(cost_min):
            cost_min = 0
        else:
            cost_min = float(cost_min)
        if cost_max is None or not is_float(cost_max):
            cost_max = 1000000
        else:
            cost_max = float(cost_max)
        self.inventorySkins.download_skins_from_inventory(cost_min, cost_max)

    def upgrading_ledit_changed(self):
        cost_min = self.upgrader_min_cost_ledit.text()
        cost_max = self.upgrader_max_cost_ledit.text()
        if cost_min is None or not is_float(cost_min):
            cost_min = 0
        else:
            cost_min = float(cost_min)
        if cost_max is None or not is_float(cost_max):
            cost_max = 1000000
        else:
            cost_max = float(cost_max)
        self.skinVariants.download_skin_variants(cost_min, cost_max)

    def upgrade_btn_clicked(self):
        for btn in self.disableBtns:
            btn.setEnabled(False)
        dropped_chance = round(random.uniform(0, 100), 2)
        if self.inventory_skin_info is not None and self.upgraded_skin_info is not None:
            invent_cost = self.inventory_skin_info[6]
            upgraded_cost = self.upgraded_skin_info[2]
            chance = round((invent_cost / upgraded_cost) * 100, 2)
            delete_item(self.inventory_skin_info[0])
            if chance >= dropped_chance:
                inf = self.upgraded_skin_info
                add_skin_into_inventory(get_player_id(), inf[0], inf[3], inf[5], inf[4], inf[2])
            self.roulette.start_animation(180 * (dropped_chance / 100), chance >= dropped_chance)
            self.inventory_skin_info = None

    def animation_ended_event(self):
        for btn in self.disableBtns:
            btn.setEnabled(True)
        self.delete_inventory_skin_image()
        self.inventorySkins.download_skins_from_inventory()



