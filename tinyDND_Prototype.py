import random

# Character stats
class Character:
    def __init__(self, name, hp, attack, defense, luck, special):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.luck = luck
        self.special = special
        self.stunned = False

# Player
player = Character("Jason", 60, 5, 13, 5, "earth_shield")

# Bosses
jorvalkarith = Character("Jorvalkarith", 70, 4, 15, 2, "root_bind")
balzeth = Character("Balzeth", 100, 7, 12, 1, "retsunami")
demon_king = Character("Demon King", 120, 8, 16, 4, "soul_burnt")

bosses = [jorvalkarith, balzeth, demon_king]

def roll_d20(): # Dice 20
    return random.randint(1, 20)

def roll_d8(): # Dice 8
    return random.randint(1, 8)

def roll8_damage(attacker): # Calculate attack damage
    return attacker.attack + roll_d8()

def roll20_decision(character, difficulty = 15): # Roll success or fail
    return roll_d20() + character.luck >= difficulty # >= 15 is success, < 15 is fail

def hit_check(attacker, target): # Check if player hit or missed
    roll = roll_d20()

    if roll == 1:
        return "crit_fail"
    
    if roll == 20:
        return "crit_hit"
    
    if roll + attacker.luck >= target.defense:
        return "hit"
    
    return "miss"

def attack(attacker, target):
    result = hit_check(attacker, target)

    if result == "crit_hit":
        damage = roll8_damage(attacker) * 2
        target.hp = max(0, target.hp - damage)

        print(f"CRITICAL HIT! {attacker.name} dealt {damage} damage to {target.name}!")

    elif result == "hit":
        damage = roll8_damage(attacker)
        target.hp = max(0, target.hp - damage)

        print(f"{attacker.name} hit {target.name} with {damage} damage!")

    elif result == "crit_fail":
        print(f"{attacker.name} critically missed!")

    else:
        print(f"{attacker.name} missed.")

def special_attack(attacker, target):
    if attacker.special == "root_bind":
        damage = random.randint(10, 15)

        target.hp -= damage
        target.stunned = True
        print(f'{attacker.name} used Root Bind! {target.name} is stunned! ({damage} dmg)')

    elif attacker.special == "soul_burnt":
        damage = random.randint(35, 50)
        recoil = random.randint(8, 12)

        target.hp -= damage
        attacker.hp -= recoil
        print(f'{attacker.name} used Soul Burnt! {damage} dmg! ({recoil} recoil)')

    elif attacker.special == "retsunami":
        heal = random.randint(5, 10)

        attacker.hp = min(attacker.hp + heal, attacker.max_hp)
        print(f"{attacker.name} regenerates {heal} HP!")

    elif attacker.special == "earth_shield":
        heal = random.randint(5, 10)
        damage = random.randint(10, 13)

        attacker.hp = min(attacker.hp + heal, attacker.max_hp)
        target.hp -= damage

        print(f'{attacker.name} used Earth Shield! Healed {heal} hp! Dealt ({damage} dmg)')

def heal(character):
    heal_amount = random.randint(10, 20)

    before = character.hp
    character.hp = min(character.hp + heal_amount, character.max_hp)
    actual_heal = character.hp - before

    print(f"{character.name} healed {actual_heal} HP!")

def player_turn(player, enemy):
    print(f"{player.name} HP: {player.hp}/{player.max_hp}")
    print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")

    print("Choose your action:")
    print("1. Attack")
    print("2. Heal")

    choice = input("> ")

    if int(choice) == 1:
        attack(player, enemy)

    elif int(choice) == 2:
        heal(player)

    else:
        print("Invalid choice.")
        print("You lose your turn.")

def story(text):
    print("\n" + text)
    input("\n(Press Enter to continue...)")

def main():
    story("""🌲 Ancient Forest Temple

        Deep within the forest, Jason steps into a forgotten temple.
        The air is heavy. The seal carved into the stone is shattered.

        Roots begin to move.
        The ground trembles.

        Something has awakened."""
        )
    
    for i, current_enemy in enumerate(bosses, start=1):
        if i == 1:
            story(
                """⚔️ Jorvalkarith – The Demon Tree

                A massive creature rises from the earth.
                Its body is formed from roots, bark, and ancient hatred.

                It was the first guardian.
                Now, it is the first demon to fall."""
                )

        elif i == 2:
            story(
                """🌊 Ruined Coast

                The sea boils. Villages lie in ruins, swallowed by waves.

                From the depths emerges Balzeth — a massive demon of muscle and fury.

                The strongest demon, second only to the King."""
                )

        elif i == 3:
            story(
                """🔥 Burning Capital

                The sky burns red.
                The Demon King stands upon a throne of fire.

                "You broke the seal," he says, "Finally, I escaped from that jail."
                "But if you're against me, I don't mind burning your soul."

                This is the final battle."""
                )

        current_enemy.hp = current_enemy.max_hp
        print(f"\n⚔️ {current_enemy.name} emerges!")

        while player.hp > 0 and current_enemy.hp > 0:
            print("__________")

            if player.stunned:
                print("😵 You are stunned and lose your turn!")
                player.stunned = False\
                
            else:
                player_turn(player, current_enemy)

            if current_enemy.hp > 0:
                if current_enemy.special and random.random() < 0.25:
                    special_attack(current_enemy, player)

                else:
                    attack(current_enemy, player)

        if player.hp <= 0:
            print("\n💀 Jason has fallen. The world is doomed.")
            return

        print(f"\n✅ {current_enemy.name} was defeated!")

    story(
        """🌍 The Demon King has fallen.

        The flames fade.
        The demons return to the Underworld.

        Jason stands alone —
        the one who caused the disaster,
        and the one who ended it.

        The world is saved."""
        )

main()