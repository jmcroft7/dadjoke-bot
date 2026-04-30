import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()

TOKEN = os.getenv('Token1')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents, help_command=None)

    async def setup_hook(self):
        # Load cogs
        initial_extensions = ['cogs.general', 'cogs.exercise']
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f'Loaded extension {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return # Ignore unknown commands
        print(f'Error in command {ctx.command}: {error}')
        await ctx.send(f'An error occurred: {error}')

bot = MyBot()

@bot.command(name='help', aliases=['h'])
async def help_command(ctx):
    # Route !help to the custom help in General cog or just define it here
    general_cog = bot.get_cog('General')
    if general_cog:
        await general_cog.help_custom(ctx)
    else:
        await ctx.send("Help command is currently unavailable.")

if __name__ == '__main__':
    bot.run(TOKEN)