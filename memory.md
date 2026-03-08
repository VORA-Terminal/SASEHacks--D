# Memory — Arcade Machine Image Integration

## Context
- The app has been merged: everything now runs via `flashcard_app.py` (PyQt6 desktop) and `Game files/` folder.
- **Do NOT attempt browser verification** — this is a desktop app.

## Key Files
| File | Purpose |
|------|---------|
| `flashcard_app.py` | Main PyQt6 app (698 lines) |
| `arcadeMachine.png` | New arcade cabinet image (677×369 px), in project root |
| `Game files/` | Game logic folder (Cards, Entities, Frame, question_wave) |

## Findings

### Current Image Setup (flashcard_app.py)
- **Line 203**: References `arcade-bg.png` (old web image, no longer correct)
- **Line 204**: Loads as `QPixmap`, displayed via `QLabel` with `setScaledContents(True)`
- **Lines 250-257** (`resizeEvent`): Background scales to full window; CRT screen positioned at:
  - `x = 34% of width, y = 35.5% of height`
  - `w = 32% of width, h = 35% of height`

### New Image: `arcadeMachine.png`
- Dimensions: **677 × 369 px** (~1.83:1 aspect ratio)
- This is a pixel-art arcade cabinet with a white/empty screen area
- The screen area sits roughly in the **center-upper** portion of the cabinet

### Screen Area Estimation (from the image)
Looking at the 677×369 image:
- Screen left edge ≈ x=228 → **33.7%** of width
- Screen right edge ≈ x=450 → **66.5%** of width → screen width ≈ **32.8%**
- Screen top edge ≈ y=52 → **14.1%** of height
- Screen bottom edge ≈ y=213 → **57.7%** of height → screen height ≈ **43.6%**

## Plan
1. ~~Change `arcade-bg.png` → `arcadeMachine.png` on line 203~~ ✅ Done
2. ~~Adjust CRT screen position in `resizeEvent` to match the new image's screen area~~ ✅ Done
3. ~~Keep aspect ratio of the background image to avoid distortion~~ ✅ Done (rewrote resizeEvent)
4. Test positioning values iteratively — **user needs to verify visually**

## Changes Made to `flashcard_app.py`
- **Line 203**: `arcade-bg.png` → `arcadeMachine.png`
- **Lines 247-280** (`resizeEvent`): Rewrote to:
  - Preserve aspect ratio of background image (no more stretching)
  - Center the image in the window
  - Position CRT screen **relative to the image placement**, not the window
  - Screen area percentages: `x=33.7%, y=14.1%, w=32.8%, h=43.6%`

## Status
- [x] Implementation complete
- [ ] User needs to visually verify CRT screen alignment — percentages may need tweaking

