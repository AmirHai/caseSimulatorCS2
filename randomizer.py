import random
from AllConstants import *

def randomizeItemsA(collection, droppedSkin=False):
    AllSkinsInCol = get_info_from_json('collections.json')[collection]
    skins = get_info_from_json('skins.json')
    AllRarities = []
    RarityItems = {}
    for skin in AllSkinsInCol['skins']:
        rarity = skins[skin]['rarity'][0]
        if rarity not in AllRarities:
            AllRarities.append(rarity)

        if rarity not in RarityItems:
            RarityItems[rarity] = [skin]
        else:
            RarityItems[rarity].append(skin)

    if 'rare_items' in AllSkinsInCol:
        AllRarities.append('#e4ae39')

    knifeChance = 0.2558
    chances = []
    baseChance = None
    amount = len(AllRarities)
    if '#e4ae39' in AllRarities:
        baseChance = (100 - knifeChance) * 0.8 / (1 - 0.2**amount)
        chances.append(round(baseChance, 4))
        for i in range(1, amount - 1):
            chances.append(round(chances[i-1] / 5, 4))
        chances.append(knifeChance)
    else:
        baseChance = 80 / (1 - 0.2 ** amount)
        chances.append(round(baseChance, 4))
        for i in range(1, amount):
            chances.append(round(chances[i-1] / 5, 4))

    drop = random.uniform(0, sum(chances))
    droppedRarity = None
    print(sum(chances))

    for i in range(len(chances)):
        drop -= chances[i]
        if drop <= 0:
            droppedRarity = AllRarities[i]
            break
    if (not droppedSkin) and droppedRarity == '#e4ae39':
        droppedRarity = AllRarities[-2]

    neededSkin = None
    if droppedRarity == '#e4ae39':
        neededSkin = random.choice(AllSkinsInCol['rare_items'])
        if 'Doppler' in neededSkin:
            neededSkin = getDopplersPhase(neededSkin)
    else:
        neededSkin = random.choice(RarityItems[droppedRarity])

    if not droppedSkin:
        return neededSkin, 0.0, False

    stattrak = False
    if skins[neededSkin]['stattrak']:
        stattrak = random.randint(1, 10) == 5
    float_range = skins[neededSkin]["float"]
    skin_float = random.uniform(float_range[0], float_range[1])
    return neededSkin, skin_float, stattrak

def getDopplersPhase(skin_name):
    AllSkins = get_info_from_json('skins.json')
    AllPhases = []
    for skin in AllSkins:
        if skin_name in skin:
            AllPhases.append(skin)
    ret = random.choice(AllPhases)
    return ret


