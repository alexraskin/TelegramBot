"""
/start
/reinquote - get a random Reinhardt quote
/reinpic - get a random Reinhardt picture
/meme - get a random meme
/reinstrat - get a random Reinhardt Strategy
/development - learn about Reinhardts Development
cats - cute cat photo
"""

import logging
import os
import random

from aiogram import Bot, Dispatcher, executor, types

from utils import send_memes

API_TOKEN = os.environ['API_KEY']
REIN_URL = 'https://overwatch.fandom.com/wiki/Reinhardt'


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    logging.info(message.from_user)
    await message.reply("Crusader online.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('./data/cats.jpg', 'rb') as photo:
      logging.info(message.from_user)
      await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler(commands=['reinquote'])
async def random_rein_quotes(message: types.Message):
  quote_list = []
  with open('./data/quotes.txt', 'r') as quotes:
    for quote in quotes:
      quote_list.append(quote)
  random_quote = random.choice(list(quote_list))
  logging.info(message.from_user)
  await message.reply(random_quote)
      

@dp.message_handler(commands=['meme'])
async def send_meme_handler(message):
    logging.info(message.from_user)
    await send_memes(bot, message.chat.id)


@dp.message_handler(commands=['reinpic'])
async def rein_pic(message: types.Message):
  path = ('./data/rein')
  files = os.listdir(path)
  random_photo = random.choice(files)
  logging.info(message.from_user)
  with open(f'./data/rein/{random_photo}', 'rb') as photo:
    await message.reply_photo(photo, caption='REIN')


@dp.message_handler(commands=['strat'])
async def rein_strategy(message: types.Message):
  with open('./data/strategy.txt', 'r') as strats:
    strat_list = []
    for strat in strats:
      strat_list.append(strat)
  random_strat = random.choice(list(strat_list))
  logging.info(message.from_user)
  await message.answer(random_strat)


@dp.message_handler(commands=['story'])
async def rein_story(message: types.Message):
  with open('./data/story.txt', 'r') as story:
    logging.info(message.from_user)
    for stories in story:
      await message.answer(stories)


@dp.message_handler(commands=['development'])
async def rein_development(message: types.Message):
  with open('./data/development.txt', 'r') as development_file:
    text = development_file.readlines()
    logging.info(message.from_user)
    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
