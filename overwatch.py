import logging
from urllib.error import HTTPError

import aiohttp
from aiogram import exceptions


class OverwatchAPI:
    def __init__(self):
        # https://ow-api.com/v1/stats/:platform/:region/:battletag/profile
        # https://ow-api.com/v1/stats/pc/us/cats-11481/profile
        self.base_url = 'https://ow-api.com/v1/stats'
        self.logger = logging.basicConfig(level=logging.INFO)

    async def _make_request(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                _json = await response.json()
                return _json

    async def get_overwatch_proifle(self, bot_to_run: str, chat_id: str,
                                    platform: str, region: str, tag: str):

        url = f"{self.base_url}/{platform}/{region}/{tag.replace('#', '-')}/profile"
        success_sent = False
        count_tries = 0
        while not success_sent and count_tries < 5:
            try:
                data = await OverwatchAPI()._make_request(url)
                if data:
                    _dict = {
                        'competitiveStats': data['rating'],
                    }
                await bot_to_run.send_message(chat_id, _dict)
                success_sent = True
            except exceptions.TelegramAPIError as exc:
                self.logger.error(f'API Error chat_id={chat_id}: {exc}')
                count_tries += 1
            except HTTPError as exc:
                self.logger.error(f'HTTP Error on chat_id={chat_id}: {exc}')
