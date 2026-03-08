from Cards.All_cards import get_starter_pair

class GameState:
    def __init__(self, player):
        self.player = player
        self.monsters_defeated = 0
        self.damage_multiplier = 1.0
        # Randomized starter cards (permanent)
        self.cards_in_deck = get_starter_pair()
        self.cards_in_hand = []
        
        # Battle effect state
        self.dodge_active = False       # True = 50% chance to dodge next enemy attack
        self.poison_active = False      # True = enemy takes poison dmg each turn
        self.poison_turns = 0           # Turns remaining for poison
        self.poison_damage = 5          # Damage per poison tick
        self.charging_card = None       # Card currently charging
