"""
/start
/help
/about
/reinquote - random Reinhardt quote
/reinpic - random Reinhardt picture
/reinstrat - random Reinhardt strategy
/development - Reinhardts development story
/hammer
/shield
/charge
/meme
"""

import logging
import os
import random

import aiofiles
from aiogram import Bot, Dispatcher, executor, types

from meme import Memer
from utils import about_text, shield, charge, help_text, rocket_hammer, fire_strike

API_TOKEN = os.environ['API_KEY']
REIN_URL = 'https://overwatch.fandom.com/wiki/Reinhardt'


logging.basicConfig(
  filename='log.txt',
  encoding='utf-8',
  level=logging.INFO
)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
  logging.info(message.from_user)
  await message.reply("Crusader online.\nTo learn more about Reinhardt /help")


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
  logging.info(message.from_user)
  await message.reply(help_text)


@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
  async with aiofiles.open('./data/rein/Reinhardt-portrait.png', 'rb') as photo:
    logging.info(message.from_user)
    await message.reply_photo(photo, caption=about_text)


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    async with aiofiles.open('./data/cats.jpg', 'rb') as photo:
      logging.info(message.from_user)
      await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler(commands=['reinquote'])
async def random_rein_quotes(message: types.Message):
  quote_list = []
  async with aiofiles.open('./data/quotes.txt', 'r') as quotes:
    async for quote in quotes:
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
  async with aiofiles.open(f'./data/rein/{random_photo}', 'rb') as photo:
    await message.reply_photo(photo, caption='REIN')


@dp.message_handler(commands=['strats', 'reinstrat'])
async def rein_strategy(message: types.Message):
  async with aiofiles.open('./data/strategy.txt', 'r') as strats:
    strat_list = []
    async for strat in strats:
      strat_list.append(strat)
  random_strat = random.choice(list(strat_list))
  logging.info(message.from_user)
  await message.answer(random_strat)


@dp.message_handler(commands=['story'])
async def rein_story(message: types.Message):
  async with aiofiles.open('./data/story.txt', 'r') as story:
    logging.info(message.from_user)
    async for stories in story:
      await message.answer(stories)


@dp.message_handler(commands=['development'])
async def rein_development(message: types.Message):
  async with aiofiles.open('./data/development.txt', 'r') as development_file:
    text = development_file.readlines()
    logging.info(message.from_user)
    await message.answer(text)


@dp.message_handler(commands=['hammer', 'rockethammer'])
async def hammer(message: types.Message):
  async with aiofiles.open('./data/about_images/rocket-hammer.jpg', mode='rb') as photo:
    await message.reply_photo(photo, caption=rocket_hammer)


@dp.message_handler(commands=['barrier', 'shield'])
async def barrier_field(message: types.Message):
  async with aiofiles.open('./data/about_images/shield.jpg', mode='rb') as photo:
    await message.reply_photo(photo, caption=shield)


@dp.message_handler(commands=['charge', 'shift'])
async def about_charge(message: types.Message):
  async with aiofiles.open('./data/about_images/charge.jpg', mode='rb') as photo:
    await message.reply_photo(photo, caption=charge)


@dp.message_handler(commands=['firestrike'])
async def send_fire_strike(message: types.Message):
  await message.reply(fire_strike)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
