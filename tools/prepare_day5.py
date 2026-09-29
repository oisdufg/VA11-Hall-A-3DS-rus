"""Stage Day 5 controllers and story dependencies from the owner's game."""
from pathlib import Path
import argparse
from prepare_day4 import prepare

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('game',type=Path)
    parser.add_argument('decompiled',type=Path)
    args=parser.parse_args()
    prepare(args.game,args.decompiled,Path(__file__).resolve().parents[1],day=5)
