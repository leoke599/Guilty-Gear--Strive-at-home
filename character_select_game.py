import random

# Guilty Gear Strive Combat System

def display_intro():
    print("Welcome to the Guilty Gear Strive Combat System!")
    print("Fight and prove your strength!\n")

def show_character_options():
    print("Choose your fighter:")
    print("1. Sol Badguy (Special: Bandit Bringer - A powerful charge attack)")
    print("2. Ky Kiske (Special: Sacred Edge - A powerful sword slash)")
    print("3. May (Special: Dolphin Dive - Summons a dolphin to attack)")
    print("4. Chip Zanuff (Special: Ninja Teleport - Teleports and attacks)")
    print("5. I-No (Special: Stroke of Midnight - A time-based guitar attack)")
    print("6. Jack-O (Special: Minion Summon - Summons minions to fight for you)")
    print("7. Happy Chaos (Special: Chaos Bullet - Fires a bullet of chaotic energy)")

def get_character_choice():
    while True:
        try:
            choice = int(input("Enter the number of your choice (1-7): "))
            if 1 <= choice <= 7:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_character_attributes(choice):
    # Attributes: (Name, Strength, Health, Special Move, Special Cooldown, Agility)
    if choice == 1:
        return "Sol Badguy", 18, 120, "Bandit Bringer", 2, 8
    elif choice == 2:
        return "Ky Kiske", 14, 100, "Sacred Edge", 3, 7
    elif choice == 3:
        return "May", 16, 80, "Dolphin Dive", 2, 10
    elif choice == 4:
        return "Chip Zanuff", 12, 70, "Ninja Teleport", 1, 12
    elif choice == 5:
        return "I-No", 14, 90, "Stroke of Midnight", 3, 6
    elif choice == 6:
        return "Jack-O", 14, 100, "Minion Summon", 4, 5
    elif choice == 7:
        return "Happy Chaos", 12, 90, "Chaos Bullet", 3, 9

def display_character_info(character, strength, health, special_move, special_cooldown, agility):
    print(f"\nYou have chosen: {character} ({special_move})")
    print(f"Strength: {strength}")
    print(f"Health: {health}")
    print(f"Agility: {agility}")
    print(f"Special move cooldown: {special_cooldown} turns\n")
    print("Get ready for battle!\n")

def can_dodge(agility):
    dodge_chance = min(agility * 5, 50)  # Max dodge chance capped at 50%
    dodge_roll = random.randint(0, 99)
    return dodge_roll < dodge_chance  # Dodge chance

def choose_action():
    print("\nChoose your action:")
    print("1. Attack")
    print("2. Shield")
    print("3. Use Special Move (Cooldown may apply)")
    print("4. Use Grab (Bypasses Shield!)")
    action = input("What will you do? (1/2/3/4): ")
    return action

def calculate_special_damage(character_name, strength, special_move):
    # Calculate damage based on character's strength and specific special move
    if special_move == "Bandit Bringer":
        damage = strength * 1.6  # Sol Badguy's special is a powerful charge
    elif special_move == "Sacred Edge":
        damage = strength * 1.4  # Ky Kiske's sacred sword slash
    elif special_move == "Dolphin Dive":
        damage = strength * 1.3  # May's dolphin move benefits from agility
    elif special_move == "Ninja Teleport":
        damage = strength * 1.2  # Chip's teleport strike, lower damage but fast
    elif special_move == "Stroke of Midnight":
        damage = strength * 1.5  # I-No's time-altering guitar move
    elif special_move == "Minion Summon":
        damage = strength * 1.2  # Jack-O's minions deal less damage directly
    elif special_move == "Chaos Bullet":
        damage = strength * 1.8  # Happy Chaos's chaotic bullet is devastating
    else:
        damage = strength * 1.3  # Default special damage for unknown moves
    return damage

def fight_opponent(player_strength, player_health, player_name, special_move, special_cooldown, player_agility, opponent_name, opponent_strength, opponent_health, opponent_agility):
    # Track cooldowns
    player_special_cooldown = 0  # Player's special cooldown
    opponent_special_cooldown = 0  # Opponent's special cooldown
    shield_active = False  # Whether the player is currently shielding

    while player_health > 0 and opponent_health > 0:
        # Handle cooldowns
        if player_special_cooldown > 0:
            print(f"\n{player_name}'s special move is on cooldown for {player_special_cooldown} more turns.")
            player_special_cooldown -= 1

        if opponent_special_cooldown > 0:
            print(f"\n{opponent_name}'s special move is on cooldown for {opponent_special_cooldown} more turns.")
            opponent_special_cooldown -= 1

        action = choose_action()
        opponent_action = random.choice(["1", "2", "3", "4"])

        # Player's action
        if action == "1":
            print(f"\n{player_name} attacks {opponent_name}!")
            if can_dodge(opponent_agility):
                print(f"{opponent_name} dodges the attack!")
            else:
                if opponent_action == "2":
                    # Opponent shields
                    print(f"{opponent_name} is shielding!")
                    damage = max(0, player_strength * 0.03)  # Shield reduces damage to 3%
                    opponent_health -= damage
                    print(f"{opponent_name} takes {damage} damage after shield!")
                else:
                    damage = max(0, player_strength - opponent_strength // 2)
                    opponent_health -= damage
                    print(f"{opponent_name} takes {damage} damage!")
        
        elif action == "2":
            print(f"\n{player_name} shields!")
            shield_active = True

        elif action == "3":
            if player_special_cooldown == 0:
                print(f"\n{player_name} uses {special_move}!")

                # Calculate special damage based on character's strength and special move
                special_damage = calculate_special_damage(player_name, player_strength, special_move)
                opponent_health -= special_damage
                print(f"{opponent_name} takes {special_damage} damage from {special_move}!")
                player_special_cooldown = special_cooldown
            else:
                print(f"\n{player_name}'s special move is still on cooldown!")

        elif action == "4":
            print(f"\n{player_name} attempts a grab on {opponent_name}!")
            grab_damage = player_strength * 0.4  # Reduced grab damage to 40%
            opponent_health -= grab_damage
            print(f"{opponent_name} takes {grab_damage} damage from the grab (bypasses shield)!")

        else:
            print("\nInvalid action. Please choose 1, 2, 3, or 4.")
            continue

        # Opponent's action
        if opponent_action == "1":
            print(f"\n{opponent_name} attacks {player_name}!")
            if can_dodge(player_agility):
                print(f"{player_name} dodges the attack!")
            else:
                if shield_active:
                    # Player shields
                    damage = max(0, opponent_strength * 0.03)  # Shield reduces damage to 3%
                    player_health -= damage
                    print(f"{player_name} takes {damage} damage after shield!")
                else:
                    damage = max(0, opponent_strength - player_strength // 2)
                    player_health -= damage
                    print(f"{player_name} takes {damage} damage!")
        
        elif opponent_action == "2":
            print(f"{opponent_name} shields!")
        
        elif opponent_action == "3":
            if opponent_special_cooldown == 0:
                # Calculate opponent's special damage
                special_damage = calculate_special_damage(opponent_name, opponent_strength, special_move)
                player_health -= special_damage
                print(f"{opponent_name} uses their special move and deals {special_damage} damage to {player_name}!")
                opponent_special_cooldown = 3
            else:
                print(f"{opponent_name}'s special move is still on cooldown!")

        elif opponent_action == "4":
            grab_damage = opponent_strength * 0.4  # Reduced grab damage to 40%
            player_health -= grab_damage
            print(f"{player_name} takes {grab_damage} damage from the grab (bypasses shield)!")

        # End turn updates
        shield_active = False  # Reset shield at the end of the turn

        # Show health after each turn
        print(f"\n{player_name}'s Health: {player_health}")
        print(f"{opponent_name}'s Health: {opponent_health}\n")

        if player_health <= 0:
            print(f"\n{player_name} has been defeated by {opponent_name}!")
            break
        elif opponent_health <= 0:
            print(f"\n{opponent_name} has been defeated by {player_name}!")
            break

def main():
    display_intro()
    
    # Choose your fighter
    show_character_options()
    player_choice = get_character_choice()
    player_name, player_strength, player_health, special_move, special_cooldown, player_agility = get_character_attributes(player_choice)

    # Display player info
    display_character_info(player_name, player_strength, player_health, special_move, special_cooldown, player_agility)

    # Battle Loop (vs CPU)
    opponents = [
        ("Sol Badguy", 18, 120, 8),
        ("Ky Kiske", 14, 100, 7),
        ("May", 16, 80, 10),
        ("Chip Zanuff", 12, 70, 12),
        ("I-No", 14, 90, 6),
        ("Jack-O", 14, 100, 5),
        ("Happy Chaos", 12, 90, 9)
    ]
    opponent_name, opponent_strength, opponent_health, opponent_agility = random.choice(opponents)

    print(f"\nYour opponent is {opponent_name}!\n")

    # Start the battle
    fight_opponent(player_strength, player_health, player_name, special_move, special_cooldown, player_agility, opponent_name, opponent_strength, opponent_health, opponent_agility)

if __name__ == "__main__":
    main()

