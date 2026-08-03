import random

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QScrollArea, QWidget, QFrame, QVBoxLayout, QGridLayout

from choosingCaseBtn import SkinButtonWidget, SkinButtonUpgraderWidget
from AllConstants import *


def random_float(skinname, flt):
    rarity = flt

    skininfo = get_info_from_json('skins.json')[skinname]
    rarityBorders = skininfo["float"]
    if rarityBorders != -1:
        if rarity[0] < rarityBorders[0]:
            rarity[0] = rarityBorders[0]
        if rarity[1] > rarityBorders[1]:
            rarity[1] = rarityBorders[1]
        return random.uniform(rarity[0], rarity[1])
    else:
        return random.uniform(0, 1)


def sorting_changes(min_price=0, max_price=1000000, name=''):
    all_skins = get_info_from_json('prices.json')
    all_list = [[i, all_skins[i]] for i in all_skins]
    ret_list = []
    for skin in all_list:
        if min_price <= skin[1] <= max_price:
            if name == '':
                ret_list.append(skin)
            else:
                spl_names = name.split(' ')
                b = True
                for n in spl_names:
                    if n.lower() not in skin[0].lower():
                        b = False
                        break
                if b:
                    ret_list.append(skin)
    return ret_list

def sort_skin_by_cost(skins, min_price=0, max_price=1000000, name=''):
    ret_skins = []
    for skin in skins:
        if min_price <= skin[-1] <= max_price:
            if name.lower() in skin[2].lower() or name == '':
                ret_skins.append(skin)
    return ret_skins



class SkinsScroll(QWidget):
    item_selected = pyqtSignal()

    def __init__(self, skin_from_invent):
        super().__init__()
        self.saved_skins = []
        self.skin_from_invent = skin_from_invent

        self.upgrading_skin = None

        self.create_window()
        if skin_from_invent:
            self.download_skins_from_inventory()
        else:
            self.download_skin_variants()

    def create_window(self):
        self.SkinScrollArea = QScrollArea(self)
        self.SkinScrollArea.setWidgetResizable(True)

        self.gridWithSkins = QGridLayout()
        self.gridWithSkins.setContentsMargins(10, 10, 10, 10)
        self.gridWithSkins.setSpacing(10)

        self.additWidget = QWidget()
        self.additWidget.setLayout(self.gridWithSkins)
        self.SkinScrollArea.setWidget(self.additWidget)

    def clear_grid_layout(self):
        while self.gridWithSkins.count():
            item = self.gridWithSkins.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def download_skins_from_inventory(self, min_price=0, max_price=1000000, name=''):
        self.clear_grid_layout()
        self.upgrading_skin = None
        self.all_skins = load_info_about_skins(get_player_id())
        self.all_skins = sort_skin_by_cost(self.all_skins, min_price, max_price, name)
        self.all_skins.sort(key=lambda x: x[-1], reverse=True)
        pos_x = 0
        pos_y = 0
        for skin in self.all_skins:
            skin_full_name = get_full_name(skin[2], skin[3], skin[-2])

            imgname = f'images/skins/{replace_symbols(skin[2])}'

            new_skin = SkinButtonUpgraderWidget(skin_full_name, skin[2], skin[3], 100, skin[0], imgname)
            new_skin.item_selected.connect(lambda s_id=skin[0]: self.inventory_skin_selected(s_id))
            self.gridWithSkins.addWidget(new_skin, pos_y, pos_x)
            pos_x += 1
            if pos_x >= 4:
                pos_x = 0
                pos_y += 1

    def inventory_skin_selected(self, skin_id):
        info = get_info_about_skin(skin_id)
        self.upgrading_skin = info
        self.item_selected.emit()

    def download_skin_variants(self, min_price=0, max_price=1000000, name=''):
        self.clear_grid_layout()
        self.all_skins = sorting_changes(min_price, max_price, name)
        self.all_skins.sort(key=lambda x: x[1], reverse=True)
        pos_x = 0
        pos_y = 0
        self.saved_skins.clear()

        for ind, skin in enumerate(self.all_skins):
            if ind <= 50:
                skin_short_name = get_short_name(skin[0])
                float_range = random_float(skin_short_name, get_flt_from_name(skin[0]))

                imgname = f'images/skins/{replace_symbols(skin_short_name)}'

                new_skin = SkinButtonUpgraderWidget(skin[0], skin_short_name, float_range, 100, 0, imgname)
                new_skin.item_selected.connect(lambda s_id=skin[0]: self.choosing_upgraded_item(s_id))
                self.saved_skins.append(skin[0])
                self.gridWithSkins.addWidget(new_skin, pos_y, pos_x)
                pos_x += 1
                if pos_x >= 4:
                    pos_x = 0
                    pos_y += 1
            else:
                break

    def choosing_upgraded_item(self, skinname):
        price = get_info_from_json('prices.json')[skinname]
        float_range = random_float(get_short_name(skinname), get_flt_from_name(skinname))
        short_name = get_short_name(skinname)
        rarity = get_info_from_json('skins.json')[short_name]['rarity'][0]
        stattrak = False
        if 'StatTrak' in skinname:
            stattrak = True
        self.upgrading_skin = [short_name, skinname, price, float_range, stattrak, rarity]
        self.item_selected.emit()

