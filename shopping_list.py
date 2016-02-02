import os

import redis
from slackbot.bot import respond_to

r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0, password=os.environ['REDIS_PASS'])
list_name = 'shopping_list'


@respond_to('show list')
def show_list(message):
    message.reply("There is %s items on the list:" % r.llen(list_name))
    for obj in r.get(list_name):
        message.reply("* %s" % obj)


@respond_to('add to list (.*)')
def add_to_list(message, item):
    r.rpush(list_name, item)
    message.reply("You've added %s to list" % item)


@respond_to('clear list')
def show_list(message):
    r.delete(list_name)
    message.reply("You've cleared the shopping list")
