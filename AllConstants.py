import json

from PyQt6.QtGui import QFont

MAINMENUSIZE = (400, 600)
WINDOWSIZE = (1000, 800)

BTNFONT = QFont()
BTNFONT.setPointSize(12)
BTNFONT.setBold(True)

CASHVALUE = {
    'DOLLARS': 78.75,
    'RUBLES': 0.013
}

RARITYNAME = {
    'bs':' (Battle-Scarred)',
    'fn':' (Factory New)',
    'ft':' (Field-Tested)',
    'mw':' (Minimal Wear)',
    'ww':' (Well-Worn)'

}


def get_info_from_json(filename):
    file = open(f'jsonFiles/{filename}', 'r', encoding='utf-8')
    collections = json.load(file)
    file.close()
    return collections