import json

from PyQt6.QtGui import QFont

MAINMENUSIZE = (400, 600)
WINDOWSIZE = (1000, 800)

BTNFONT = QFont()
BTNFONT.setPointSize(12)
BTNFONT.setBold(True)

NAMEFONT = QFont()
NAMEFONT.setPointSize(11)

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

def give_skin_floatname(floatrange):
    if floatrange <= 0.07:
        return RARITYNAME['fn']
    elif floatrange <= 0.15:
        return RARITYNAME['mw']
    elif floatrange <= 0.38:
        return RARITYNAME['ft']
    elif floatrange <= 0.45:
        return RARITYNAME['ww']
    return RARITYNAME['bs']

def get_info_from_json(filename):
    file = open(f'jsonFiles/{filename}', 'r', encoding='utf-8')
    collections = json.load(file)
    file.close()
    return collections