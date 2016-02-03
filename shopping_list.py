import os

import redis
from slackbot.bot import respond_to

r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0, password=os.environ['REDIS_PASS'])
list_name = 'shopping_list'


@respond_to('show list')
def show_list(message):
    number_of_items = r.llen(list_name)
    if number_of_items > 0:
        message.reply("There is %s items on the list:" % number_of_items)
        for obj in r.lrange(list_name, 0, r.llen(list_name) + 1):
            message.send("* %s" % obj.decode('utf-8'))
    else:
        message.reply("List is empty")


@respond_to('add to list (.*)')
def add_to_list(message, item):
    r.rpush(list_name, str(item))
    message.reply("You've added %s to list" % item)


@respond_to('clear list')
def show_list(message):
    r.delete(list_name)
    message.reply("You've cleared the shopping list")
