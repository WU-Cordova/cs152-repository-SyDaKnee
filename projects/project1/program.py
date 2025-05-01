import random
from typing import List, TypeVar, Generic

T = TypeVar('T')

# I copied over the bag code I had implemented from the original assignment becuase I was having a hard time
# trying to access it outside of the project1 folder. I know there probably is a way to do it, I'm just not sure how
# to go about that in this current moment. I noticed the ibag file was using TypeVar and Generic to help define types,
# so I just copied that implementation over. At first, I had it implemented it so that the bag being accessed was only 
# directly storing Card objects, but I realized this was not the right way to go about things because the card decks 
# were essentially just lists of Card objects and did not feel faithful to the bag structure concept.

# https://www.w3schools.com/python/python_classes.asp -> I used this while I was implementing this code. 

class Bag(Generic[T]):

    def __init__(self):
        self.items = []

    def add(self, item: T):
        if item is None:
            raise TypeError("You cannot add nothing to the bag.")
        self.items.append(item)  
        
    def remove(self, item: T) -> None:
        self.items.remove(item)
        if item not in self.items:
            raise ValueError("You cannot remove this item, it isn't in the bag.") 
        
    def count(self, item: T) -> int:
        return self.items.count(item)

    def __len__(self) -> int:
        return len(self.items)  

    def distinct_items(self) -> int:
        distinct_items = set(self.items) 
        return distinct_items  

    def __contains__(self, item) -> bool:
        return item in self.items
    
    def clear(self) -> None:
        self.items.clear()

class Card:
    """Establishes playing cards with differing suits and ranks."""

    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

    def card_value(self):
        if self.rank in ['J', 'K', 'Q']:
            return 10
        return 11 if self.rank == 'A' else int(self.rank)
        
    def __str__(self) -> str:
        return f"[{self.rank}{self.suit}]" # Formats how the Card object is displayed when it's printed as a string. This took surprisingly long for me to figure out!

class MultiDeck:
    """Establishes multiple shuffled decks of cards."""

    def __init__(self, number_of_decks: int):
        self.bag = Bag()
        self.number_of_decks = number_of_decks
        self.create_deck()

    def create_deck(self):
        suits = ['♥', '♣', '♦', '♠']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for _ in range(self.number_of_decks): # Used a placeholder variable here because we are initializing multiple decks.
            for suit in suits:
                for rank in ranks:
                    self.bag.add(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.bag.items)

    def draw_card(self) -> Card:
        if len(self.bag) == 0:
            raise ValueError("There are no more cards in the deck!")
        return self.bag.items.pop() # Removes the card from the deck once it has been drawn.

class Game:
    """Handles Blackjack game logic."""
    # The hands are lists and not bags because I needed an easy way to directly index the dealer's hand so that only the first card is shown at the beginning of play.
    # I cannot index a bag like a list because order does not matter with bags. It's also more efficient to use a list when calculating the value of each hand because
    # I can utilize sum() instead of having to write out a function within the bag class for calculation. 

    def __init__(self):
        self.deck = MultiDeck(random.choice([2, 4, 6, 8]))
        self.player_hand = []
        self.dealer_hand = []

    def deal_first_cards(self): 
        self.player_hand = [self.deck.draw_card(), self.deck.draw_card()]
        self.dealer_hand = [self.deck.draw_card(), self.deck.draw_card()]

    def hand_value(self, hand: List[Card]) -> int:
        value = sum(card.card_value() for card in hand)
        number_of_aces = sum(1 for card in hand if card.rank == 'A')
        while value > 21 and number_of_aces:
            value -= 10
            number_of_aces -= 1
        return value
    
    def show_hands(self, show_dealer_hand: bool = False):
        print(f"Player's Hand: {' '.join(str(card) for card in self.player_hand)} | Score: {self.hand_value(self.player_hand)}")
        if show_dealer_hand:
            print(f"Dealer's Hand: {' '.join(str(card) for card in self.dealer_hand)} | Score: {self.hand_value(self.dealer_hand)}\n")
        else:
            print(f"Dealer's Hand: {self.dealer_hand[0]} [Hidden] | Score: {self.hand_value([self.dealer_hand[0]])}\n") # It's only displaying/reading the first card in the dealer's hand.

    def play(self):
        print("🃁 Welcome to Blackjack! 🂺\n")
        self.deal_first_cards()
        print("🃁 First Deal: 🂺\n")
        self.show_hands()

        player_score = self.hand_value(self.player_hand)

        if player_score == 21:
            print("🏆 Player has a Blackjack! Player Wins! 🏆")
            return

        while player_score < 21:
            turn_action = input("Would you like to (H)Hit or (S)Stay?").strip().upper()
            if turn_action == 'H':
                self.player_hand.append(self.deck.draw_card())
                player_score = self.hand_value(self.player_hand)
                print(f"Player Hand: {' '.join(str(card) for card in self.player_hand)} | Score: {player_score}\n")
            elif turn_action == 'S':
                break
            else:
                print("Please enter either 'H' or 'S'.")

        if player_score > 21:
            print("Bust! You went over 21! Dealer wins!")
            return
        
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.draw_card())
        self.show_hands(show_dealer_hand = True)
        dealer_score = self.hand_value(self.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            print("Player wins!")
        elif player_score < dealer_score:
            print("Dealer wins!")
        else:
            print("It's a tie!")

if __name__ == "__main__":
    while True:
        game = Game()
        game.play()
        if input("Would you like to play again? (Y)Yes or (N)No?").strip().upper() != 'Y':
            print("Thanks for playing!")
            break
        