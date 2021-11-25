import logging
from urllib.error import HTTPError

from aiogram import exceptions

from meme import Memer

logging.basicConfig(level=logging.INFO)

about_text = """/start
/reinquote - get a random Reinhardt quote
/reinpic - get a random Reinhardt picture
/reinstrat - get a random Reinhardt Strategy
/development - learn about Reinhardts Development
/meme - get a random meme
cats - cute cat photo
"""

async def send_memes(bot_to_run, chat_id):
    success_sent = False
    count_tries = 0
    while not success_sent and count_tries < 5:
        try:
            meme, meme_ext = await Memer().get_random_meme()
            if meme_ext.lower() == 'gif':
                await bot_to_run.send_document(chat_id, meme)
            else:
                await bot_to_run.send_photo(chat_id, meme)
            success_sent = True
        except exceptions.TelegramAPIError as exc:
            logging.error(f'API Error chat_id={chat_id}: {exc}')
            count_tries += 1
        except HTTPError as exc:
            logging.error(f'HTTP Error on chat_id={chat_id}: {exc}')

