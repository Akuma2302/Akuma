# *********************************************************
# Program: main.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL7L
# Year: 2023/24 Trimester 1
# Names: AHMAD AKMAL ASYRAAF BIN SHAMSUL AZHAR | MUHAMMAD AISH QAYYIM BIN MOHD AZMI | MUHAMMAD ALTAF BIN HAMID
# IDs: 1221109308 | 1221109286 | 1221109019
# Emails: 1221109308@student.mmu.edu.my | 1221109286@student.mmu.edu.my | 1221109019@student.mmu.edu.my
# Phones: +60 17-250 7341 | +60 12-342 5662 | +60 13-650 2857
# *********************************************************

import os
import random
import pygame
from pygame import mixer  #https://www.youtube.com/watch?v=LspPtqm3RDI (1:23)
import pathlib
from pathlib import Path

#Get the Current directory where the script is located
current_directory = Path(__file__).resolve().parent

pygame.mixer.init()
main_song = current_directory / "theme.mp3"   #Background Sound
click_sound_effect = pygame.mixer.Sound(str(current_directory / "click.mp3"))    #Input and Click Sound: https://www.youtube.com/watch?v=LspPtqm3RDI (1:51)

pygame.mixer.music.load(main_song)   #Load music file for playback: https://www.pygame.org/docs/ref/music.html
pygame.mixer.music.play(-1)   #https://www.youtube.com/watch?v=LspPtqm3RDI (5:32)

run = True         #https://www.youtube.com/watch?v=iMS75wmppew (1:01)
menu = True
play = False
tutorial = False
standing = True
inven = False
shop = False
s_shop = False
speak = False
boss = False
key = False

#Weapon Attribute
weapon = {
    "Fist":{
        "at" : 0,
        "go" : 0
    },
    "Wooden Sword":{
        "at" : 2,
        "go" : 15
    },
    "Stone Sword":{
        "at" : 5,
        "go" : 40
    },
    "Iron Sword":{
        "at" : 10,
        "go" : 80
    },
    "Obsidian Sword":{
        "at" : 20,
        "go" : 120
    },
    "Diamond Sword":{
        "at" : 40,
        "go" : 160
    }
    }

#Armor Attribute
armor = {
    "None":{
        "hp" : 0,
        "def" : 0,
        "go" : 0
    },
    "Leather Armor":{
        "hp" : 3,
        "def" : 1,
        "go" : 15
    },
    "Bronze Armor":{
        "hp"  : 10,
        "def" : 5,
        "go"  : 40
    },
    "Steel Armor":{
        "hp"  : 20,
        "def" : 10,
        "go"  : 80
    },
    "Platinum Armor":{
        "hp"  : 35,
        "def" : 16,
        "go"  : 120
    },
    "Titanium Armor":{
        "hp"  : 50,
        "def" : 25,
        "go"  : 160
    }
}

#Player Stats: https://www.youtube.com/watch?v=i3j3iZNPUbI&t=35s (0:37)
in_weapon = ['Fist']
in_armor = ['None']
use_weapon = 'Fist'
use_armor = 'None'
BASE_HP = 50
HP = BASE_HP + armor[use_armor]["hp"]
HPMAX = HP
BASE_ATK = 2
ATK = BASE_ATK + weapon[use_weapon]["at"]
BASE_DEF = 0
DEF = BASE_DEF + armor[use_armor]["def"]
EXP = 0
LVL = 1
s_pot = 1
b_pot = 0
elix = 0
gold = 0
x = 0
y = 0
open_story = True

#map https://www.youtube.com/watch?v=i3j3iZNPUbI&t=35s(2:26)
map = [# x = 0      x = 1      x = 2      x = 3      x = 4        x = 5        x = 6    x = 7      x = 8      x = 9     x = 10     x = 11     x = 12      x = 13      x = 14      x = 15      x = 16      x = 17       x = 18          x = 19          x = 20      x = 21      x = 22     x = 23
    ["forest",  "forest",  "forest",  "forest",  "forest",     "hills",     "hills",  "wall",  "forest",  "forest",  "forest",  "forest",    "shop",    "hills", "mountain",     "wall",  "dungeon",  "hallway",   "hallway",  "cursed room",  "cursed room",     "lair",     "lair",    "wall"],  # y = 0
    ["forest",  "fields",  "bridge",  "plains",   "hills",    "forest",     "hills",  "wall",  "forest",  "fields",    "town",    "town",   "trees",    "hills",    "hills",     "wall",  "dungeon",  "hallway",   "hallway",  "throne room",  "throne room",     "lair",     "lair",    "wall"],  # y = 1              
    ["plains",    "shop",    "town",    "town",  "plains",     "hills",  "mountain",  "wall",  "plains",   "trees",    "town",  "plains",  "plains",    "trees",    "hills",     "wall",   "plains",  "chamber",      "town",       "castle",          "lab",      "lab",  "library",    "wall"],  # y = 2
    ["plains",  "fields",  "fields",  "plains",   "hills",  "mountain",  "mountain",  "door",    "shop",  "fields",    "town",  "plains",   "hills",    "trees",   "forest", "fortress",     "shop",  "chamber",      "town",       "plains",          "lab",  "library",  "library",   "tower"],  # y = 3          
    ["plains",  "fields",  "fields",  "plains",   "hills",  "mountain",  "mountain",  "wall",  "plains",   "trees",  "fields",   "river",   "river",   "plains",   "forest",     "wall",   "plains",  "chamber",  "corridor",     "corridor",  "cursed room",  "library",  "library",    "wall"],  # y = 4          
    ["forest",  "forest",  "forest",  "forest",  "forest",     "hills",    "forest",  "wall",  "plains",   "trees",  "fields",   "river",   "river",   "plains",   "forest",     "wall",   "plains",  "chamber",    "fields",       "plains",  "cursed room",    "vault",   "prison",    "wall"],  # y = 5
    ["forest",  "fields",  "bridge",  "plains",    "shop",    "forest",     "hills",  "wall",  "plains",   "trees",   "river",  "bridge",  "bridge",   "plains",   "forest",     "wall",   "forest",   "forest",    "fields",       "plains",         "lair",    "vault",   "prison",    "wall"]   # y = 6
       ] 

y_len = len(map)-1
x_len = len(map[0])-1

#Location Information: https://www.youtube.com/watch?v=i3j3iZNPUbI&t=35s (3:57)
biom = {
    "plains":{
        "t": "PLAINS",
        "e": True},
    "forest":{
        "t": "WOODS",
        "e": True},
    "fields":{
        "t": "FIELDS",
        "e": False},
    "bridge":{
        "t": "BRIDGE",
        "e": True},
    "hills":{
        "t":"HILLS",
        "e":True},
    "town":{
        "t": "TOWN CENTRE",
        "e": False},
    "shop":{
        't': "SHOP",
        "e": False},
    "castle":{
        "t": "CASTLE",
        "e": False},
    "tower":{
        "t": "TOWER",
        "e": False},
    "corridor":{
        "t": "CORRIDOR",
        "e": False},
    "mountain":{
        "t": "MOUNTAIN",
        "e": True},
    "dungeon":{
        "t": "DUNGEON",
        "e": True},  
     "prison":{
        "t": "PRISON",
        "e": True},  
    "trees":{
        "t": "TREES",
        "e": True}, 
    "river":{
        "t": "RIVER",
        "e": False},
    "fortress":{
        "t": "FORTRESS",
        "e": False},
    "door":{
        "t": "DOOR",
        "e": False},
    "wall":{
        "t": "WALL",
        "e": False},
    "throne room":{
        "t": "THRONE ROOM",
        "e": True},
    "cursed room":{
        "t": "CURSED ROOM",
        "e": True},
    "lab":{
        "t": "LAB",
        "e": True},
    "library":{
        "t": "LIBRARY",
        "e": False},
    "chamber":{
        "t": "CHAMBER",
        "e": False},
    "vault":{
        "t": "VAULT",
        "e": True},
    "lair":{
        "t": "LAIR",
        "e": True},
    "hallway":{
        "t": "HALLWAY",
        "e": False}
    }


#Enemy List and Stat: https://www.youtube.com/watch?v=0PMF36-00ag (0:30)

e_list_1 = ["Goblin", "Orc", "Slime"]
e_list_2 = ["Goblin", "Orc", "Slime", "Spider", "Zombie", "Skeleton", "Wolf"]
e_list_3 = ["Spider", "Zombie", "Skeleton", "Wolf", "Bat", "Golem", "Thug"]

mobs = {
    "Goblin":{
        "hp": 15,
        "at": 2,
        "go": 3,
        "ex": 5
    },
    "Orc":{
        "hp": 20,
        "at": 4,
        "go": 5,
        "ex": 10
    },
    "Slime":{
        "hp": 30,
        "at": 2,
        "go": 12,
        "ex": 6
    },
    "Spider":{
        "hp": 70,
        "at": 26,
        "go": 9,
        "ex": 15
    },
    "Zombie":{
        "hp": 100,
        "at": 40,
        "go": 15,
        "ex": 20
    },
    "Skeleton":{
        "hp": 50,
        "at": 26,
        "go": 15,
        "ex": 15
    },
    "Wolf":{
        "hp": 80,
        "at": 50,
        "go": 8,
        "ex": 15
    },
    "Bat":{
        "hp": 20,
        "at": 3,
        "go": 20,
        "ex": 5
    },
    "Golem":{
        "hp": 160,
        "at": 65,
        "go": 25,
        "ex": 40
    },
    "Thug":{
        "hp": 200,
        "at": 50,
        "go": 25,
        "ex": 30
    },
    "Sorcerer":{
        "hp": 400,
        "at": 75,
        "go": 100,
        "ex": 100
    }
}

#Clear previous output: https://www.youtube.com/watch?v=iMS75wmppew (5:56)
def clear():
    os.system("cls")

#Saving Data: https://www.youtube.com/watch?v=iMS75wmppew (3:18)
def save():
    list = [
        name,
        str(BASE_HP),
        str(HP),
        str(BASE_ATK),
        str(ATK),
        str(BASE_DEF),
        str(DEF),
        str(EXP),
        str(LVL),
        str(s_pot),
        str(b_pot),
        str(elix),
        str(gold),
        str(x),
        str(y),
        str(in_weapon),
        str(in_armor),
        str(use_weapon),
        str(use_armor),
        str(open_story)
    ]

    f = open("load.txt", "w")

    for item in list:
        f.write(item + "\n")
    f.close()

#Drawing lines: https://www.youtube.com/watch?v=iMS75wmppew (6:26)
def draw():
    print("Xx--------------------------------------Xx")    

#Health Point Recover: https://www.youtube.com/watch?v=0PMF36-00ag (5:13)
def heal(amount):
    global HP
    if HP + amount < HPMAX:
        HP += amount
    else:
        HP = HPMAX
    print(name + "'s HP refilled to " + str(HP) + "!")
    
#Level Up
def levelup(amount):
    global EXP, LVL, BASE_ATK, BASE_HP, BASE_DEF, HP, HPMAX, ATK, DEF 
    EXP += amount
    if LVL >= 1 and LVL <= 5:
        if EXP >= 50:
            LVL += 1
            EXP -= 50
            BASE_ATK += 1
            BASE_HP += 5
            BASE_DEF += 1
            HP = BASE_HP + armor[use_armor]["hp"]
            HPMAX = HP
            ATK = BASE_ATK + weapon[use_weapon]["at"]
            DEF = BASE_DEF + armor[use_armor]["def"]
            print(f"Congratualtion, You reached level {LVL}")
            print("Your health is recover")
            input("> ")
            click_sound_effect.play()
    elif LVL >= 6 and LVL <= 10:
        if EXP >= 80:
            HP = HPMAX
            LVL += 1
            EXP -= 80
            BASE_ATK += 1
            BASE_HP += 5
            BASE_DEF += 1
            HP = BASE_HP + armor[use_armor]["hp"]
            HPMAX = HP
            ATK = BASE_ATK + weapon[use_weapon]["at"]
            DEF = BASE_DEF + armor[use_armor]["def"]
            print(f"Congratualtion, You reached level {LVL}")
            print("Your health is recover")
            input("> ")
            click_sound_effect.play()
    elif LVL >= 11:
        if EXP >= 100:
            HP = HPMAX
            LVL += 1
            EXP -= 100
            BASE_ATK += 1
            BASE_HP += 5
            BASE_DEF += 1
            HP = BASE_HP + armor[use_armor]["hp"]
            HPMAX = HP
            ATK = BASE_ATK + weapon[use_weapon]["at"]
            DEF = BASE_DEF + armor[use_armor]["def"]
            print(f"Congratualtion, You reached level {LVL}")
            print("Your health is recover")
            input("> ")
            click_sound_effect.play()

#Battle with enemy: https://www.youtube.com/watch?v=0PMF36-00ag (2:24)
def battle():
    global fight, play, run, HP, s_pot, b_pot, elix, gold, boss, EXP, LVL, x
    draw()
    # Determine if it is Boss or not: https://www.youtube.com/watch?v=wnizccXysKE&t=2s (3:20)
    if not boss:
        if x >= 16:
            enemy = random.choice(e_list_3)
        elif x >= 8 and x < 16:
            enemy = random.choice(e_list_2)
        elif x < 8:
            enemy = random.choice(e_list_1)
    else:
        enemy = "Sorcerer"
    hp = mobs[enemy]["hp"]
    hpmax = hp
    atk = mobs[enemy]["at"]
    g = mobs[enemy]["go"]
    e = mobs[enemy]["ex"]
    draw()
    while fight:
        atk = mobs[enemy]["at"]
        clear()
        draw()
        print("            Defeat the " + enemy + "!")
        draw()
        print(enemy + "'s HP: " + str(hp) + "/" + str(hpmax))
        print(enemy + "'s ATK: " + str(atk))
        print(name + "'s HP: " + str(HP) + "/" + str(HPMAX))
        print(name + "'s ATK: " + str(ATK))
        print(name + "'s DEF: " + str(DEF))
        print("SMALL POTIONS: " + str(s_pot))
        print("BIG POTIONS: " + str(b_pot))
        print("ELIXER: " + str(elix))
        draw()

        print("1 - ATTACK")
        if s_pot > 0:
            print("2 - USE SMALL POTION (30HP)")
        if b_pot > 0:
            print("3 - USE SMALL POTION (50HP)")
        if elix > 0:
            print("4 - USE ELIXIR (70HP)")
        draw()
        
        choice = input("# ")
        if choice == "1":
            hp -= ATK
            print(name + " dealt " + str(ATK) + " damage to the " + enemy + ".")
            if hp > 0:
                if atk > DEF:
                    atk -= DEF
                    HP -= atk
                    print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    HP -= 1
                    print(enemy + " dealt " + str(1) + " damage to " + name + ".")
        elif choice == "2":
            if s_pot > 0:
                s_pot -= 1
                heal(30)
                if atk > DEF:
                    atk -= DEF
                    HP -= atk
                    print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    HP -= 1
                    print(enemy + " dealt " + str(1) + " damage to " + name + ".")
            else:
                print("You don't have any potions.")
        elif choice == "3":
            if b_pot > 0:
                b_pot -= 1
                heal(50)
                if atk > DEF:
                    atk -= DEF
                    HP -= atk
                    print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    HP -= 1
                    print(enemy + " dealt " + str(1) + " damage to " + name + ".")
            else:
                print("You don't have any potions.")        
        elif choice == "4":
            if elix > 0:
                elix -= 1
                heal(70)
                if atk > DEF:
                    atk -= DEF
                    HP -= atk
                    print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
                else:
                    HP -= 1
                    print(enemy + " dealt " + str(1) + " damage to " + name + ".")
            else:
                print("You don't have an Elixir.")
        input("> ")
        if HP <= 0 :
            print(enemy + " defeated " + name + "...")
            fight = False
            play = False
            run = False
            boss = False
            print("GAME OVER")
            input("> ")
            
        if hp <= 0:
            print(name + " defeated the " + enemy + "!")
            
            fight = False
            gold += g
            print("You've found " + str(g) + " gold!")
            input("> ")
            click_sound_effect.play()
            levelup(e)
            if random.randint(0,100) < 30:
                s_pot += 1
                print("You've found a small potion!")
                input("> ")
                click_sound_effect.play()
            if enemy == "Sorcerer":
                clear()
                print("After the sorcerer has been defeated, Sir " + name + " freed the princess from the cell.")
                input("> ")
                click_sound_effect.play()
                print("Princess Isabella: Thank you for saving me.")
                input("> ")
                click_sound_effect.play()
                print("Sir " + name + ": You're welcome princess. Now come let's take you back to the castle.")
                input("> ")
                click_sound_effect.play()
                print("As the two ride back to the castle, the local town celebrated they're return cheering and singing for them.")
                input("> ")
                click_sound_effect.play()
                print("King Wade who was standing outside of the castle embraced his daughter with joy and relief.")
                input("> ")
                click_sound_effect.play()
                print("He thanked Sir " + name + " for his service and awarded him the highest honor bestow by the king.")
                input("> ")
                click_sound_effect.play()
                print("Words spread across the kingdom of Sir " + name + " glorious victory as well as his will live on for generations to come.")
                input("> ")
                click_sound_effect.play()
                clear()
                draw()
                print("       THANK YOU FOR PLAYING! :)")
                draw()
                save()
                input("> ")
                boss = False
                play = False
                run = False

#Shop: https://www.youtube.com/watch?v=wnizccXysKE&t=2s (1:01)
def shopping():
    global shop, gold, s_pot, b_pot, elix, LVL, in_weapon, in_armor, use_weapon, use_armor, ATK, HPMAX, DEF, BASE_ATK, BASE_HP, BASE_DEF, HP
    buy = False
    sell = False
    select = False
    while shop:
        clear()
        draw()
        print("           WELCOME TO THE SHOP")
        draw()
        print("                GOLD: " + str(gold))
        draw()
        print("1 - BUY")
        print("2 - SELL")
        print("3 - LEAVE")
        draw()
        
        choice = input("# ")
        
        if choice == "1":
            click_sound_effect.play()
            buy = True
            while buy:
                clear()
                draw()
                print("                BUY ITEM")
                draw()
                print("                GOLD: " + str(gold))
                draw()
                print("1 - POTION")
                print("2 - WEAPON")
                print("3 - ARMOR")
                print("4 - BACK")
                draw()
                choice = input("# ")
                if choice == "1":
                    click_sound_effect.play()
                    select = True
                    while select:
                        clear()
                        draw()
                        print("               BUY POTION")
                        draw()
                        print("               GOLD: " + str(gold))
                        draw()
                        print("0 - BACK")
                        print("1 - SMALL POTION (30HP) - 5 GOLD")
                        if LVL >= 5:
                            print("2 - BIG POTION (50HP) - 30 GOLD")
                        if LVL >= 10:
                            print("3 - ELIXER POTION (70HP) - 70 GOLD")
                        draw()
                        choice = input("# ")
                        click_sound_effect.play()
                        if choice == "1":
                            if gold >= 5:
                                gold -= 5
                                s_pot += 1
                                print(f"You had buy a small potion for 5 golds")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            click_sound_effect.play()
                        elif choice == "2" and LVL >= 5:
                            if gold >= 30:
                                gold -= 30
                                b_pot += 1
                                print(f"You had buy a big potion for 30 golds")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            click_sound_effect.play()
                        elif choice == "3" and LVL >= 10:
                            if gold >= 70:
                                gold -= 70
                                elix += 1
                                print(f"You had buy an elixer for 70 golds")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            click_sound_effect.play()
                        elif choice == "0":
                            select = False
                            
                elif choice == "2":
                    click_sound_effect.play()
                    select = True
                    while select:
                        clear()
                        draw()
                        print("               BUY WEAPON")
                        draw()
                        print("               GOLD: " + str(gold))
                        draw()
                        print("0 - BACK")
                        print("1 - WOODEN SWORD (2ATK) - 15 GOLD")
                        if LVL >= 3:
                            print("2 - STONE SWORD (6ATK) - 40 GOLD")
                        if LVL >= 5:
                            print("3 - IRON SWORD (10ATK) - 80 GOLD")
                        if LVL >= 8: 
                            print("4 - OBSIDIAN SWORD (20ATK) - 120 GOLD")
                        if LVL >= 12:
                            print("5 - DIAMOND SWORD (40ATK) - 160 GOLD")    
                        draw()
                        choice = input("# ")
                        if choice == "1":
                            click_sound_effect.play()
                            if gold >= 15:
                                gold -= 15
                                in_weapon.append("Wooden Sword")
                                print("You had buy a Wooden Sword")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                                
                        elif choice == "2" and LVL >= 3:
                            click_sound_effect.play()
                            if gold >= 40:
                                gold -= 40
                                in_weapon.append("Stone Sword")
                                print("You had buy Stone Sword")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                                
                        elif choice == "3" and LVL >= 5:
                            click_sound_effect.play()
                            if gold >= 80:
                                gold -= 80
                                in_weapon.append("Iron Sword")
                                print("You had buy Iron Sword")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                                
                        elif choice == "4" and LVL >= 8:
                            click_sound_effect.play()
                            if gold >= 120:
                                gold -= 120
                                in_weapon.append("Obsidian Sword")
                                print("You had buy Obsidian Sword")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                                
                        elif choice == "5" and LVL >= 12:
                            click_sound_effect.play()
                            if gold >= 160:
                                gold -= 160
                                in_weapon.append("Diamond Sword")
                                print("You had buy Diamond Sword")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            
                        elif choice == "0":
                            click_sound_effect.play()
                            select = False  
                                    
                elif choice == "3":
                    click_sound_effect.play()
                    select = True
                    while select:
                        clear()
                        draw()
                        print("                 BUY ARMOR")
                        draw()
                        print("                 GOLD: " + str(gold))
                        draw()
                        print("0 - BACK")
                        print("1 - LEATHER (3HP,1DEF) - 15 GOLD")
                        if LVL >= 3:
                            print("2 - BRONZE (10HP,5DEF) - 40 GOLD")
                        if LVL >= 5:
                            print("3 - STEEL (20HP,10DEF) - 80 GOLD")
                        if LVL >= 8:
                            print("4 - PLANTINUM (35HP,16DEF) - 120 GOLD")
                        if LVL >= 12:
                            print("5 - TITANIUM (50HP,25DEF) - 160 GOLD")
                        draw()
                        choice = input("# ")
                        if choice == "1":
                            click_sound_effect.play()
                            if gold >= 15:
                                gold -= 15
                                in_armor.append("Leather Armor")
                                print("You had buy a Leather Armor")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            click_sound_effect.play()
                                
                        elif choice == "2" and LVL >= 3:
                            click_sound_effect.play()
                            if gold >= 40:
                                gold -= 40
                                in_armor.append("Bronze Armor")
                                print("You had buy Bronze Armor")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            click_sound_effect.play()
                                
                        elif choice == "3" and LVL >= 5:
                            click_sound_effect.play()
                            if gold >= 80:
                                gold -= 80
                                in_armor.append("Steel Armor")
                                print("You had buy Steel Armor")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            click_sound_effect.play()
                                
                        elif choice == "4" and LVL >= 8:
                            click_sound_effect.play()
                            if gold >= 120:
                                gold -= 120
                                in_armor.append("Platinum Armor")
                                print("You had buy Platinum Armor")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            click_sound_effect.play()
                                
                        elif choice == "5" and LVL >= 12:
                            click_sound_effect.play()
                            if gold >= 160:
                                gold -= 160
                                in_armor.append("Titanium Armor")
                                print("You had buy Titanium Armor")
                            else:
                                print("Not enough GOLDS!")
                            input("> ")
                            click_sound_effect.play()
                            
                        elif choice =="0":
                            click_sound_effect.play()
                            select = False  

                elif choice =="4":
                    click_sound_effect.play()
                    buy = False
        elif choice == "2":
            click_sound_effect.play()
            sell = True
            while sell:
                clear()
                draw()
                print("                SELL ITEM")
                draw()
                print("                GOLD: " + str(gold))
                draw()
                print("1 - WEAPON")
                print("2 - ARMOR")
                print("3 - BACK")
                draw()
                choice = input("# ")
                if choice == "1":
                    click_sound_effect.play()
                    select = True
                    while select:
                        clear()
                        draw()
                        print("               SELL WEAPON")
                        draw()
                        print("               GOLD: " + str(gold))
                        draw()
                        i = 0
                        print("0 - BACK")
                        for j in range(len(in_weapon)):
                            i += 1
                            at = weapon[in_weapon[j]]['at']
                            print(str(i) + " - " + in_weapon[j].upper() + " (" + str(at) + "ATK)")
                        draw()
                        sell_weapon = int(input("Sell weapon: "))
                        if sell_weapon == 0:
                            click_sound_effect.play()
                            select = False
                        else:
                            sell_weapon = in_weapon[sell_weapon - 1]
                            click_sound_effect.play()
                            if sell_weapon == "Fist":
                                clear()
                                draw()
                                print("You can't sell your Fist")
                                draw()
                                input("> ")
                                click_sound_effect.play()
                            else:
                                draw()
                                print("Are you sure? y/n")
                                confirm = input("> ")
                                if confirm == "y":
                                    click_sound_effect.play()
                                    clear()
                                    in_weapon.remove(sell_weapon)
                                    sell_gold = weapon[sell_weapon]["go"]
                                    gold += sell_gold
                                    draw()
                                    print("You sold "+ sell_weapon + " for " + str(sell_gold))
                                    draw()
                                    input("> ")
                                    click_sound_effect.play()
                                    if sell_weapon == use_weapon:
                                        use_weapon = "Fist"
                                        ATK = BASE_ATK + weapon[use_weapon]["at"]
                                        print("You're now using Fist")
                                        input("> ")
                                        click_sound_effect.play()
                                elif confirm == "n":
                                    continue
                            
                elif choice == "2":
                    select = True
                    while select:
                        click_sound_effect.play()
                        clear()
                        draw()
                        print("               SELL ARMOR")
                        draw()
                        print("               GOLD: " + str(gold))
                        draw()
                        i = 0
                        print("0 - BACK")
                        for j in range(len(in_armor)):
                            i += 1
                            de = armor[in_armor[j]]['def']
                            h = armor[in_armor[j]]["hp"]
                            print(str(i) + " - " + in_armor[j].upper() + " (" + str(h) + "HP, " + str(de) + "DEF)")
                        draw()
                        sell_armor = int(input("Sell weapon: "))
                        if sell_armor == 0:
                            click_sound_effect.play()
                            select = False
                        else:
                            sell_armor = in_armor[sell_armor - 1]
                            click_sound_effect.play()
                            if sell_armor == "None":
                                clear()
                                draw()
                                print("You can't sell your None")
                                draw()
                                input("> ")
                                click_sound_effect.play()
                            else:
                                draw()
                                print("Are you sure? y/n")
                                confirm = input("> ")
                                click_sound_effect.play()
                                if confirm == "y":
                                    clear()
                                    in_armor.remove(sell_armor)
                                    sell_gold = armor[sell_armor]["go"]
                                    gold += sell_gold
                                    draw()
                                    print("You sold " + sell_armor + " for " + str(sell_gold))
                                    draw()
                                    input("> ")
                                    click_sound_effect.play()
                                    if sell_armor == use_armor:
                                        use_armor = "None"
                                        DEF = BASE_DEF + armor[use_armor]["def"]
                                        HPMAX = BASE_HP + armor[use_armor]["hp"]
                                        if HP > HPMAX:
                                            HP = HPMAX
                                        print("You're now have no armor")
                                        input("> ")
                                        click_sound_effect.play()
                                elif confirm == "n":
                                    continue
                elif choice == "3":
                    click_sound_effect.play()
                    sell = False              
        elif choice == "3":
            click_sound_effect.play()
            shop = False 


def inventory():    #Player inventory
    global inven, in_weapon, in_armor, use_weapon, use_armor, ATK, BASE_ATK, weapon, armor, HP, HPMAX, BASE_HP, DEF, BASE_DEF, x, y
    weapon_select = False
    armor_select = False
    maps = False
    swap = False
    while inven:    #Option What To Look In Inventory
        clear()
        draw()    
        print("                INVENTORY")
        draw()
        print("1 - WEAPON")
        print("2 - ARMOR")
        print("3 - MAP")
        print("4 - BACK")
        draw()
        choice = input("# ")
        if choice == "1":
            click_sound_effect.play()
            weapon_select = True
            while weapon_select:
                clear()
                draw()
                print("    Current use weapon: " + use_weapon)
                draw()
                print("1 - SWAP")
                print("2 - BACK")
                draw()
                choice = input("# ")
                if choice == "1":    #Change Weapon Option
                    click_sound_effect.play()
                    swap = True
                    while swap:
                        clear()
                        draw()
                        print("    Current use weapon: " + use_weapon)
                        draw()
                        i = 0
                        print("0 - BACK")
                        for j in range(len(in_weapon)):
                            i += 1
                            at = weapon[in_weapon[j]]['at']
                            print(str(i) + " - " + in_weapon[j].upper() + " (" + str(at) +"ATK)")
                        draw()
                        swap_weapon = int(input("Swap weapon: "))
                        click_sound_effect.play()
                        if swap_weapon == 0:
                            swap = False
                        else:
                            use_weapon = in_weapon[swap_weapon - 1]
                            ATK = BASE_ATK + weapon[use_weapon]["at"]
                            draw()
                            print("Now you are using " + use_weapon)
                            draw()
                            input("> ")
                            click_sound_effect.play()

                elif choice == "2":
                    click_sound_effect.play()
                    weapon_select = False
                         
        elif choice == "2":
            click_sound_effect.play()
            armor_select = True
            while armor_select:
                clear()
                draw()
                print("    Current use armor: " + use_armor)
                draw()
                print("1 - SWAP")
                print("2 - BACK")
                draw()
                choice = input("# ")
                if choice == "1":    #Change Armor Option
                    click_sound_effect.play()
                    swap = True
                    while swap:
                        clear()
                        draw()
                        print("    Current use armor: " + use_armor)
                        draw()
                        i = 0
                        print("0 - BACK")
                        for j in range(len(in_armor)):
                            i += 1
                            de = armor[in_armor[j]]['def']
                            h = armor[in_armor[j]]["hp"]
                            print(str(i) + " - " + in_armor[j].upper() + " (" + str(h) +"HP, " + str(de) +"DEF)")
                        draw()
                        swap_armor = int(input("Swap armor: "))
                        click_sound_effect.play()
                        if swap_armor == 0:
                            swap = False
                        else:
                            use_armor = in_armor[swap_armor - 1]
                            DEF = BASE_DEF + armor[use_armor]["def"]
                            HPMAX = BASE_HP + armor[use_armor]["hp"]
                            if HP > HPMAX:
                                HP = HPMAX
                            draw()
                            print("Now you are using " + use_armor)
                            draw()
                            input("> ")
                            click_sound_effect.play()

                elif choice == "2":
                    click_sound_effect.play()
                    armor_select = False
        elif choice == "3":
            click_sound_effect.play()
            maps = True
            while maps:
                clear()
                print("Xx------------------------------------------------------------------------------------------------Xx")
                print("                                      LOCATION: " + biom[map[y][x]]["t"])
                print("                                   COORDINATE: " + "x: " +  str(x) + " y: " + str(y))
                print("Xx------------------------------------------------------------------------------------------------Xx")
                if x <= 7:
                    print("           x = 0    x = 1    x = 2    x = 3    x = 4    x = 5      x = 6    x = 7")
                    print("          forest   forest   forest   forest   forest      hills      hills   wall   y = 0")
                    print("          forest   fields   bridge   plains    hills     forest      hills   wall   y = 1")              
                    print("          plains     shop     town     town   plains      hills   mountain   wall   y = 2")           
                    print("          plains   fields   fields   plains    hills   mountain   mountain   door   y = 3")          
                    print("          plains   fields   fields   plains    hills   mountain   mountain   wall   y = 4")          
                    print("          forest   forest   forest   forest   forest      hills     forest   wall   y = 5")
                    print("          forest   fields   bridge   plains     shop     forest      hills   wall   y = 6")
                elif x > 7 and x <= 15:
                    print("          x = 8    x = 9   x = 10   x = 11   x = 12    x = 13    x = 14     x = 15")
                    print("         forest   forest   forest   forest     shop     hills   mountain     wall     y = 0")
                    print("         forest   fields     town     town    trees     hills      hills     wall     y = 1")
                    print("         plains    trees     town   plains   plains     trees      hills     wall     y = 2")
                    print("           shop   fields     town   plains    hills     trees     forest   fortress   y = 3")      
                    print("         plains    trees   fields    river    river    plains     forest     wall     y = 4")          
                    print("         plains    trees   fields    river    river    plains     forest     wall     y = 5")
                    print("         plains    trees    river   bridge   bridge    plains     forest     wall     y = 6")
                elif x > 15:
                    print("     x = 16    x = 17     x = 18     x = 19         x = 20      x = 21    x = 22   x = 23")
                    print("    dungeon   hallway    hallway   cursed room   cursed room      lair      lair    wall   y = 0")
                    print("    dungeon   hallway    hallway   throne room   throne room      lair      lair    wall   y = 1")
                    print("     plains   chamber       town        castle           lab       lab   library    wall   y = 2")
                    print("       shop   chamber       town        plains           lab   library   library   tower   y = 3")
                    print("     plains   chamber   corridor      corridor   cursed room   library   library    wall   y = 4")
                    print("     plains   chamber     fields        plains   cursed room     vault    prison    wall   y = 5")
                    print("     forest    forest     fields        plains          lair     vault    prison    wall   y = 6")
                print("Xx------------------------------------------------------------------------------------------------Xx")
                print("  BACK")
                input("> ")
                click_sound_effect.play()
                maps = False
        elif choice == "4":
            click_sound_effect.play()
            inven = False

#Story: Opening
def opening():
    clear()
    global open_story
    while open_story:
        print("Once upon a time, in the kingdom of Silvercrest, there lived King Wade and his daughter Princess Isabella who lived happily.")
        input("> ")
        click_sound_effect.play()
        print("There is also lived a knight by the name of Sir " + name + " renowned for his bravery and unwavering sense of honor.")
        input("> ")
        click_sound_effect.play()
        print("One fateful day, the kingdom was thrown into turmoil when the malevolent sorcerer, Zephyrus, abducted Princess Isabella and imprisoned her in his tower, shrouded in darkness and guarded by sinister creatures.")
        input("> ")
        click_sound_effect.play()
        print("King Wade ask for Sir " + name + " help to rescue the princess from the sorcerer.")            
        input("> ")
        click_sound_effect.play()
        print("Determined to rescue the princess and restore peace to the kingdom, Sir " + name + " embarked on a daunting and perilous quest.")
        input("> ")
        click_sound_effect.play()
        print("Clad in gleaming armor and wielding his mighty sword, he journeyed across treacherous landscapes to save the princess.")
        input("> ")
        click_sound_effect.play()
        open_story = False
    
#Place To Get A Key For Boss Fight: https://www.youtube.com/watch?v=wnizccXysKE&t=2s (2:06)
def castle():
    global speak, key
    while speak:
        clear()
        print("King Wade: Greetings, Sir " + name + "!")
        input("> ")
        click_sound_effect.play()
        if LVL < 13:
            print("King Wade: You're not strong enough to face Zephyrus yet! Keep practicing and come back later")
            input("> ")
            print("You need to reach level 14 to get a key")
            input("> ")
            click_sound_effect.play()
            key = False
        else:
            print("King Wade: You might want to take on Zephyrus now!")
            input("> ")
            click_sound_effect.play()
            print("King Wade: Take this key. My men have found it on one of his creatures.")
            input("> ")
            click_sound_effect.play()
            key = True

        print("  Back")
        input("> ")
        click_sound_effect.play()
        speak = False

#Boss Domain: https://www.youtube.com/watch?v=wnizccXysKE&t=2s (2:44)
def tower():
    global boss, key, fight, x
    
    while boss:
        clear()
        print("King Wade: Here lies Zephyrus's tower. What will you do now?")
        input("> ")
        click_sound_effect.play()
        clear()
        draw()
        if key:
            print("1 - USE KEY")
        print("2 - TURN BACK")
        draw()
        
        choice = input("# ")
        click_sound_effect.play()
        if choice == "1":
            if key:
                fight = True
                clear()
                print("King Wade: Be careful, local said that he is one of the most powerful sorcerer in the kingdom.")
                input("> ")
                click_sound_effect.play()
                print("As Sir " + name + " makes his way into the tower, he encountered the sorcerer with the princess being encaptured in his cell.")
                input("> ")
                click_sound_effect.play()
                print("Sir " + name + ": Hold it right there, Sorcerer.")
                input("> ")
                click_sound_effect.play()
                print("Zephyrus: So, you must be the brave knight this kingdom has been raving about.")
                input("> ")
                click_sound_effect.play()
                print("Zephyrus: No matter what you do, you will never defeat me.")
                input("> ")
                click_sound_effect.play()
                battle()
        elif choice == "2":
            x -= 1
            boss = False


def lock():
    global x, LVL
    if x == 7:
        if LVL < 5:
            clear()
            print("  Your level are not enough")
            input("> ")
            click_sound_effect.play()
            print("  You can't pass through the door")
            input("> ")
            click_sound_effect.play()
            print("  Need to reach level 5")
            input("> ")
            click_sound_effect.play()
            print("  Back")
            input("> ")
            click_sound_effect.play()
            x -= 1
        else:
            clear()
            x += 1
            print("  You are now in the middle of the forest")
            input("> ")
    
    if x == 15:
        if LVL < 10:
            clear()
            print("  Your level are not enough")
            input("> ")
            click_sound_effect.play()
            print("  You can't pass through the fortress")
            input("> ")
            click_sound_effect.play()
            print("  Need to reach level 10")
            input("> ")
            click_sound_effect.play()
            print("  Back")
            input("> ")
            click_sound_effect.play()
            x -= 1
        else:
            clear()
            x += 1
            print("You are now inside the Sorcerer domain")
            input("> ")

#Tutorial for this game
def tutor():
    global tutorial
    while tutorial:
        draw()
        print("         THIS IS THE MENU SCREEN")
        draw()
        print("1) NEW GAME                   <--- To play New Game")
        print("2) LOAD GAME                  <--- To load your Game")
        print("3) HOW TO PLAY                <--- Tutorial")
        print("4) QUIT GAME                  <--- Quit game")
        draw()
        input("> ")
        click_sound_effect.play()
        clear()
        draw()
        print("         THIS IS IN GAME SCREEN")
        draw()
        print("           LOCATION: BRIDGE   <--- This show your current location")
        draw()
        print("NAME: Akmal                   <--- This is your Name")
        print("HEALTH POINT (HP): 55/55      <--- This is your Health Point")
        print("LEVEL (LVL): 2                <--- This is your Level")
        print("ATTACK POINT (ATK): 5         <--- This is your Attack Point")
        print("SMALL POTIONS: 1              <--- This is your Potion")
        print("BIG POTIONS: 0                <---")
        print("ELIXIRS: 0                    <---")
        print("GOLD: 0                       <--- This is your Gold")
        print("COORDINATE:  2 2              <--- This is your currrent Coordinate")
        draw()
        print("0 - SAVE AND QUIT             <--- Save & Quit Game")
        print("1 - NORTH                     <--- Move Up")
        print("2 - EAST                      <--- Move to the Right")
        print("3 - SOUTH                     <--- Move Down")
        print("4 - WEST                      <--- Move to the Left")
        print("5 - USE SMALL POTION (30HP)   <--- Use Potion to Heal")
        print("6 - USE BIG POTION (50HP)")
        print("7 - USE ELIXIR (70HP)")
        print("8 - INVENTORY                 <--- Check Inventory and Map")
        print("9 - ENTER                     <--- Enter a particular place (Shop)")
        draw()
        print("You need to enter any number from 1 to 4 to move in a specific direction")
        input("> ")
        click_sound_effect.play()
        clear()
        print("For the item sell in the will be update on level 1,3,5,8,12 (For Weapon and Armor) and 1,5,10 (For Potion)")
        input("> ")
        click_sound_effect.play()
        clear()
        print("Embark on a remarkable quest to rescue your one and only princess, abducted by a malevolent force.")
        input("> ")
        click_sound_effect.play()
        print("Your duty is to combat evil, safeguard your kingdom, and reunite with your beloved.")
        input("> ")
        click_sound_effect.play()
        print("Good luck, Sir :)")
        input("> ")
        click_sound_effect.play()
        tutorial = False
        
#Game Running:https://www.youtube.com/watch?v=iMS75wmppew (1:06)
while run:
    # Running Menu
    while menu:
        clear()
        draw()
        print("         WELCOME TO ENIGMA QUEST")
        draw()
        print("1) NEW GAME")
        print("2) LOAD GAME")
        print("3) HOW TO PLAY")
        print("4) QUIT GAME")
        draw()
        choice = input("# ")
        click_sound_effect.play()
        # New Game
        if choice == "1":
            clear()
            name = input("What is your name?\n ")
            print("Welcome " + name + "!")
            input("> ")
            click_sound_effect.play()
            menu = False
            play = True
            opening()
        # Load Game: https://www.youtube.com/watch?v=iMS75wmppew (4:05)
        elif choice == "2":
            try:
                clear()
                f = open("load.txt", "r")
                load_list = f.readlines()
                if len (load_list) == 20:
                    name = load_list[0][:-1]
                    BASE_HP = int(load_list[1][:-1])
                    HP = int(load_list[2][:-1])
                    BASE_ATK = int(load_list[3][:-1])
                    ATK = int(load_list[4][:-1])
                    BASE_DEF = int(load_list[5][:-1])
                    DEF = int(load_list[6][:-1])
                    EXP = int(load_list[7][:-1])
                    LVL = int(load_list[8][:-1])
                    s_pot = int(load_list[9][:-1])
                    b_pot = int(load_list[10][:-1])
                    elix = int(load_list[11][:-1])
                    gold = int(load_list[12][:-1])
                    x = int(load_list[13][:-1])
                    y = int(load_list[14][:-1])
                    in_weapon = load_list[15][:-1]
                    in_armor = load_list[16][:-1]
                    in_weapon = in_weapon.replace("[","")
                    in_weapon = in_weapon.replace("]","")
                    in_weapon = in_weapon.replace("'","")
                    in_weapon = list(in_weapon.split(", "))
                    in_armor = in_armor.replace("[","")
                    in_armor = in_armor.replace("]","")
                    in_armor = in_armor.replace("'","")
                    in_armor = list(in_armor.split(", "))
                    use_weapon = load_list[17][:-1]
                    use_armor = load_list[18][:-1]
                    open_story = load_list[19][:-1]
                    HPMAX = BASE_HP + armor[use_armor]["hp"]
                    clear()
                    print("Welcome back," + name + "!")
                    input("> ")
                    click_sound_effect.play()
                    menu = False
                    play = True
                else:
                    print("Corrupt save file!")
                    input("> ")
                    click_sound_effect.play()
            except OSError:
                print("No loadable save file!")
                input("> ")
                click_sound_effect.play()
        # Read Tutorial
        elif choice == "3":
            clear()
            tutorial = True
            tutor()
        # Quit Game
        elif choice == "4":
            clear()
            quit()
    # While Playing Game
    while play:
        # Autosave
        save()
        clear()
        #https://www.youtube.com/watch?v=0PMF36-00ag (1:10)
        if not standing:         
            if biom[map[y][x]]["e"]:
                if random.randint(0 ,100) <= 30:
                    fight = True
                    battle()
        # https://www.youtube.com/watch?v=i3j3iZNPUbI&t=35s (4:51)
        if play:
            clear()
            draw()
            print("            LOCATION: " + biom[map[y][x]]["t"])
            draw()
            print("NAME: " + name)
            print("HEALTH POINT (HP): " + str(HP) + "/" + str(HPMAX))
            print("LEVEL (LVL): " + str(LVL))
            print("EXPERIENCE (EXP): " + str(EXP))
            print("ATTACK POINT (ATK): " + str(ATK))
            print("DEFENCE POINT (DEF): " + str(DEF))
            print("SMALL POTIONS: " + str(s_pot))
            print("BIG POTIONS: " + str(b_pot))
            print("ELIXIRS: " + str(elix))
            print("GOLD: "+ str(gold))
            print("COORDINATE: " + "x: " +  str(x) + " y: " + str(y))
            draw()
            # https://www.youtube.com/watch?v=i3j3iZNPUbI&t=35s (5:36)
            print("0 - SAVE AND QUIT")
            if y > 0:
                print("1 - NORTH")
            if x < x_len:
                print("2 - EAST")
            if y < y_len:
                print("3 - SOUTH")
            if x > 0:
                print("4 - WEST")
            if s_pot > 0:
                print("5 - USE SMALL POTION (30HP)")
            if b_pot > 0:
                print("6 - USE BIG POTION (50HP)")
            if elix > 0:
                print("7 - USE ELIXIR (70HP)")
            print("8 - INVENTORY")
            if map[y][x] == "shop" or map[y][x] == "castle" or map[y][x] == "tower": #https://www.youtube.com/watch?v=wnizccXysKE&t=2s (0:43)
                print("9 - ENTER")
            draw()
            dest = input("# ")
            click_sound_effect.play()
            if dest == "0":
                play = False
                menu = True
                save()
            elif dest == "1":
                if y > 0:
                    y -= 1
                    if map[y][x] == "wall":
                        y += 1
                        print("You can't pass through wall")
                        input("> ")
                    standing = False
            elif dest == "2":
                if x < x_len:
                    x += 1
                    if map[y][x] == "wall":
                        x -= 1
                        print("You can't pass through wall")
                        input("> ")
                    if map[y][x] == "door" or map[y][x] == "fortress":
                        lock()
                    standing = False
            elif dest == "3":
                if  y < y_len:
                    y += 1
                    if map[y][x] == "wall":
                        y -= 1
                        print("You can't pass through wall")
                        input("> ")
                    standing = False
            elif dest == "4":
                if x > 0:
                    x -= 1
                    if map[y][x] == "wall":
                        x += 1
                        clear()
                        print("You can't pass through wall")
                        input("> ")
                    if x == 7:
                        clear()
                        x -= 1
                        print("  You are now in front of your castle")
                        input("> ")
                    if x == 15:
                        clear()
                        x -= 1
                        print("  You are now in the middle of the forest")
                        input("> ")

                    standing = False
            elif dest == "5":
                if s_pot > 0:
                    s_pot -= 1
                    heal(30)
                else:
                    print("You don't have any potions.")
                input("> ")
                standing = True
            elif dest == "6":
                if b_pot > 0:
                    b_pot -= 1
                    heal(50)
                else:
                    print("You don't have any potions.")
                input("> ")
                standing = True    
            elif dest == "7":
                if elix > 0:
                    elix -= 1
                    heal(70)
                else:
                    print("You don't have any Elixir.")
                input("> ")
                standing = True
            elif dest == "8":
                inven = True
                inventory()    
            elif dest == "9":
                if map[y][x] == "shop":
                    shop = True
                    shopping()
                if map[y][x] == "castle":
                    speak = True
                    castle()
                if map[y][x] == "tower":
                    boss = True
                    tower()
            else:
                standing = True