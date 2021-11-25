"""
/start
/reinquote - get a random Reinhardt quote
/reinpic - get a random Reinhardt picture
/reinstrat - get a random Reinhardt strategy
/development - learn about Reinhardts development
/meme - get a random meme
cats - cute cat photo
"""

import logging
import os
import random
import aiofiles

from aiogram import Bot, Dispatcher, executor, types


from meme import Memer
from utils import help_text, about_text, charge, barrier_field, rocket_hammer

API_TOKEN = os.environ['API_KEY']
REIN_URL = 'https://overwatch.fandom.com/wiki/Reinhardt'


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    logging.info(message.from_user)
    await message.reply("Crusader online.\nTo learn more about ReinFrogBot /help")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
  logging.info(message.from_user)
  await message.reply(help_text)


@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
  logging.info(message.from_user)
  with open('./data/rein/Reinhardt-portrait.png', 'rb') as photo:
    await message.reply_photo(photo, caption=about_text)


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
    await Memer.send_memes(bot, message.chat.id)


@dp.message_handler(commands=['reinpic'])
async def rein_pic(message: types.Message):
  path = ('./data/rein')
  files = os.listdir(path)
  random_photo = random.choice(files)
  logging.info(message.from_user)
  with open(f'./data/rein/{random_photo}', 'rb') as photo:
    await message.reply_photo(photo, caption='REIN')


@dp.message_handler(commands=['strats'])
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

@dp.message_handler(commands=['hammer'])
async def hammer(message: types.Message):
  async with aiofiles.open('./data/about_images/hammer.png', mode='rb') as photo:
    await message.reply_photo(photo, caption=rocket_hammer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
