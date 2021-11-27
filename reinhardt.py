import logging
import os
from urllib.error import HTTPError

import aiohttp
import wget
from aiogram import exceptions

logging.basicConfig(level=logging.INFO)


class ReinhardtBot:
    def __init__(self):
        pass

    async def make_request(
        self,
        url: str,
        path: str,
    ):
        self._clear_dir(path)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                _json = await response.json()
        if url.endswith('random'):
            download = _json['message']
            filename = _json['message'].split("/")[-1]
        elif url.endswith('gimme'):
            download = _json['url']
            filename = _json['url'].split("/")[-1]
        filename = os.path.join(path, filename)
        wget.download(download, filename)
        _img = open(filename, 'rb')
        file_ext = filename.split('.')[-1]
        return _img, file_ext

    def _clear_dir(
        self,
        path: str,
    ) -> None:
        for file in os.listdir(path):
            try:
                os.remove(os.path.join(path, file))
            except PermissionError as e:
                logging.error(f'{e}')
                pass

    @staticmethod
    async def send_photo(bot_to_run, chat_id, meme=False, dog=False):
        if meme == True:
            url = 'https://meme-api.herokuapp.com/gimme'
            path = 'data/memes'
        elif dog == True:
            url = 'https://dog.ceo/api/breeds/image/random'
            path = 'data/dogs'
        else:
            return
        success_sent = False
        count_tries = 0
        while not success_sent and count_tries < 5:
            try:
                file, file_ext = await ReinhardtBot().make_request(url, path)
                if file_ext.lower() == 'gif':
                    await bot_to_run.send_document(chat_id, file)
                else:
                    await bot_to_run.send_photo(chat_id, file)
                success_sent = True
            except exceptions.TelegramAPIError as exc:
                logging.error(f'API Error chat_id={chat_id}: {exc}')
                count_tries += 1
            except HTTPError as exc:
                logging.error(f'HTTP Error on chat_id={chat_id}: {exc}')
