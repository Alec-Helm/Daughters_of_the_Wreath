import pygame
import math
import csv
from sys import exit


def BHP_fun(character):
    character[0]["HP"] += 2
    character[0]["BODY"] += 1
    return character

def BSR_fun(character):
    character[0]["Slow Regen"] += 1
    character[0]["BODY"] += 1
    return character

def BD_fun(character):
    character[0]["Durability"] += 1
    character[0]["BODY"] += 1
    return character

def Bstrength_fun(character):
    character[0]["Strength"] += 1
    character[0]["BODY"] += 1
    return character

def BAtheletics_fun(character):
    if "Atheletics" in character[1]:
        character[1]["Atheletics"] += 1
    else:
        character[1].update({"Atheletics": 1})
    character[0]["BODY"] += 1
    return character

def BHeavyPrecision_fun(character):
    if "Heavy Precision" in character[1]:
        character[1]["Heavy Precision"] += 1
    else:
        character[1].update({"Heavy Precision": 1})
    character[0]["BODY"] += 1
    return character

def BStandardPrecision_fun(character):
    if "Standard Precision" in character[1]:
        character[1]["Standard Precision"] += 1
    else:
        character[1].update({"Standard Precision": 1})
    character[0]["BODY"] += 1
    return character

def BLightPrecision_fun(character):
    if "Light Precision" in character[1]:
        character[1]["Light Precision"] += 1
    else:
        character[1].update({"Light Precision": 1})
    character[0]["BODY"] += 1
    return character

def BRangedPrecision_fun(character):
    if "Ranged Precision" in character[1]:
        character[1]["Ranged Precision"] += 1
    else:
        character[1].update({"Ranged Precision": 1})
    character[0]["BODY"] += 1
    return character

def BThrownPrecision_fun(character):
    if "Thrown Precision" in character[1]:
        character[1]["Thrown Precision"] += 1
    else:
        character[1].update({"Thrown Precision": 1})
    character[0]["BODY"] += 1
    return character

def BShieldPrecision_fun(character):
    if "Shield Precision" in character[1]:
        character[1]["Shield Precision"] += 1
    else:
        character[1].update({"Shield Precision": 1})
    character[0]["BODY"] += 1
    return character

def BSlashingPrecision_fun(character):
    if "Slashing Precision" in character[1]:
        character[1]["Slashing Precision"] += 1
    else:
        character[1].update({"Slashing Precision": 1})
    character[0]["BODY"] += 1
    return character

def BPiercingPrecision_fun(character):
    if "Piercing Precision" in character[1]:
        character[1]["Piercing Precision"] += 1
    else:
        character[1].update({"Piercing Precision": 1})
    character[0]["BODY"] += 1
    return character

def BBludgeoningPrecision_fun(character):
    if "Bludgeoning Precision" in character[1]:
        character[1]["Bludgeoning Precision"] += 1
    else:
        character[1].update({"Bludgeoning Precision": 1})
    character[0]["BODY"] += 1
    return character

def BStrength_fun(character):
    character[0]["Strength"] += 1
    character[0]["BODY"] += 1
    return character

def BHeavyDamage_fun(character):
    if "Heavy Damage" in character[1]:
        character[1]["Heavy Damage"] += 1
    else:
        character[1].update({"Heavy Damage": 1})
    character[0]["BODY"] += 1
    return character

def BStandardDamage_fun(character):
    if "Standard Damage" in character[1]:
        character[1]["Standard Damage"] += 1
    else:
        character[1].update({"Standard Damage": 1})
    character[0]["BODY"] += 1
    return character

def BLightDamage_fun(character):
    if "Light Damage" in character[1]:
        character[1]["Light Damage"] += 1
    else:
        character[1].update({"Light Damage": 1})
    character[0]["BODY"] += 1
    return character

def BRangedDamage_fun(character):
    if "Ranged Damage" in character[1]:
        character[1]["Ranged Damage"] += 1
    else:
        character[1].update({"Ranged Damage": 1})
    character[0]["BODY"] += 1
    return character

def BThrownDamage_fun(character):
    if "Thrown Damage" in character[1]:
        character[1]["Thrown Damage"] += 1
    else:
        character[1].update({"Thrown Damage": 1})
    character[0]["BODY"] += 1
    return character

def BSlashingDamage_fun(character):
    if "Slashing Damage" in character[1]:
        character[1]["Slashing Damage"] += 1
    else:
        character[1].update({"Slashing Damage": 1})
    character[0]["BODY"] += 1
    return character

def BPiercingDamage_fun(character):
    if "Piercing Damage" in character[1]:
        character[1]["Piercing Damage"] += 1
    else:
        character[1].update({"Piercing Damage": 1})
    character[0]["BODY"] += 1
    return character

def BBludgeoningDamage_fun(character):
    if "Bludgeoning Damage" in character[1]:
        character[1]["Bludgeoning Damage"] += 1
    else:
        character[1].update({"Bludgeoning Damage": 1})
    character[0]["BODY"] += 1
    return character

def BUnarmedPrecision_fun(character):
    if "Unarmed Precision" in character[1]:
        character[1]["Unarmed Precision"] += 1
    else:
        character[1].update({"Unarmed Precision": 1})
    character[0]["BODY"] += 1
    return character

def BUnarmedDamage_fun(character):
    if "Unarmed Damage" in character[1]:
        character[1]["Unarmed Damage"] += 1
    else:
        character[1].update({"Unarmed Damage": 1})
    character[0]["BODY"] += 1
    return character