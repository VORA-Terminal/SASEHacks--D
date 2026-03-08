# Memory

## Project Overview
- **Type:** Pygame game (SASEHacks hackathon project)
- **Theme:** Gator character fighting enemies using cards, answering flashcard questions
- **Workspace:** `c:\Users\jor26\OneDrive\Documents\GitHub\SASEHacks--D\Game files\`

## Game Flow
`Overworld (3s walk) -> Battle (card combat) -> Post-Battle Walk (2s) -> Question Wave (interactive) -> Card Reward (pick 2/3 if >60%) -> DONE screen`

## Key Files
| File | Purpose |
|------|---------|
| `main.py` | Main game loop, stage routing, event handling |
| `Frame/stage_manager.py` | Stage enum + StageManager class |
| `Frame/scroll_engine.py` | Background scrolling |
| `Frame/game_state.py` | Player deck, damage multiplier, global state |
| `Frame/core.py` | BattleLogic class (turn resolution, win/loss) |
| `Entities/player.py` | Player class (rect placeholder) |
| `Entities/enemies.py` | Enemy class (rect placeholder) |
| `Cards/Cards.py` | Card class (name, dmg, type, effect, rarity, permanent, charge) |
| `Cards/All_cards.py` | Full card registry, starter pairs, reward pool helpers |
| `question_wave/question_controller.py` | QuestionScreen orchestrator |
| `question_wave/question_logic.py` | Score tracking, pass/fail (>60%) |
| `question_wave/question_renderer.py` | Draws questions/choices |
| `question_wave/question_generator.py` | Generates dummy questions |
| `question_wave/question_events.py` | Mouse/keyboard input for questions |

## Important Decisions
- UI/sprites are **placeholders only** — user will replace later
- Player starts with exactly **2 starter cards** (permanent, cannot be replaced)
- Starter cards are randomized between 2 variants at game start
- Question pass threshold: **> 60%**
- Card reward: pick **2 out of 3** on pass
- Failed wave: no reward, brief pause, then DONE screen
- `pygame` must be imported in `question_controller.py` (was missing, caused crash)

## Card System (Latest)
### Starter Cards (permanent, randomized at start)
- Sand Throw OR Rock Throw — 15 flat damage
- Stick Poke OR Eye Poke — 10 flat damage

### Reward/Obtainable Cards
| Card | Type | Damage | Special | Rarity |
|------|------|--------|---------|--------|
| Tail Whip | Physical | 10-35 | — | Common |
| Gator Bite | Physical | 10-25 | — | Common |
| Scratch | Physical | 10-20 | — | Common |
| Snot Bubble | Ranged | 10-20 | 30% poison | Common |
| Water Bubble | Ranged | 10-25 | — | Common |
| Barrel Roll | Defensive | 0 | 50% dodge | Common |
| Water Barrage | Ranged | 10-25 x2-3 | Multi-hit (fires 2-3 times) | Rare |
| Death Roll | Physical | 35-55 | — | Rare |
| Super Whip | Physical | 35-45 | 50% stun | Rare |
| Chud Attack | Special | Instakill | Instakill | Super Rare (1%) |

### Rarity Tiers
| Tier | Spawn Rate | Card Color |
|------|-----------|------------|
| Common | 60% | Grey |
| Rare | 30% | Gold |
| Super Rare | 10% | Purple |
| Starter | N/A (permanent) | Blue-grey |

## Bugs Fixed
- `All-cards.py` was renamed to `All_cards.py` — Python can't import filenames with hyphens
- Effects: poison (30% chance, 5 dmg/turn for 3 turns), dodge (50% miss), stun (50% chance on Super Whip), multi_hit (Water Barrage fires 2-3x), instakill (Chud Attack)
