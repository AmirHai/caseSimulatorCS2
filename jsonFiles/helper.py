import json

skins = json.load(open('skins.json', 'r', encoding='utf-8'))
collections = json.load(open('collections.json', 'r', encoding='utf-8'))
prices = json.load(open('prices.json', 'r', encoding='utf-8'))
for i in collections:
    print(i)

