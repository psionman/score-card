import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src", "score_card"))

from src.score_card.app import ScoreCard


if __name__ == "__main__":
    ScoreCard().run()
