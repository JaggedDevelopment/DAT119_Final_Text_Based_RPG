# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 13:51:48 2021

@author: Nicolas Shelley
Last Edited: 5/14/2021
Simple Text Based RPG with Saving and Reload System

This program is just a simple RPG game that uses all varaible types and allows the player to level,
accrue gold and defeat bosses. It uses a .txt file saving system that creates a list and the splits the list
back into usable variables. The game uses Rings as its checkpoints of progress. It is easily expandable
so that it could be used to create more dungeons or a more in depth gear system.
"""
import random
import sys

enemies = ["slime", "zombie"]

def global_constructor():
    #inventory Constructors
    global gold_wallet, potions_amount
    gold_wallet = 0 
    potions_amount = 3
    #player constructors
    global player_level, player_health, base_player_health, armor, weapon
    player_level = 0
    player_health = 10000
    base_player_health = 100
    armor = "none"
    weapon = "none"
    #enemy constructors
    global enemy_health, enemy, enemy_level
    #dungeon constructors
    global area, rooms, current_room
    #boss constructors
    global boss, boss_health, boss_attack_max, boss_battle_running
    boss_battle_running = False
    #Ring constructors
    global ruby_ring, saphire_ring, emerald_ring
    ruby_ring = False
    saphire_ring = False
    emerald_ring = False
    #player Exp System
    global current_xp, xp_gain, xp_needed
    current_xp = 0
    
    
def save_game():
    global gold_wallet,potions_amount,player_level, player_health, base_player_health, armor, weapon, area, ruby_ring, emerald_ring, saphire_ring
    #all global variables are saved so when the player rejoins the progress is not lost. The global variables control the entire game
    save_info = [str(player_health), str(player_level), str(gold_wallet), str(potions_amount), armor, weapon, area, str(emerald_ring), str(saphire_ring), str(ruby_ring)]
    
    print("\nSaving File...")
    
    save_data_file = open("text_adventure_save.txt", "w")
   
    for i in range(len(save_info)):
        save_data_file.write(save_info[i] + ', ')
        
    save_data_file.close()

    
    print("\nFiles Saved...")
    
    town()
    
def load_game():
    global gold_wallet,potions_amount,player_level, player_health, base_player_health, armor, weapon, area, ruby_ring, emerald_ring, saphire_ring
    load_info = []
    
    try:
        save_data_file = open("text_adventure_save.txt", "r")
    except OSError as e:
        #debug print('files do not exist', e)
        print('Welcome new user!')
        print('\nIf you are not a new user check the directory for your completed and todo items files.')
        menu()
    else: # runs if (and only if) the except clause does not run
        #debug print('files exist')
        
        print('\nLoading Files...')
        
        mailman = save_data_file.read()
        #reads the existing file
        mailman_split = mailman.split()
        #Splits the text from files into text to be appended later
        for i in range(len(mailman_split)):
            mailman_split[i] = mailman_split[i].strip(',')
            #strips commas
            load_info.append(mailman_split[i])
            #adds the stripped and split text to list
            i += 1
            
        #This section of code loads each piece of information into the game with proper data types  
        player_health = int(load_info[0])
        player_level = int(load_info[1])
        gold_wallet = int(load_info[2])
        potions_amount = int(load_info[3])
        armor = load_info[4]
        weapon = load_info[5]
        area = load_info[6]
        emerald_ring = bool(load_info[7])
        saphire_ring = bool(load_info[8])
        ruby_ring = bool(load_info[9])
        
        print("\nFiles successfully loaded...\n")
        print("Welcome Back!\nAs a reminder heres your stats:\nHealth:", player_health, "\nLevel:", player_level,"\nGold:", gold_wallet,"\nPotions", potions_amount,"\nArmor:", armor,"\nWeapon:", weapon,"\nCurrent Area:", area.title)
        print(" ")
        save_data_file.close()
        town()
        forest()

def menu():
    navigation = 0
    menu = ["Start New Game", "Load Game", "Quit"]
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1
        
    navigation = input("\nEnter a number to select a menu item... ")    
    
    if navigation == "1":
        town()
    elif navigation == "2":
        load_game()
    elif navigation == "3":
        sys.exit()
    else:
        print("invalid entry...")
        menu()

def town():
    menu = ["Journey to a Dungeon", "Alchemist", "Blacksmith", "Save Game"]
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1

    navigation = input("\nEnter a number to select a menu item... ")

    if navigation == "1":
        dungeons()
    elif navigation == "2":
        alchemist()
    elif navigation == "3":
        blacksmith()
    elif navigation == "4":
        save_game()
    else:
        print("invalid entry...")
        town()

def alchemist():
    print("\nWelcome to Brooding Mary's! I'll be right with you!")
    
    menu = ["Buy Potion", "Return to Town"]
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1

    navigation = input("\nEnter a number to select a menu item... ")

    if navigation == "1":
        potion_sale()
    elif navigation == "2":
        town()
    else:
        print("invalid entry...")
        alchemist()

def potion_sale():
    global gold_wallet, potions_amount
    
    if (gold_wallet < 20):
        print("Sorry but you are too short on gold to be shopping here...")
        town()
    else:
        print("How many do you want?")
        cost = 20
        total_available = gold_wallet/cost #tells player how many potions they can buy max
        print("You have enough gold to buy:", total_available, "\nEnter 0 to return...\n")
        purchase = int(input("Enter total to purchase: "))#amount player wants to buy
        if(purchase <= total_available):
            gold_wallet -= (purchase * cost)#charges player gold
            potions_amount += purchase#adds potions to potions_amount
        elif(purchase > total_available or purchase < 0):#ensures valid entry
            print("Thats not a valid option... ")
            potion_sale()
        elif(purchase == 0):#returns
            alchemist()
        
def blacksmith():
    print("Welcome to McGough's Smithy Adventurer!\nHow can I be of service?")
    menu = ["Buy Armor","Buy Weapon","Return to Town"]
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1
        
    navigation = input("\nEnter a number to select a menu item... ")
    
    if navigation == "1":
        blacksmith_armor()
    elif navigation == "2":
        blacksmith_weapon()
    elif navigation == "3":
        town()
    else:
        print("invalid entry...")
        blacksmith()
        
def blacksmith_armor():
    global base_player_health, player_health, armor, gold_wallet
    menu = ["Iron Armor : 150 G", "Steel Armor : 300 G", "Dragon Bone Armor : 500 G", "Return to Smithy Menu"]
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1
        
    navigation = input("\nEnter a number to select a menu item... ")
    
    if navigation == "1":
        cost = 150
        if (gold_wallet < cost):
            print("Sorry pal not enough gold...")
        else:
            base_player_health = 150
            armor = "iron"
            player_health = base_player_health
            print("Here's your", armor, "armor.  \n*while you were waiting your health restores and you gain a buff from the new armor*")
        blacksmith()
    elif navigation == "2":
        cost = 300
        if (gold_wallet < cost):
            print("Sorry pal not enough gold...")
        else:
            base_player_health = 250
            armor = "steel"
            player_health = base_player_health
            print("Here's your", armor, "armor.  \n*while you were waiting your health restores and you gain a buff from the new armor*")
        blacksmith()
    elif navigation == "3":
        cost = 500
        if (gold_wallet < cost):
            print("Sorry pal not enough gold...")
        else:
            base_player_health = 500
            armor = "dragonbone"
            player_health = base_player_health
            print("Here's your", armor, "armor.  \n*while you were waiting your health restores and you gain a buff from the new armor*")
        blacksmith()
    elif navigation == "4":
        blacksmith()
    else:
        print("invalid option...")
        blacksmith_armor()
    
def blacksmith_weapon():
    global weapon
    menu = ["Sword : 100 G", "Axe : 250 G", "Drakesbane : 450 G", "Return to Smithy Menu"]
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1
        
    navigation = input("\nEnter a number to select a menu item... ")
    
    if navigation == "1":
        cost = 100
        if (gold_wallet < cost):
            print("Sorry pal not enough gold...")
        else:
            weapon = "sword"
            print("Thanks for your patronage adventurer! Heres your", weapon)
        blacksmith()
    elif navigation == "2":
        cost = 250
        if (gold_wallet < cost):
            print("Sorry pal not enough gold...")
        else:
            weapon = "axe"
            print("Thanks for your patronage adventurer! Heres your", weapon)
        blacksmith()
    elif navigation == "3":
        cost = 450
        if (gold_wallet < cost):
            print("Sorry pal not enough gold...")
        else:
            weapon = "drakesbane"
            print("Thanks for your patronage adventurer! Heres your", weapon)
        blacksmith()
    elif navigation == "4":
        blacksmith()
    else:
        print("invalid option...")
        blacksmith_weapon()
        
def dungeons():
    menu = ["Forest", "Ocean", "Volcano", "Return to Town"]
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1

    navigation = input("\nEnter a number to select a menu item... ")

    if navigation == "1":
        forest()
    if navigation == "2":
        if (emerald_ring == False):
            print("You do not posess the treasure of the golem...\nComplete the forest dungeon to proceed...")
            dungeons()
        else:
            ocean()
    elif navigation == "3":
        if (saphire_ring == False):
            print("You do not posess the treasure of the serpent...\nComplete the forest dungeon to proceed...")
            dungeons()
        else:
            volcano()        
    elif navigation == "4":
        town()  
    else:
        print("invalid option...")
        dungeons()

def forest():
    global area, rooms, current_room, enemies
    area = "forest"
    current_room = 0
    rooms = random.randint(3,5)
    enemies = ["zombie", "skeleton", "goblin", "moss bug"]
    menu = ["Continue Onward","Check Equipment", "Return to Town"]
    
    print("\nWelcome to the Cursed Forests of Gardenia. \nThe Legends state there's a mysterious Golem that guards a precious ring deep in the forest dungeon.\n")
    
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1
    
    navigation = input("\nEnter a number to select a menu item... ")
    
    if navigation == "1":
        battle()
    if navigation == "2":
        equip_check()
    if navigation == "3":
        town()
    else:
        print("invalid option...")
        forest()

def ocean():
    global area, rooms, current_room, enemies
    area = "ocean"
    current_room = 0
    rooms = random.randint(4,6)
    enemies = ["drowned", "dragoon", "trident drowned", "water-logged bug"]
    menu = ["Continue Onward","Check Equipment", "Return to Town"]
    
    print("\nWelcome to the Tidal Lands of Oceania. \nThe Legends state there's a powerful Sea Serpent devouring those who try to enter its domain.\n")
    
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1
    
    navigation = input("\nEnter a number to select a menu item... ")
    
    if navigation == "1":
        battle()
    if navigation == "2":
        equip_check()
    if navigation == "3":
        town()
    else:
        print("invalid option...")
        ocean()
        
def volcano():
    global area, rooms, current_room, enemies
    area = "volcano"
    current_room = 0
    rooms = random.randint(5,7)
    enemies = ["crystal lizard", "obsidian skeleton", "flame golem", "molten bug"]
    menu = ["Continue Onward","Check Equipment", "Return to Town"]
    
    print("\nWelcome to the Molten Rivers of Advarna. \nThe Legends state there's a powerful dragon that guards a precious ring at the volcano's peak.\n")
    
    
    for i in range(len(menu)):
        print(i + 1, menu[i])
        i += 1
    
    navigation = input("\nEnter a number to select a menu item... ")
    
    if navigation == "1":
        battle()
    if navigation == "2":
        equip_check()
    if navigation == "3":
        town()
    else:
        print("invalid option...")
        volcano()        

def equip_check():
    global area, armor, weapon
    print("Armor: ", armor,"\nWeapon: ", weapon)
    if (area == "forest"):
        forest()
    if (area == "ocean"):
        ocean()
    if (area == "volcano"):
        volcano()
    
def battle():
    global enemy_health, player_health, enemy, enemy_level, enemies, current_room, rooms
    
    current_room += 1
    
    if (current_room >= rooms):
        boss_start()
    
    enemy = enemies[random.randint(0, (len(enemies)-1))]
    print("\nA", enemy, "appeared!\n")
    print("Current Room:", current_room,"/", rooms)
    
    if(area == "forest"):
        enemy_health = random.randint(20, 50)
        enemy_level = random.randint(1,5)
    if(area == "ocean"):
        enemy_health = random.randint(40, 60)
        enemy_level = random.randint(4,11)
    if(area == "volcano"):
        enemy_health = random.randint(50, 80)
        enemy_level = random.randint(10,20)
        
    battle_idle()
    
def battle_idle():
    global enemy_health, player_health, enemy, enemy_level, player_level
    battle_menu = ["Fight", "Potion", "Escape"]
    
    if(player_health <= 0):
        game_over()
    if(enemy_health <= 0):
        win_loot()
    
    print("\nThe", enemy, "has", enemy_health, "health left!")
    print("Enemy lvl:", enemy_level)
    print("\nPlayer lvl:", player_level, "\nPlayer Health:", player_health, "\n")
    for i in range(len(battle_menu)):
        print(i + 1, battle_menu[i])
        i += 1
    
    navigation = input("\nEnter a number to select a menu item... ")
    
    if navigation == "1":
        player_attack()
    elif navigation == "2":
        potion_bag()
    elif navigation == "3":
        town()
    else:
        print("invalid option...")
        battle_idle()
        
def player_attack():
    global enemy_health, player_health, enemy, enemy_level, player_level
    player_attack_max = (player_level * 2) + 15
    if (weapon == "sword"):
        player_attack_max += 15
    elif (weapon == "axe"):
        player_attack_max += 30
    elif (weapon == "drakesbane"):
        player_attack_max += 60
    player_hit = random.randint(1, player_attack_max)
    enemy_health -= player_hit
    
    if (enemy_health <= 0):
        enemy_health = 0

    
    print("\nPlayer attacks", enemy, "for", player_hit, "damage!")
    print("Enemy has", enemy_health, "left.\n")
    
    enemy_attack()
    
def enemy_attack():
    global enemy_health, player_health, enemy, enemy_level
    enemy_attack_max = (enemy_level * 2) + 5
    enemy_hit = random.randint(1, enemy_attack_max)
    player_health -= enemy_hit
    
    if (player_health <= 0):
        player_health = 0
        
    print(enemy, "attacks for", enemy_hit, "damage!")
    print("Player has", player_health, "left.\n")
    
    battle_idle()
    
def boss_start():
    global area, boss, boss_health, boss_attack_max, boss_battle_running, emerald_ring, saphire_ring, ruby_ring
    
    if (area == "forest"):
        if(emerald_ring == False):
            boss = "Titan"
            boss_health = random.randint(175,250)
            boss_attack_max = 30
            print("The mighty golem drops from the ceiling of the treasure room!")
        else:
            print("You've already defeated the golem!\n Returning to town...")
            town()
    if (area == "ocean"):
        if(saphire_ring == False):
            boss = "Serpent"
            boss_health = random.randint(225,300)
            boss_attack_max = 50
            print("The fearsome serpent darts from the waters! Rapidly approaching!")
        else:
            print("You've already defeated the serpent!\n Returning to town...")
            town()
    if (area == "volcano"):
        if(emerald_ring == False):
            boss = "Igmael"
            boss_health = random.randint(175,250)
            boss_attack_max = 75
            print("As you reach the peak the dragon notices your prescence and screeches as it plumets towards you!")
        else:
            print("You've already defeated the dragon!\n Returning to town...")
            town()
            
            
    boss_battle_running = True        
    boss_idle()

def boss_idle():
    global boss, boss_health, player_health, player_level
    battle_menu = ["Fight", "Potion", "Escape"]
    
    if(player_health <= 0):
        game_over()
    if(boss_health <= 0):
        win_loot()
    
    print("\nThe", boss, "has", boss_health, "health left!\n")
    print("\nPlayer lvl:", player_level, "\nPlayer Health:", player_health, "\n")
    for i in range(len(battle_menu)):
        print(i + 1, battle_menu[i])
        i += 1
    
    navigation = input("\nEnter a number to select a menu item... ")
    
    if navigation == "1":
        player_boss_attack()
    if navigation == "2":
        potion_bag()
    if navigation == "3":
        print("You run out before the golem notices your there.")
        town()
    else:
        print("invalid option...")
        boss_idle()
        
def player_boss_attack():   
    global boss, boss_health, player_health, player_level
    
    player_attack_max = (player_level * 2) + 15 #calculates the players attack based on level
    if (weapon == "sword"):
        player_attack_max += 15
    elif (weapon == "axe"):
        player_attack_max += 30
    elif (weapon == "drakesbane"):
        player_attack_max += 60
    player_hit = random.randint(1, player_attack_max)
    boss_health -= player_hit
    
    if (boss_health <= 0):
        boss_health = 0

    
    print("\nPlayer attacks", boss, "for", player_hit, "damage!")
    print("Boss has", boss_health, "left.\n")
    
    boss_attack()
    
def boss_attack():  
    global boss, boss_health, player_health, player_level
        
    boss_hit = random.randint(1, boss_attack_max)
    player_health -= boss_hit
    
    if (player_health <= 0):
        player_health = 0
        
    print(boss, "attacks for", boss_hit, "damage!")
    print("Player has", player_health, "left.\n")
    
    boss_idle()
    
def potion_bag():
    global potions_amount, player_health, boss_battle_running
    
    if(potions_amount >= 1):
        #adds hp to the players health
        player_health += 50
        potions_amount -= 1
        print("You healed for 50 HP!\nYou have", potions_amount, "potions left")
        
    else:
        print("You have no potions...")
        
    if(boss_battle_running == True):
        boss_idle()
    else:
        battle_idle()
        
def game_over():
    global enemy_health, player_health, player_level, enemy, enemy_level
    print("\nAfter the journey into the dungeon the adventurer's story had come to an end.")  
    sys.exit()

def win_loot():
    global gold_wallet, potions_amount, enemy, xp_gain, current_xp
    if (boss_battle_running == True):
        enemy = boss
        
    print("Congrats! you beat the", enemy +"!")
    
    xp_gain = random.randint(5, 15)
    
    #multiplies the xp if the battle was a boss battle
    if (boss_battle_running == True):
        xp_gain *= 3
    current_xp += xp_gain #adds the battle xp gain to the players total xp
    
    drop_chance = random.randint(0,100)
    #creates a 60 percent chance of gold drop
    if(drop_chance <= 60):
        gold_drop = 0
        gold_drop = random.randint(2,10)
        gold_wallet += gold_drop
        print("\nThe", enemy, "had", gold_drop, "pieces of gold!")
        print("You now have", gold_wallet, "gold in your wallet.\n")
        
    drop_chance = random.randint(0,100)
    #creates a 30 percent chance of potion drop
    if(drop_chance <= 30):
        pot_drop = 1
        potions_amount += pot_drop
        print("The", enemy, "dropped a health potion.")
        
    #runs the function to check if player leveled up or not
    xp_system()
 
def xp_system():
    global xp_needed,player_level,current_xp,xp_gain,boss_battle_running
    xp_needed = [1,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,42,47,52,57,62,67,72,77,82,87,92,97,102,117,112]
    #Each number is attached to a player level. this is the amount of xp required to reach the next level in the game
    
    
    
    if (player_level < 30):
        #this simply allows the player to level through the game until the level cap of 30
        print("You gained", xp_gain, "xp. \nYou still need")
        if(current_xp >= xp_needed[player_level]):# this controls when the player levels up
            player_level +=1
            current_xp = 0 #resets the xp for the player to reach the next level
            print("You've leveled up!")
    elif(player_level >= 30):
        print("You've reached the level cap. Good Job!")
    
    print(xp_needed[player_level],"xp to get to gain level")
    
    if(boss_battle_running == True):
        boss_battle_running = False
        town()
    else:
        battle()

def ring_reward():
    global emerald_ring, saphire_ring, ruby_ring, area
    if (area == "forest"):
        print("You've defeated the great guardian of the forest relic.\nYou discover a bright green emerald ring on pedestal behind where the once proud defender stood.\nWith the ring there is a letter.")
        print("The letter reads *I see you've defeated the great golem created by the one who brought life to this land.\nThe ring that he guarded is a stone of power once the 3 stones that are deep within the dungeons are reunited\nthe dungeons will close up never to be used again.")
        print("Closing the dungeons will erase all manner of monsters that attack villages and kill caravans, but alas no hero has been able to collect all 3* The letter ends...")
        emerald_ring = True
        print("I must go to the ocean dungeon and find the ring. If there's a way to keep everyone safe it must be done!")
        town()
    if (area == "ocean"):
        print("After a tough battle the serpent falls to ocean floor.\n As you enter its treasure room you notice a bright blue stone on a pedestal.\n It's the saphire ring that matches the emerald ring from the forest!")
        print("You stow away the ring and the leave the dungeon. A voice speaks from the heavens *congrats young adventurer! you've only one more ring to go.* the voice fades.")
        print("It's time to conquer the volcano dungeon. I should train and get better gear for the upcoming task.")
        saphire_ring = True
        town()
    if (area == "volcano"):
        print("With burned gear and broken bones you enter the dragons keep as the dead dragon lay before you. \nYou take the ruby colored ring from the keeps alter and leave before any more monsters arrive")
        print("The same voice from before seems to speak inside your head.*Unite the three rings and all shall be done* \nthe adventurer places all the rings on a nearby stone and the dragons keep crumbles into the ground.")
        print("The adventurer has done it! the task has been completed and the villages will have no monster to fear!")
        ruby_ring = True
        ending_credits()
        
def ending_credits():
    print("Thanks for playing!\nCreated by: Nicolas J Shelley")
    
def main():
    global_constructor()
    menu()

if __name__ == "__main__":
    
    main()