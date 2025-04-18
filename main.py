import sys
from pathlib import Path

base_path = Path(__file__).parent.absolute()
sys.path.append(str(base_path / "classes"))

from game import Game

if __name__ == '__main__':
    Game(850, 550).main()
