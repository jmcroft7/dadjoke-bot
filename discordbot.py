import discord
import os
import random
import requests
import json


# responses that the bot randomly cycles through
responses = ["Hello! I am a discord bot", "Hi I am NOT a discord bot", "I am real!"]


# class that represents the data recieved from the api, including its inputs.
class Joke:
    def __init__(self, id, contents):
        self.id = id
        self.contents = contents

# function that requests data from api


def get_quote():
    q = requests.get('https://icanhazdadjoke.com', headers={"Accept": "application/json"})
    words = q.json()
    endjoke = words['joke']
    return (endjoke)


# this is the bot
client = discord.Client()

# on statement for bot


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# commands for bot


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/response'):
        await message.channel.send(random.choice(responses))

    if message.content.startswith('/joke'):
        await message.channel.send(get_quote())


# this is what makes bot run
# token1 = .env or some secret file not displayed to public
client.run(os.getenv('Token1'))
