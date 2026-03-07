import json
import os
import random

QUESTIONS_PER_WAVE = 10

class QuestionGenerator:
    def __init__(self, flashcard_dir="FlashcardUploads"):
        self.flashcard_dir = flashcard_dir
        self.all_cards = []
        self.load_all_flashcards()

    def load_all_flashcards(self):
        """Loads every JSON file in FlashcardUploads into one pool"""
        for filename in os.listdir(self.flashcard_dir):
            if filename.endswith(".json"):
                path = os.path.join(self.flashcard_dir, filename)
                with open(path, "r") as f:
                    cards = json.load(f)
                    self.all_cards.extend(cards)

    def generate_wave(self):
        """
        Returns a list of 10 question dicts, mixed between
        multiple choice and free response.
        Format:
        {
            "type": "multiple_choice" or "free_response",
            "term": "...",
            "answer": "...",
            "choices": ["...", "...", "...", "..."]  # only for multiple_choice
        }
        """
        if len(self.all_cards) < QUESTIONS_PER_WAVE:
            pool = self.all_cards * (QUESTIONS_PER_WAVE // len(self.all_cards) + 1)
        else:
            pool = self.all_cards.copy()

        selected = random.sample(pool, QUESTIONS_PER_WAVE)
        questions = []

        for i, card in enumerate(selected):
            # Alternate between types, randomize for variety
            q_type = "multiple_choice" if i % 2 == 0 else "free_response"

            q = {
                "type": q_type,
                "term": card["term"],
                "answer": card["answer"]
            }

            if q_type == "multiple_choice":
                # Build 3 wrong answers from other cards
                wrong_pool = [c["answer"] for c in self.all_cards if c["answer"] != card["answer"]]
                wrong_answers = random.sample(wrong_pool, min(3, len(wrong_pool)))
                choices = wrong_answers + [card["answer"]]
                random.shuffle(choices)
                q["choices"] = choices

            questions.append(q)

        return questions