import pygame

# Initialize pygame before font operations inside components
pygame.init()

from Frame.stage_manager import StageManager, Stage
from Frame.scroll_engine import ScrollEngine
from Frame.game_state import GameState
from Entities.player import Player
from Entities.enemies import Enemy
from Cards.Cards import Card
from Cards.All_cards import get_reward_pool
from question_wave.question_controller import QuestionScreen
import random

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("SASEHacks Game")
clock = pygame.time.Clock()

# Setup
player = Player(x=200, y=300)
game_state = GameState(player)
scroll = ScrollEngine()
stage_manager = StageManager(game_state)
question_screen = QuestionScreen(screen, game_state, stage_manager)

# Fonts for temporary UI
font = pygame.font.SysFont(None, 48)

# Dummy state vars for placeholder screens
active_screen = "overworld"
overworld_timer = 0
overworld_duration = 3000
reward_timer = 0
reward_duration = 2000
battle_timer = 0
walk_timer = 0
walk_duration = 2000 # 2 seconds of walking
enemy = None
drawn_cards = []
card_rects = []
reward_cards = []
reward_rects = []
cards_picked = 0
battle_log_text = ""   # Feedback text shown during battle
log_timer = 0
enemy_stunned = False   # True = enemy skips next attack

# Callback functions
def start_overworld():
    global active_screen, battle_timer, enemy, overworld_timer
    active_screen = "overworld"
    scroll.start_scroll()
    battle_timer = pygame.time.get_ticks()
    overworld_timer = pygame.time.get_ticks()

def start_battle():
    global active_screen, enemy, drawn_cards, card_rects, battle_log_text
    active_screen = "battle"
    scroll.stop_scroll()
    enemy = Enemy("Slime", 100, 100, 10, x=600, y=300)
    battle_log_text = ""
    enemy_stunned = False
    
    # Reset effect state for new battle
    game_state.dodge_active = False
    game_state.poison_active = False
    game_state.poison_turns = 0
    game_state.charging_card = None
    
    # Draw up to 3 cards from deck
    deck_copy = game_state.cards_in_deck.copy()
    random.shuffle(deck_copy)
    drawn_cards = deck_copy[:3]
    
    # Recalculate card rects
    _recalc_card_rects()

def _recalc_card_rects():
    global card_rects
    card_rects = []
    total = len(drawn_cards)
    card_w, card_h = 140, 120
    gap = 10
    total_w = total * card_w + (total - 1) * gap
    start_x = (800 - total_w) // 2
    for i in range(total):
        rect = pygame.Rect(start_x + i * (card_w + gap), 450, card_w, card_h)
        card_rects.append(rect)

def start_post_battle_walk():
    global active_screen, walk_timer
    active_screen = "post_battle_walk"
    scroll.start_scroll()
    walk_timer = pygame.time.get_ticks()

def show_card_select():
    global active_screen
    active_screen = "card_select"

def start_questions():
    global active_screen
    active_screen = "question_wave"
    question_screen.start()

def show_card_reward():
    global active_screen, reward_timer, reward_cards, reward_rects, cards_picked
    active_screen = "card_reward"
    reward_timer = pygame.time.get_ticks()
    cards_picked = 0
    
    # Pull from real card pool
    reward_cards = get_reward_pool(3)
    
    reward_rects = []
    card_w, card_h = 140, 120
    gap = 10
    total_w = 3 * card_w + 2 * gap
    start_x = (800 - total_w) // 2
    for i in range(len(reward_cards)):
        rect = pygame.Rect(start_x + i * (card_w + gap), 250, card_w, card_h)
        reward_rects.append(rect)

def show_game_over():
    global active_screen
    active_screen = "game_over"

def next_stage():
    # just loop back to overworld for now
    stage_manager.transition_to(Stage.OVERWORLD)

stage_manager.register(Stage.OVERWORLD,     start_overworld)
stage_manager.register(Stage.BATTLE,        start_battle)
stage_manager.register(Stage.POST_BATTLE_WALK, start_post_battle_walk)
stage_manager.register(Stage.CARD_SELECT,   show_card_select)
stage_manager.register(Stage.QUESTION_WAVE, start_questions)
stage_manager.register(Stage.CARD_REWARD,   show_card_reward)
stage_manager.register(Stage.GAME_OVER,     show_game_over)
stage_manager.register(Stage.NEXT_STAGE,    next_stage)

# Initialization
stage_manager.transition_to(Stage.OVERWORLD)
stage_manager.check_conditions()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if active_screen == "question_wave":
            question_screen.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Battle card clicks
                if active_screen == "battle" and enemy and enemy.is_alive():
                    for i, rect in enumerate(card_rects):
                        if rect.collidepoint(event.pos):
                            card = drawn_cards[i]
                            
                            # --- HANDLE SPECIAL EFFECTS ---
                            if card.effect == "instakill":
                                enemy.hp = 0
                                battle_log_text = f"{card.name}! INSTAKILL!"
                                log_timer = pygame.time.get_ticks()
                                break
                            
                            if card.effect == "dodge":
                                game_state.dodge_active = True
                                battle_log_text = f"{card.name}! Dodge ready (50%)"
                                log_timer = pygame.time.get_ticks()
                                break
                            
                            if card.effect == "multi_hit":
                                # Water Barrage: fires Water Bubble 2-3 times
                                hits = random.randint(2, 3)
                                total_dmg = 0
                                for _ in range(hits):
                                    dmg = card.roll_damage()
                                    total_dmg += dmg
                                    if enemy:
                                        enemy.take_damage(dmg)
                                battle_log_text = f"{card.name} x{hits}! Total: {total_dmg} damage!"
                                log_timer = pygame.time.get_ticks()
                                break
                            
                            # --- NORMAL DAMAGE ---
                            damage = card.roll_damage()
                            enemy.take_damage(damage)
                            battle_log_text = f"{card.name} dealt {damage} damage!"
                            log_timer = pygame.time.get_ticks()
                            
                            # Poison check
                            if card.effect == "poison" and card.roll_effect():
                                game_state.poison_active = True
                                game_state.poison_turns = 3
                                battle_log_text += " POISONED!"
                            
                            # Stun check
                            if card.effect == "stun" and card.roll_effect():
                                enemy_stunned = True
                                battle_log_text += " STUNNED!"
                            
                            # Replace used card (only non-permanent ones cycle)
                            if not card.permanent:
                                drawn_cards.pop(i)
                                deck_copy = [c for c in game_state.cards_in_deck if c not in drawn_cards]
                                if deck_copy:
                                    random.shuffle(deck_copy)
                                    drawn_cards.insert(i, deck_copy[0])
                                _recalc_card_rects()
                            
                            break

                # Reward card clicks
                elif active_screen == "card_reward":
                    # Only allow clicks if they actually passed the wave
                    if question_screen.logic.result == "pass":
                        for i, rect in enumerate(reward_rects):
                            if rect.collidepoint(event.pos):
                                card = reward_cards[i]
                                # Add chosen card to deck
                                game_state.cards_in_deck.append(card)
                                cards_picked += 1
                                
                                # Remove clicked card from screen
                                reward_cards.pop(i)
                                reward_rects.pop(i)
                                
                                # Check if they picked 2 yet
                                if cards_picked >= 2:
                                    stage_manager.transition_to(Stage.GAME_OVER)
                                break

    # Update
    scroll.update()
    stage_manager.check_conditions()

    if active_screen == "question_wave":
        question_screen.update()
        
    if active_screen == "overworld":
        if pygame.time.get_ticks() - overworld_timer > overworld_duration:
            stage_manager.transition_to(Stage.BATTLE)
            
    if active_screen == "battle":
        if enemy and not enemy.is_alive():
            stage_manager.transition_to(Stage.POST_BATTLE_WALK)
            enemy = None
        else:
            # Tick poison damage on enemy
            if game_state.poison_active and game_state.poison_turns > 0 and enemy:
                pass  # Poison tracked via turns, applied per card click cycle
            
    if active_screen == "post_battle_walk":
        if pygame.time.get_ticks() - walk_timer > walk_duration:
            stage_manager.transition_to(Stage.QUESTION_WAVE)
            
    if active_screen == "card_reward":
        # If they failed, just use standard timer to skip reward screen
        if question_screen.logic.result == "fail":
            if pygame.time.get_ticks() - reward_timer > reward_duration:
                stage_manager.transition_to(Stage.GAME_OVER)

    # Draw
    screen.fill((0, 0, 0))

    if active_screen in ["overworld", "battle", "post_battle_walk"]:
        scroll.draw_background(screen)
        player.draw(screen)
        if active_screen == "battle" and enemy:
            enemy.draw(screen)
        

        if active_screen == "overworld":
            text = font.render(f"Overworld (Walking)", True, (255, 255, 255))
            screen.blit(text, (250, 50))
        elif active_screen == "battle":
            text = font.render(f"Battle! (Select a Card)", True, (255, 0, 0))
            screen.blit(text, (200, 50))
            
            # Battle log text
            if battle_log_text:
                log_surf = pygame.font.SysFont(None, 28).render(battle_log_text, True, (255, 255, 100))
                screen.blit(log_surf, (200, 90))
            
            # Draw Cards
            for i, card in enumerate(drawn_cards):
                if i < len(card_rects):
                    rect = card_rects[i]
                    
                    # Color by rarity
                    if card.rarity == "super_rare":
                        bg_color = (150, 50, 200)   # Purple
                    elif card.rarity == "rare":
                        bg_color = (180, 140, 50)    # Gold
                    elif card.rarity == "starter":
                        bg_color = (120, 120, 180)   # Blue-grey
                    else:
                        bg_color = (200, 200, 200)   # Grey
                    
                    pygame.draw.rect(screen, bg_color, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 3)
                    
                    # Card Name
                    name_text = pygame.font.SysFont(None, 22).render(card.name, True, (0, 0, 0))
                    screen.blit(name_text, (rect.x + 5, rect.y + 5))
                    
                    # Attack type
                    type_text = pygame.font.SysFont(None, 18).render(f"[{card.attack_type}]", True, (80, 80, 80))
                    screen.blit(type_text, (rect.x + 5, rect.y + 25))
                    
                    # Card Dmg
                    if card.damage_min == card.damage_max:
                        dmg_str = f"Dmg: {card.damage_min}"
                    elif card.damage_max == 0:
                        dmg_str = "No damage"
                    else:
                        dmg_str = f"Dmg: {card.damage_min}-{card.damage_max}"
                    dmg_text = pygame.font.SysFont(None, 18).render(dmg_str, True, (200, 0, 0))
                    screen.blit(dmg_text, (rect.x + 5, rect.y + 45))
                    
                    # Effect label
                    if card.effect:
                        eff_text = pygame.font.SysFont(None, 18).render(f"FX: {card.effect}", True, (0, 100, 200))
                        screen.blit(eff_text, (rect.x + 5, rect.y + 65))
                    
                    # Permanent badge
                    if card.permanent:
                        perm_text = pygame.font.SysFont(None, 16).render("PERM", True, (255, 255, 255))
                        screen.blit(perm_text, (rect.x + 100, rect.y + 100))
                
        elif active_screen == "post_battle_walk":
            text = font.render(f"Enemy Defeated! Walking...", True, (100, 255, 100))
            screen.blit(text, (200, 50))

    elif active_screen == "card_select":
        text = font.render(f"Card Select (Press SPACE)", True, (255, 255, 255))
        screen.blit(text, (200, 200))

    elif active_screen == "question_wave":
        question_screen.draw()

    elif active_screen == "card_reward":
        if question_screen.logic.result == "pass":
            text = font.render(f"Pick 2 Cards to Add to Your Deck!", True, (100, 255, 100))
            screen.blit(text, (100, 150))
            
            # Draw Reward Cards
            for i, card in enumerate(reward_cards):
                if i < len(reward_rects):
                    rect = reward_rects[i]
                    
                    if card.rarity == "super_rare":
                        bg_color = (150, 50, 200)    # Purple
                    elif card.rarity == "rare":
                        bg_color = (180, 140, 50)    # Gold
                    else:
                        bg_color = (50, 150, 50)     # Green
                    
                    pygame.draw.rect(screen, bg_color, rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 3)
                    
                    name_text = pygame.font.SysFont(None, 22).render(card.name, True, (255, 255, 255))
                    screen.blit(name_text, (rect.x + 5, rect.y + 5))
                    
                    type_text = pygame.font.SysFont(None, 18).render(f"[{card.attack_type}]", True, (200, 200, 200))
                    screen.blit(type_text, (rect.x + 5, rect.y + 25))
                    
                    if card.damage_min == card.damage_max:
                        dmg_str = f"Dmg: {card.damage_min}"
                    elif card.damage_max == 0:
                        dmg_str = "No damage"
                    else:
                        dmg_str = f"Dmg: {card.damage_min}-{card.damage_max}"
                    dmg_text = pygame.font.SysFont(None, 18).render(dmg_str, True, (200, 255, 200))
                    screen.blit(dmg_text, (rect.x + 5, rect.y + 45))
                    
                    if card.effect:
                        eff_text = pygame.font.SysFont(None, 18).render(f"FX: {card.effect}", True, (100, 200, 255))
                        screen.blit(eff_text, (rect.x + 5, rect.y + 65))
                    
                    if card.rarity == "super_rare":
                        badge = pygame.font.SysFont(None, 16).render("SUPER RARE", True, (255, 100, 255))
                        screen.blit(badge, (rect.x + 5, rect.y + 100))
                    elif card.rarity == "rare":
                        rare_text = pygame.font.SysFont(None, 16).render("RARE", True, (255, 215, 0))
                        screen.blit(rare_text, (rect.x + 100, rect.y + 100))
        else:
            # Failed wave, no reward
            text = font.render(f"No rewards this time...", True, (255, 100, 100))
            screen.blit(text, (200, 200))

    elif active_screen == "game_over":
        text = font.render(f"DONE", True, (0, 255, 0))
        screen.blit(text, (350, 200))
        sub_text = pygame.font.SysFont(None, 32).render(f"(Baseplate for future end screen)", True, (200, 200, 200))
        screen.blit(sub_text, (200, 260))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()