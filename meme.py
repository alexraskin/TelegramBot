import logging
import os
from urllib.error import HTTPError

import aiohttp
import wget
from aiogram import exceptions

logging.basicConfig(level=logging.INFO)


MEMES_TO_SAVE_PATH = 'data/memes'

class Memer:
    async def get_random_meme(self):
        self._clear_dir()
        async with aiohttp.ClientSession() as session:

            meme_url = 'https://meme-api.herokuapp.com/gimme'
            async with session.get(meme_url) as meme_response:
                meme_json = await meme_response.json()

        filename = meme_json['url'].split("/")[-1]
        filename = os.path.join(MEMES_TO_SAVE_PATH, filename)
        wget.download(meme_json['url'], filename)
        meme_img = open(filename, 'rb')
        file_ext = filename.split('.')[-1]
        return meme_img, file_ext

    def _clear_dir(self):
        for file in os.listdir(MEMES_TO_SAVE_PATH):
            try:
                os.remove(os.path.join(MEMES_TO_SAVE_PATH, file))
            except PermissionError:
                pass
    
    @staticmethod
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