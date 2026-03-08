import random

class Card:
    def __init__(self, name, damage_min, damage_max, description="",
                 attack_type="physical", effect=None, effect_chance=0.0,
                 rarity="common", permanent=False, charge_turns=0):
        self.name = name
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.description = description
        self.attack_type = attack_type      # "physical", "ranged", "defensive", "special"
        self.effect = effect                # None, "poison", "dodge", "charge", "instakill"
        self.effect_chance = effect_chance   # 0.0 to 1.0
        self.rarity = rarity                # "starter", "common", "rare"
        self.permanent = permanent          # True = cannot be replaced/discarded
        self.charge_turns = charge_turns    # 0 = instant, >0 = takes that many turns to charge
        
        # Runtime state
        self.charging = False
        self.charge_remaining = 0
        
    def roll_damage(self):
        if self.damage_min == self.damage_max:
            return self.damage_min  # flat damage
        return random.randint(self.damage_min, self.damage_max)
    
    def roll_effect(self):
        """Returns True if the card's special effect triggers."""
        if self.effect and self.effect_chance > 0:
            return random.random() < self.effect_chance
        return False
    
    def start_charge(self):
        """Begin charging this card. Returns turns remaining."""
        self.charging = True
        self.charge_remaining = self.charge_turns
        return self.charge_remaining
    
    def tick_charge(self):
        """Tick down one charge turn. Returns True when ready to fire."""
        if self.charging:
            self.charge_remaining -= 1
            if self.charge_remaining <= 0:
                self.charging = False
                return True
        return False
    
    def reset(self):
        """Reset runtime state."""
        self.charging = False
        self.charge_remaining = 0