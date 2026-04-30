import discord
import random
from discord.ext import commands
from jokes import get_quote

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = ["Poop you buddy!", "POOP you!", "POOP YOU!", "I am a liberal", "I am a communist"]

    @commands.command(name='gooby', aliases=['g'])
    async def gooby(self, ctx):
        await ctx.send(random.choice(self.responses))

    @commands.command(name='joke', aliases=['j'])
    async def joke(self, ctx):
        await ctx.send(await get_quote())

    @commands.command(name='help_custom') # Named help_custom to avoid conflict with default help
    async def help_custom(self, ctx):
        help_text = """
```
Gooby Bot Commands:
!gooby (!g), !joke (!j), !help (!h)

Exercise Tracking:
(exercise: pushups, pullups, squats, crunches)

Goals:
!add/!a <ex> <amt>   - Add to daily goal.
!total/!t [ex]       - Show daily goal(s).
!setTotal/!st <ex> <amt> - Set daily goal.

Personal Logging:
!done/!d [ex] [amt]  - Log exercises (defaults to 10 pushups).
!setDone/!sd <ex> <amt> - Set your daily count.

Stats:
!progress/!p [ex]    - Show today's progress (default pushups).
!myProgress/!mp      - Show all your stats.
!lifetime/!l [ex]    - Show lifetime leaderboard (default pushups).
```
"""
        await ctx.send(help_text)

async def setup(bot):
    await bot.add_cog(General(bot))
