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

check_skin()