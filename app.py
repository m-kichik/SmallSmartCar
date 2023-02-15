from smallcarbot.smallcarbot import SmallCarBot

import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    from smallcarbot.utils.image_processing import detect
    detect('bus.jpg')
    bot = SmallCarBot()
    bot.run()

if __name__ == "__main__":
    main()
