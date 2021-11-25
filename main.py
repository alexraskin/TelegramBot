import os
import logging
import random
from urllib.error import HTTPError
from aiogram import Bot, Dispatcher, executor, types, exceptions

from meme import Memer

API_TOKEN = os.environ['API_KEY']


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Crusader online.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('./data/cats.jpg', 'rb') as photo:
      await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler(commands=['reinquote'])
async def random_rein_quotes(message: types.Message):
  quote_list = []
  with open('./data/quotes.txt', 'r') as quotes:
    for quote in quotes:
      quote_list.append(quote)
  random_quote = random.choice(list(quote_list))
  await message.reply(random_quote)
      

@dp.message_handler(commands=['meme'])
async def send_meme_handler(message):
    await send_memes(bot, message.chat.id)


@dp.message_handler(commands=['reinpic'])
async def rein_pic(message: types.Message):
  path = ('./data/rein')
  files = os.listdir(path)
  random_photo = random.choice(files)
  with open(f'./data/rein/{random_photo}', 'rb') as photo:
    await message.reply_photo(photo, caption='REIN')

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



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)