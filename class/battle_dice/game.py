import random
from character import Character

class Game:

    def __init__(self, player1: Character, player2: Character):
        self.__player1 = player1
        self.__player2 = player2

    def attack(self, attacker: Character, defender: Character):
        dice_roll = random.randint(1, 6)
        damage_dealt = dice_roll * attacker.attack_power
        defender.health -= damage_dealt 

        print(f"{attacker.name} has rolled a {dice_roll}! They deal {damage_dealt} to the {defender.name}!")
    
    def start_battle(self):
        print(f"The battle has begun! {self.__player1.name} and {self.__player2.name} are battling it out!")

        attacker, defender = self.__player1, self.__player2
        
        while self.__player1.health > 0 and self.__player2.health > 0:
            self.attack(attacker, defender)

            if defender.health <= 0:
                print(f"{defender.name} has been defeated!")
                break

            attacker, defender = defender, attacker # Makes the attacker and defender roles take turns. 
