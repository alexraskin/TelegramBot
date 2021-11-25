import uuid
from replit import db
import random


# quote_list = []
# with open('./data/quotes.txt') as infile:
#   for quote in infile:
#     set_quote = db[uuid.uuid4()] = quote.strip()
keys = db.keys()

random_quote = random.choice(list(keys))

value = db[random_quote]
print(value)
