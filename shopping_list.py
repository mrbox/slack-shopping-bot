import os
import random

import redis
from slackbot.bot import respond_to

r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=0, password=os.environ['REDIS_PASS'])
list_name = 'shopping_list'


catchall_responses = """Ask about your neighbors, then buy the house.
Don't live in a town where there are no doctors.
If God lived on earth, people would break his windows.
If the rich could hire the poor to die for them, the poor would make a very nice living.
He has more in his head than in his pocket.
Rejoice not at thine enemy's fall - but don't rush to pick him up either.
Worries go down better with soup than without.
You can't sit on two horses with one behind.
They are both in love: he with himself and she with herself.
With horses you check the teeth; with a human you check the brains.
The hat is fine but the head is too small.
He's meditating on whether a flea has a belly-button.
Thieves and lovers like the dark
All is not butter that comes from a cow.
If he were twice as smart, he'd be an idiot!
If a girl can't dance, she says the musicians can't play.
Dress up a broom and it will look nice too.
Even a bear can be taught to dance.
Don't give me the honey and spare me the sting.
A black hen can lay a white egg.
Man plans and God laughs.
If you sleep with dogs, you get up with fleas.
A bird that you set free may be caught again, but a word that escapes your lips will not return.
A mother understands what a child does not say.
A pessimist, confronted with two bad choices, chooses both.
As he thinks in his heart, so he is.
As you teach, you learn.
Do not be wise in words - be wise in deeds.
Don't be sweet, lest you be eaten up; don't be bitter, lest you be spewed out.
Don't look for more honor than your learning merits.
First mend yourself, and then mend others.
He that can't endure the bad, will not live to see the good.
If charity cost nothing, the world would be full of philanthropists.
If not for fear, sin would be sweet.
Make sure to be in with your equals if you're going to fall out with your superiors.
Not to have felt pain is not to have been human.
What you don't see with your eyes, don't invent with your mouth.
Anytime a person goes into a delicatessen and orders a pastrami on white bread, somewhere a Jew dies. - Milton Berle
Jesus was a Jew, yes, but only on his mother's side. - Archie Bunker
America is a place where Jewish merchants sell Zen love beads to agnostics for Christmas. - John Burton""".split('\n')


@respond_to('(show list)|(show)')
def show_list(message, matched):
    number_of_items = r.llen(list_name)
    if number_of_items > 0:
        message.reply("There is %s items on the list:" % number_of_items)
        for idx, obj in enumerate(r.lrange(list_name, 0, r.llen(list_name) + 1), 1):
            message.send("%s %s" % (idx, obj.decode('utf-8')))
    else:
        message.reply("List is empty")


@respond_to('(add)|(add to list) (.*)')
def add_to_list(message, matched, item):
    r.rpush(list_name, str(item))
    message.reply("You've added %s to list" % item)


@respond_to('(clear)|(clear list)')
def show_list(message, matched):
    r.delete(list_name)
    message.reply("You've cleared the shopping list")


@respond_to('remove (\d+)')
def remove_item(message, item_index):
    item = r.lindex(list_name, item_index)
    r.lrem(list_name, 0, item)
    message.reply("You've removed %s from the shopping list" % item)


@respond_to('(.*)')
def catchall(message, text):
    message.reply(random.choice(catchall_responses))
