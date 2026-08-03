import json
import sqlite3

from AllConstants import get_info_from_json


def create_db():
    db = sqlite3.connect('players.db')
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE players (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    money FLOAT NOT NULL)''')

    cursor.execute('''CREATE TABLE skins (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    skin_name TEXT NOT NULL,
    float_value FLOAT NOT NULL,
    rarity TEXT NOT NULL,
    stattrak BOOLEAN NOT NULL,
    cost FLOAT NOT NULL,
    FOREIGN KEY (player_id) REFERENCES players(id))
    ''')
    db.commit()
    db.close()

def add_player(name, money):
    db = sqlite3.connect('players.db')
    cursor = db.cursor()
    cursor.execute(''' INSERT INTO players (name, money) VALUES (?, ?)''', (name, money))
    db.commit()
    db.close()

def check_skin():
    file = open(f'newskins.json', 'r', encoding='utf-8')
    skins = json.load(file)
    file.close()

    for i in skins:
        if 'Doppler' in i:
            print(i)

def clear_prices():
    collectPrices = {}
    skinPrices = {}
    file = open(f'prices.json', 'r', encoding='utf-8')
    prices = json.load(file)
    file.close()
    for i in prices:
        if '(' not in i:
            if '★' not in i:
                collectPrices[i] = prices[i]
            else:
                skinPrices[i] = prices[i]
        else:
            ind = i.index('(')
            fls = ['(Battle-Scarred)', '(Factory New)', '(Field-Tested)', '(Minimal Wear)', '(Well-Worn)']
            b = False
            for j in fls:
                if j in i:
                    b = True
            if b:
                skinPrices[i] = prices[i]

    new = open('prices.json', 'w', encoding='utf-8')
    json.dump(skinPrices, new)
    new.close()

def printf():
    file = open(f'prices.json', 'r', encoding='utf-8')
    prices = json.load(file)
    file.close()
    for i in prices:
        if '★' in i:
            print(i)

def print_skin():
    file = open(f'prices.json', 'r', encoding='utf-8')
    skins = json.load(file)
    file.close()
    newdata = {}
    for i in skins:
        if 'BlackPearl' in i:
            name = list(i)
            name[i.rindex('P')] = 'p'
            newdata[''.join(name)] = skins[i]
        else:
            newdata[i] = skins[i]
    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump(newdata, f)





