from slackbot.bot import respond_to

@respond_to('show list')
def show_list(message):
    message.reply("Show list")


