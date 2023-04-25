import bot
import telegram_1
import threading
import time

if __name__ == '__main__':
    try:
        # bot.run_discord_bot()
        # x = threading.Thread(target=telegram_1.start_bot)
        y = threading.Thread(target=bot.run_discord_bot)
        # y.start()
        y.start()
        telegram_1.start_bot()
        while True:
            time.sleep(5)
            print("Test")
    except Exception as e:
        print("Exception - main - " + str(e))
