from argparse import ArgumentParser

from smallcarbot.smallcarbot import SmallCarBot

import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--on_board", nargs="?", const=True, default=False)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    bot = SmallCarBot(args.on_board)

    bot.run()


if __name__ == "__main__":
    main()
