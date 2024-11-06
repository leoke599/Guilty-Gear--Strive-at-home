import random
import time

# Get current time (for time window comparisons)
def get_current_time():
    """ Returns the current time in seconds (for time window comparisons) """
    return time.time()

def perform_timed_combo(combo_sequence, time_limit=0.7):
    """ Checks if the player performs a combo within the time limit using W, A, S, D """
    start_time = get_current_time()  # Start the timer when the combo begins
    combo_index = 0  # Track where we are in the combo sequence
    combo_bonus = 1  # Default combo bonus multiplier (1x damage)
    
    print("\nCombo sequence started! You have 0.7 seconds to complete each move!")

    for action in combo_sequence:
        print(f"Waiting for input: {action}...")

        while True:
            current_time = get_current_time()  # Get current time
            elapsed_time = current_time - start_time  # Time elapsed since the last input

            if elapsed_time > time_limit:  # Timeout if too much time passes
                print(f"Combo input timed out! You took too long.")
                return 0  # Return 0 damage bonus if the combo fails
            
            # Try to get player input
            player_input = input(f"Press {action} (W/A/S/D): ").strip().lower()

            # If player input is correct, break the loop and move to next combo step
            if player_input == action:
                print(f"Correct! {action} executed.")
                combo_index += 1
                start_time = get_current_time()  # Reset the timer for the next move
                break
            else:
                print(f"Incorrect input! Try again.")
    
    # Successfully completed the combo within the time limit
    print("\nCombo completed! Bonus damage applied.")
    combo_bonus = 1.5  # Combo multiplier for the final move (1.5x damage for completing combo)
    return combo_bonus

def calculate_damage(base_damage, combo_bonus):
    """ Calculates damage with combo bonus """
    final_damage = base_damage * combo_bonus
    return final_damage

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

def cpu_choose_action():
    # Randomly choose an action for the CPU (can be expanded for smarter AI)
    return random.choice(["1", "2", "3", "4"])

def fight_opponent(player_strength, player_health, player_name, special_move, special_cooldown, player_agility, opponent_name, opponent_strength, opponent_health, opponent_agility):
    turns_left_on_special_cooldown = 0  # Track how many turns remain on special cooldown
    shield_active = False  # Whether the player is currently shielding
    
    combo_sequence = ["w", "a", "d"]  # Example combo sequence: Up (W) + Left (A) + Right (D)
    time_limit = 0.7  # Time limit for each input in the combo (in seconds)

    while player_health > 0 and opponent_health > 0:
        # Handle cooldown
        if turns_left_on_special_cooldown > 0:
            print(f"\n{player_name}'s special move is on cooldown for {turns_left_on_special_cooldown} more turns.")
            turns_left_on_special_cooldown -= 1

        action = choose_action()
        opponent_action = cpu_choose_action()  # CPU chooses its action

        # Timed Combo Damage Calculation
        combo_bonus = 1  # Default combo bonus (no combo)
        if action == "1":  # Attack
            print(f"\n{player_name} attacks {opponent_name}!")
            combo_bonus = perform_timed_combo(combo_sequence, time_limit)  # Perform combo check

        # Player's normal attack damage (with combo bonus)
        if combo_bonus > 1:
            damage = calculate_damage(player_strength, combo_bonus)
            if shield_active:  # Apply shield reduction
                damage *= 0.03  # Shield reduces damage to 3% of the original
            opponent_health -= damage
            print(f"{opponent_name} takes {damage} damage from combo attack!")
        elif action == "1":
            damage = max(0, player_strength - opponent_strength // 2)
            if shield_active:  # Apply shield reduction
                damage *= 0.03  # Shield reduces damage to 3% of the original
            opponent_health -= damage
            print(f"{opponent_name} takes {damage} damage from attack!")

        # Handle player actions
        if action == "2":  # Shield
            print(f"{player_name} shields!")
            shield_active = True
        
        elif action == "3":  # Special Move
            if turns_left_on_special_cooldown == 0:
                print(f"{player_name} uses {special_move}!")
                special_damage = player_strength * 1.5
                if shield_active:  # Apply shield reduction
                    special_damage *= 0.03  # Shield reduces damage to 3% of the original
                opponent_health -= special_damage
                print(f"{opponent_name} takes {special_damage} damage from {special_move}!")
                turns_left_on_special_cooldown = special_cooldown
            else:
                print(f"{player_name}'s special move is still on cooldown!")

        elif action == "4":  # Grab (Bypasses Shield)
            print(f"{player_name} attempts a grab on {opponent_name}!")
            grab_damage = player_strength * 0.4  # Full grab damage (bypasses shield)
            opponent_health -= grab_damage
            print(f"{opponent_name} takes {grab_damage} damage from the grab (bypasses shield)!")

        # Opponent's action
        if opponent_action == "1":  # Opponent Attack
            print(f"\n{opponent_name} attacks {player_name}!")
            if can_dodge(player_agility):
                print(f"{player_name} dodges the attack!")
            else:
                damage = max(0, opponent_strength - player_strength // 2)
                if shield_active:
                    damage *= 0.03  # Shield reduces damage to 3% of the original
                player_health -= damage
                print(f"{player_name} takes {damage} damage!")

        elif opponent_action == "2":  # Opponent Shield
            print(f"{opponent_name} shields!")

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
