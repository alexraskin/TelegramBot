import aiohttp
import wget
import os

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
