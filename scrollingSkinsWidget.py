import os.path
import random

from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QLabel, \
    QGridLayout, QSizePolicy, QFrame, QMessageBox, QDialog
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QUrl, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from SkinDialog import SkinDropDialog

from AllConstants import *


class SpinItemWidget(QWidget):
    def __init__(self,item_size, img_info, color, skin_name):
        super().__init__()
        self.setFixedSize(item_size, int(WINDOWSIZE[0] *  0.18))

        self.Vlayout = QVBoxLayout(self)

        self.iconLbl = QLabel()
        icon_size = item_size
        self.iconLbl.setFixedSize(icon_size, icon_size)
        self.iconLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.iconLbl.setStyleSheet(f''' background-color: {color}; ''')

        img_path = img_info
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            self.iconLbl.setPixmap(pixmap.scaled(
                icon_size, icon_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        self.Vlayout.addWidget(self.iconLbl)

        self.textLbl = QLabel()
        self.textLbl.setFixedSize(icon_size, int(icon_size * 0.2))
        self.textLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textLbl.setFont(NAMEFONT)
        self.textLbl.setText(skin_name)
        self.Vlayout.addWidget(self.textLbl)



class ScrollingSkinsWidget(QWidget):
    item_sold = pyqtSignal()

    def __init__(self, data, key):
        super().__init__()
        self.setWindowTitle(data['case'])
        self.setFixedSize(WINDOWSIZE[0], WINDOWSIZE[1])

        self.data = data
        self.key = key

        self.create_window()

    def create_window(self):
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ScrollingArea = QScrollArea()
        self.ScrollingArea.setWidgetResizable(True)
        self.ScrollingArea.setFixedSize(int(WINDOWSIZE[0] *  0.8), int(WINDOWSIZE[0] *  0.2))
        self.ScrollingArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Прячем скроллбар
        self.ScrollingArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ScrollingArea.setStyleSheet("border: 2px solid #3d3d3d; background-color: #252525;")

        self.tape_widget = QWidget()
        self.tape_layout = QHBoxLayout(self.tape_widget)
        self.tape_layout.setContentsMargins(0, 0, 0, 0)
        self.tape_layout.setSpacing(0)

        self.ScrollingArea.setWidget(self.tape_widget)
        self.layout.addWidget(self.ScrollingArea, alignment=Qt.AlignmentFlag.AlignCenter)

        self.pointer = QLabel("▼", self)
        self.pointer.setStyleSheet("color: #eb4b4b; font-size: 16px; margin-top: -10px;")
        self.pointer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.pointer)

        self.openCaseBtn = QPushButton('Open Case')
        self.openCaseBtn.setFixedSize(int(WINDOWSIZE[0] * 0.2), int(WINDOWSIZE[1] * 0.1))
        self.openCaseBtn.setStyleSheet("""
                   QPushButton { background-color: #087800; color: black; font-weight: bold; border-radius: 15px; border: 3px solid #000000; }
                   QPushButton:hover { background-color: #065700; }
                   QPushButton:disabled { background-color: #555; color: #888; }
               """)
        self.openCaseBtn.setFont(BTNFONT)
        self.openCaseBtn.clicked.connect(self.open_btn_pressed)
        self.layout.addWidget(self.openCaseBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.gridWithItems = QGridLayout()
        self.gridWithItems.setSpacing(10)
        self.gridWithItems.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridWithItems.setContentsMargins(10, 10, 10, 10)

        self.gridScroll= QScrollArea()
        self.gridScroll.setWidgetResizable(True)
        self.gridWidget = QWidget()
        self.gridWidget.setLayout(self.gridWithItems)
        self.gridScroll.setWidget(self.gridWidget)

        self.skinsInfo = get_info_from_json('skins.json')
        self.allskins = []
        skinIconSize = (WINDOWSIZE[0] - 20 * 7) // 6
        pos_x, pos_y=0,0


        for skin in self.data['skins']:
            btn_skin = QPushButton()
            btn_skin.setStyleSheet(f'background-color: {self.skinsInfo[skin]['rarity'][0]};')
            btn_skin.setFixedSize(skinIconSize, skinIconSize)

            self.gridWithItems.addWidget(btn_skin, pos_y, pos_x)
            pos_x += 1
            if pos_x >= 5:
                pos_x = 0
                pos_y += 1
            self.allskins.append(skin)
        if 'rare_items' in self.data.keys():
            btn_skin = QPushButton()
            btn_skin.setStyleSheet(f'background-color: #e4ae39;')
            btn_skin.setFixedSize(skinIconSize, skinIconSize)

            self.gridWithItems.addWidget(btn_skin, pos_y, pos_x)

        self.layout.addWidget(self.gridScroll)

    def clear_tape(self):
        """Очищает верхнюю ленту от старых виджетов перед новым прокрутом"""
        while self.tape_layout.count():
            item = self.tape_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def open_btn_pressed(self):
        self.openCaseBtn.setEnabled(False)
        self.clear_tape()
        self.ScrollingArea.horizontalScrollBar().setValue(0)

        item_width = int(WINDOWSIZE[0] * 0.15)
        self.winning_index = random.randint(60, 65)
        self.droppedSkin = self.randomizeItems(True)
        print(self.droppedSkin)

        self.tape_skins = []
        for i in range(70):
            if i != self.winning_index:
                selectedSkin = self.randomizeItems(False)
            else:
                selectedSkin = self.droppedSkin
            color = self.skinsInfo[selectedSkin[0]]['rarity'][0]
            name = selectedSkin[0]
            if '★' in name:
                name = 'rare_item'
                color = '#e4ae39'
            newItem = SpinItemWidget(item_width, '', color, name)
            self.tape_skins.append(newItem)
            self.tape_layout.addWidget(newItem)
            self.tape_skins.append(newItem)

        scroll_center = self.ScrollingArea.width() / 2
        winning_item_x = 10 + self.winning_index * item_width

        target_value = int(winning_item_x + (item_width / 2) - scroll_center)
        target_value += random.randint(-int(item_width * 0.3), int(item_width * 0.3))

        self.animation = QPropertyAnimation(self.ScrollingArea.horizontalScrollBar(), b"value")
        self.animation.setDuration(6000)  # Время анимации (4.5 секунды)
        self.animation.setStartValue(0)
        self.animation.setEndValue(target_value)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.caseSound = QSoundEffect()
        self.caseSound.setSource(QUrl.fromLocalFile(os.path.abspath('soundEffects/go-new-gambling.wav')))
        self.caseSound.setVolume(0.5)

        self.itemDroppedSound = QSoundEffect()
        self.itemDroppedSound.setSource(QUrl.fromLocalFile(os.path.abspath('soundEffects/gambling.wav')))
        self.itemDroppedSound.setVolume(0.5)

        self.animation.finished.connect(lambda: self.animation_finished())
        self.caseSound.play()
        self.animation.start()

    def animation_finished(self):
        self.caseSound.stop()
        self.itemDroppedSound.play()
        self.openCaseBtn.setEnabled(True)
        skin_name = ''
        if self.droppedSkin[2]:
            skin_name += 'StatTrak™ '
        skin_name += self.droppedSkin[0]
        skin_name += give_skin_floatname(self.droppedSkin[1])

        self.droppedSkinDialog = SkinDropDialog(skin_name, self.droppedSkin[1], '')
        if self.droppedSkinDialog.exec() == QDialog.DialogCode.Accepted:
            if self.droppedSkinDialog.user_choice == "sell":
                sell_item(skin_name)
                self.item_sold.emit()
            elif self.droppedSkinDialog.user_choice == "save":
                self.add_item_into_inventory(skin_name)

    def add_item_into_inventory(self, skin_full_name):
        player_id = get_player_id()
        skin_name = self.droppedSkin[0]
        skin_lft = self.droppedSkin[1]
        skin_st = self.droppedSkin[2]
        skin_rarity = self.skinsInfo[skin_name]['rarity'][0]
        cost = get_info_from_json('prices.json')[skin_full_name]

        add_skin_into_inventory(player_id, skin_name, skin_lft, skin_rarity, skin_st, cost)

    def randomizeItems(self, droppedSkin=False):
        # rare - 1:7992, epic - 7993:9590, leg - 9591:9910, tai - 9911:9974, knife - 9975:9999

        # comm - 1:800000, uncom 800001:960000, rare - 960001:992000,
        # epic - 992001:998400, leg - 998401:999680, tai - 999680:999999
        neededDigit = random.randint(1, 9999)
        skinName = None
        items_rarity = {}
        for i in self.data['skins']:
            if self.skinsInfo[i]['rarity'][1] in items_rarity:
                items_rarity[self.skinsInfo[i]['rarity'][1]].append(i)
            else:
                items_rarity[self.skinsInfo[i]['rarity'][1]] = [i]

        if neededDigit <= 7992:
            skinName = random.choice(items_rarity['rarity_rare_weapon'])
        elif neededDigit <= 9590:
            skinName = random.choice(items_rarity['rarity_mythical_weapon'])
        elif neededDigit <= 9910:
            skinName = random.choice(items_rarity['rarity_legendary_weapon'])
        elif neededDigit <= 9974:
            skinName = random.choice(items_rarity['rarity_ancient_weapon'])
        elif droppedSkin:
            skinName = random.choice(self.data['rare_items'])
        else:
            skinName = random.choice(items_rarity['rarity_ancient_weapon'])
        skindata = self.skinsInfo[skinName]
        skin_float = 0.0
        stattrak = False
        if skindata['stattrak']:
            stattrak = random.randint(1, 10) == 1
        skin_float = random.uniform(skindata['float'][0], skindata['float'][1])
        return skinName, skin_float, stattrak








