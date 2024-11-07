import random
import time
import threading

# Get current time (for time window comparisons)
def get_current_time():
    """ Returns the current time in seconds (for time window comparisons) """
    return time.time()

# Function to handle input with timeout using threading
def timed_input(prompt, timeout=1.0):
    """ Returns player input or None if timeout occurs """
    print(prompt, end='', flush=True)

    # This function will store the input in a global variable
    input_received = [None]

    def get_input():
        input_received[0] = input().strip().lower()

    # Start the input thread
    input_thread = threading.Thread(target=get_input)
    input_thread.start()

    # Wait for the input or timeout
    start_time = time.time()
    while input_received[0] is None:
        if time.time() - start_time >= timeout:
            return None  # Timeout after the specified duration
        time.sleep(0.01)

    input_thread.join()
    return input_received[0]

def generate_random_combo(length=10):
    """ Generates a random combo sequence of length `length` with W, A, S, D inputs """
    return [random.choice(["w", "a", "s", "d"]) for _ in range(length)]

def perform_timed_combo(combo_sequence, time_limit=1.0):
    """ Checks if the player performs a combo within the time limit using W, A, S, D """
    start_time = get_current_time()  # Start the timer when the combo begins
    combo_index = 0  # Track where we are in the combo sequence
    combo_bonus = 1  # Default combo bonus multiplier (1x damage)
    
    print("\nCombo sequence started! You have 1 second to complete each move!")

    for action in combo_sequence:
        print(f"Waiting for input: {action}...")

        while True:
            current_time = get_current_time()  # Get current time
            elapsed_time = current_time - start_time  # Time elapsed since the last input

            if elapsed_time > time_limit:  # Timeout if too much time passes
                print(f"Combo input timed out! You took too long.")
                return 0.4  # Changed from 0.7 to 0.4 (40% damage if combo fails)
            
            # Try to get player input
            player_input = timed_input(f"Press {action} (W/A/S/D): ", time_limit)

            if player_input is None:  # Timeout if no input
                print(f"Combo input timed out!")
                return 0.4  # Changed from 0.7 to 0.4 (40% damage if combo fails)

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
    combo_bonus = 1.2  # Combo multiplier for the final move (1.2x damage for completing combo)
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
    """CPU chooses an action randomly, but ensures it always picks something"""
    return random.choice(["1", "2", "3", "4"])

def special_move_message(character, special_move, damage):
    if special_move == "Bandit Bringer":
        print(f"\n{character} roars and unleashes a massive {special_move}, sending shockwaves through the arena!")
        print(f"The attack deals {damage} damage to the opponent!")
    elif special_move == "Sacred Edge":
        print(f"\n{character} raises his sword high and slashes with a divine {special_move}, cutting through the air!")
        print(f"The attack deals {damage} damage to the opponent!")
    elif special_move == "Dolphin Dive":
        print(f"\n{character} summons a playful dolphin and leaps into the air, crashing down with a devastating {special_move}!")
        print(f"The attack deals {damage} damage to the opponent!")
    elif special_move == "Ninja Teleport":
        print(f"\n{character} disappears in a puff of smoke and reappears behind the opponent, landing a quick {special_move}!")
        print(f"The attack deals {damage} damage to the opponent!")
    elif special_move == "Stroke of Midnight":
        print(f"\n{character} strums their guitar, sending a shockwave through time with {special_move}!")
        print(f"The attack deals {damage} damage to the opponent!")
    elif special_move == "Minion Summon":
        print(f"\n{character} summons a horde of minions to overwhelm the opponent with {special_move}!")
        print(f"The attack deals {damage} damage to the opponent!")
    elif special_move == "Chaos Bullet":
        print(f"\n{character} channels chaotic energy and fires a devastating {special_move}, ripping through reality itself!")
        print(f"The attack deals {damage} damage to the opponent!")

def fight_opponent(player_strength, player_health, player_name, special_move, special_cooldown, player_agility, opponent_name, opponent_strength, opponent_health, opponent_agility):
    shield_active = False
    opponent_shield_active = False
    turns_left_on_special_cooldown = 0
    combo_sequence = generate_random_combo()
    combo_bonus = 1

    while player_health > 0 and opponent_health > 0:
        # Player chooses their action
        action = choose_action()
        
        # CPU chooses its action
        opponent_action = cpu_choose_action()  # Get the opponent's action

        # First, handle the player's action:
        if action == "1":  # Player Attack
            print(f"\n{player_name} attacks {opponent_name}!")
            combo_sequence = generate_random_combo()
            combo_bonus = perform_timed_combo(combo_sequence)  # Perform combo check
            damage = calculate_damage(player_strength, combo_bonus)

            # If the opponent shields, apply the shield effect here first
            if opponent_shield_active:
                damage *= 0.2  # Opponent takes 20% of damage if shielded
                print(f"{opponent_name} is shielding! Damage reduced.")
            opponent_health -= damage
            print(f"{opponent_name} takes {damage} damage from the attack!")

        elif action == "2":  # Player Shield
            print(f"{player_name} shields!")
            shield_active = True
        elif action == "3":  # Player Special Move
            if turns_left_on_special_cooldown == 0:
                print(f"{player_name} uses {special_move}!")
                special_damage = player_strength * 1.5
                if opponent_shield_active:
                    special_damage *= 0.2  # Reduce special damage if opponent shields
                    print(f"{opponent_name} is shielding! Special damage reduced.")
                opponent_health -= special_damage
                special_move_message(player_name, special_move, special_damage)
                turns_left_on_special_cooldown = special_cooldown
            else:
                print(f"{player_name}'s special move is still on cooldown for {turns_left_on_special_cooldown} more turns.")
        
        elif action == "4":  # Player Grab
            print(f"{player_name} attempts a grab on {opponent_name}!")
            grab_damage = player_strength * 0.4
            opponent_health -= grab_damage
            print(f"{opponent_name} takes {grab_damage} damage from the grab!")

        # Now handle the opponent's action:
        if opponent_action == "1":  # Opponent Attack
            print(f"\n{opponent_name} attacks {player_name}!")
            damage = opponent_strength
            # If the player shields, apply the shield effect here first
            if shield_active:
                damage *= 0.2  # Player takes 20% damage if shielded
                print(f"{player_name} is shielding! Damage reduced.")
            player_health -= damage
            print(f"{player_name} takes {damage} damage from the opponent's attack!")

        elif opponent_action == "2":  # Opponent Shield
            print(f"{opponent_name} shields!")
            opponent_shield_active = True

        elif opponent_action == "3":  # Opponent Special Move
            print(f"{opponent_name} uses a special move!")
            special_damage = opponent_strength * 1.5
            if shield_active:
                special_damage *= 0.2  # Reduce special damage if player shields
                print(f"{player_name} is shielding! Special damage reduced.")
            player_health -= special_damage
            print(f"{player_name} takes {special_damage} damage from {opponent_name}'s special move!")

        elif opponent_action == "4":  # Opponent Grab
            print(f"{opponent_name} attempts a grab on {player_name}!")
            grab_damage = opponent_strength * 0.4
            player_health -= grab_damage
            print(f"{player_name} takes {grab_damage} damage from the grab!")

        # Show health after each turn:
        print(f"\n{player_name}'s Health: {player_health}")
        print(f"{opponent_name}'s Health: {opponent_health}\n")

        # Check for the end of the battle
        if player_health <= 0:
            print(f"\n{player_name} has been defeated by {opponent_name}!")
            break
        elif opponent_health <= 0:
            print(f"\n{opponent_name} has been defeated by {player_name}!")
            break

        # Reset shields for the next round
        shield_active = False
        opponent_shield_active = False


def main():
    display_intro()
    show_character_options()
    player_choice = get_character_choice()
    player_name, player_strength, player_health, special_move, special_cooldown, player_agility = get_character_attributes(player_choice)

    display_character_info(player_name, player_strength, player_health, special_move, special_cooldown, player_agility)

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

    fight_opponent(player_strength, player_health, player_name, special_move, special_cooldown, player_agility, opponent_name, opponent_strength, opponent_health, opponent_agility)

if __name__ == "__main__":
    main()
