import json
import sqlite3

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

def get_player_id():
    with open('playerID.txt', 'r', encoding='utf-8') as file:
        Id = int(file.readlines()[0])
        return Id

def set_player_id(player_id):
    with open('playerID.txt', 'w', encoding='utf-8') as file:
        file.write(str(player_id))

def get_info_about_player(player_id):
    db = sqlite3.connect('jsonFiles/players.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM players WHERE id = ?', (int(player_id),))
    info = cursor.fetchone()
    db.close()
    return info

def add_skin_into_inventory(player_id, skin, flt, rarity,stattrak, cost):
    db = sqlite3.connect('jsonFiles/players.db')
    cursor = db.cursor()
    cursor.execute('''
            INSERT INTO skins (player_id, skin_name, float_value, rarity, stattrak, cost) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_id, skin, flt, rarity, stattrak, cost))
    db.commit()
    db.close()

def sell_item(skin_full_name):
    player_id = get_player_id()
    cost = get_info_from_json('prices.json')[skin_full_name]
    sell_skin(player_id, cost)

def sell_skin(player_id, cost):
    db = sqlite3.connect('jsonFiles/players.db')
    cursor = db.cursor()
    cursor.execute(""" UPDATE players SET money = money + ? WHERE id = ? """, (cost, player_id))
    db.commit()
    db.close()

def sell_skin_from_inventory(skin_id, skin_name):
    sell_item(skin_name)
    db = sqlite3.connect('jsonFiles/players.db')
    cursor = db.cursor()
    cursor.execute(''' DELETE FROM skins WHERE id = ? ''', (skin_id,))
    db.commit()
    db.close()

def load_info_about_skins(player_id):
    db = sqlite3.connect('jsonFiles/players.db')
    cursor = db.cursor()
    cursor.execute(''' SELECT * FROM skins WHERE player_id = ? ''', (int(player_id),))
    return cursor.fetchall()

def replace_symbols(name):
    return name.replace(' ', '').replace('|', '').replace('★', '')