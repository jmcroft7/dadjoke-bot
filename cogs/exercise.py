import discord
from discord.ext import commands
import data_manager

class Exercise(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        data_manager.maybe_reset_daily()

    @commands.command(name='add', aliases=['a'])
    async def add(self, ctx, *args):
        if not args:
            await ctx.send('Usage: !add <exercise> <amount> or !add <amount> (for pushups)')
            return
        
        exercise = 'pushups'
        amount = None
        
        for arg in args:
            if arg.isdigit():
                amount = int(arg)
            else:
                parsed = data_manager.parse_exercise(arg)
                if parsed:
                    exercise = parsed

        if amount is None:
            await ctx.send('Usage: !add <exercise> <amount> or !add <amount> (for pushups)')
            return

        data_manager.daily_totals[exercise] += amount
        data_manager.save_data()
        
        role = discord.utils.get(ctx.guild.roles, name='Pushin P')
        mention = role.mention if role else '@Pushin P'
        await ctx.send(f"{mention} Added {amount} {exercise} to the daily total!\nTotal for today: {data_manager.daily_totals[exercise]}.")

    @commands.command(name='total', aliases=['t'])
    async def total(self, ctx, exercise_name: str = None):
        if exercise_name:
            exercise = data_manager.parse_exercise(exercise_name)
            if not exercise:
                await ctx.send(f"Unknown exercise: {exercise_name}. Valid are: {', '.join(data_manager.EXERCISES)}")
                return
            await ctx.send(f'Total {exercise} for the day: {data_manager.daily_totals[exercise]}')
        else:
            lines = [f"Total {ex.capitalize()} for the day: {data_manager.daily_totals[ex]}" for ex in data_manager.EXERCISES]
            await ctx.send('**Daily Totals:**\n' + '\n'.join(lines))

    @commands.command(name='setTotal', aliases=['st'])
    async def set_total(self, ctx, *args):
        if len(args) < 2:
            await ctx.send('Usage: !setTotal <exercise> <amount>')
            return
        
        exercise = None
        amount = None
        
        for arg in args:
            if arg.isdigit():
                amount = int(arg)
            else:
                parsed = data_manager.parse_exercise(arg)
                if parsed:
                    exercise = parsed
        
        if exercise is None or amount is None:
            await ctx.send('Usage: !setTotal <exercise> <amount>')
            return
        
        data_manager.daily_totals[exercise] = amount
        data_manager.save_data()
        await ctx.send(f'Total for {exercise} set to {amount} for today.')

    @commands.command(name='setDone', aliases=['sd'])
    async def set_done(self, ctx, *args):
        if len(args) < 2:
            await ctx.send('Usage: !setDone <exercise> <amount>')
            return
            
        exercise = None
        amount = None
        
        for arg in args:
            if arg.isdigit():
                amount = int(arg)
            else:
                parsed = data_manager.parse_exercise(arg)
                if parsed:
                    exercise = parsed
                    
        if exercise is None or amount is None:
            await ctx.send('Usage: !setDone <exercise> <amount>')
            return
        
        name = ctx.author.display_name
        if name not in data_manager.users:
            today = str(data_manager.get_pst_date())
            data_manager.users[name] = {
                'exercises': {ex: {'lifetime': 0, 'current': 0} for ex in data_manager.EXERCISES},
                'last_active': None,
                'streak': 0,
                'started': today,
                'days_tracked': 0
            }
        
        user_ex_stats = data_manager.users[name]['exercises'][exercise]
        user_ex_stats['lifetime'] += amount - user_ex_stats['current']
        user_ex_stats['current'] = amount
        data_manager.save_data()
        await ctx.send(f"{name} set their current total for {exercise} to {amount}.")

    @commands.command(name='done', aliases=['d'])
    async def done(self, ctx, *args):
        name = ctx.author.display_name
        exercise = 'pushups'
        amount = 10

        if args:
            # check if first part is exercise
            parsed_ex = data_manager.parse_exercise(args[0])
            if parsed_ex:
                exercise = parsed_ex
                if len(args) > 1 and args[1].isdigit():
                    amount = int(args[1])
            # check if first part is amount
            elif args[0].isdigit():
                amount = int(args[0])
            else:
                await ctx.send('Usage: !done [exercise] [amount]')
                return

        if name not in data_manager.users:
            today = str(data_manager.get_pst_date())
            data_manager.users[name] = {
                'exercises': {ex: {'lifetime': 0, 'current': 0} for ex in data_manager.EXERCISES},
                'last_active': None,
                'streak': 0,
                'started': today,
                'days_tracked': 0
            }
        
        user_ex_stats = data_manager.users[name]['exercises'][exercise]
        user_ex_stats['lifetime'] += amount
        user_ex_stats['current'] += amount
        data_manager.save_data()
        await ctx.send(f"{name} has done {user_ex_stats['current']} {exercise} today!")

    @commands.command(name='progress', aliases=['p'])
    async def progress(self, ctx, exercise_name: str = 'pushups'):
        exercise = data_manager.parse_exercise(exercise_name)
        if not exercise:
            await ctx.send(f"Unknown exercise: {exercise_name}. Valid are: {', '.join(data_manager.EXERCISES)}")
            return

        if not data_manager.users:
            await ctx.send('No one has logged their exercises yet.')
        else:
            sorted_users = sorted(data_manager.users.items(), key=lambda item: item[1]['exercises'][exercise].get('current', 0), reverse=True)
            lines = [f"{user}: {stats['exercises'][exercise]['current']} / {data_manager.daily_totals[exercise]}" for user, stats in sorted_users if stats['exercises'][exercise]['current'] > 0]
            if not lines:
                await ctx.send(f"No one has logged any {exercise} today.")
                return
            await ctx.send(f'**{exercise.capitalize()} Progress:**\n' + '\n'.join(lines))

    @commands.command(name='myProgress', aliases=['mp'])
    async def my_progress(self, ctx):
        name = ctx.author.display_name
        if name not in data_manager.users:
            await ctx.send('You have not logged any exercises yet.')
        else:
            stats = data_manager.users[name]
            ex_lines = []
            for ex in data_manager.EXERCISES:
                ex_stats = stats['exercises'][ex]
                ex_lines.append(f"- {ex.capitalize()}: {ex_stats['current']} today, {ex_stats['lifetime']} lifetime")

            msg = (
                f"{name} Stats:\n"
                f"**Exercises:**\n" + '\n'.join(ex_lines) + "\n\n"
                f"**Overall:**\n"
                f"Started: {stats['started']}\n"
                f"Days Tracked: {stats['days_tracked']}\n"
                f"Streak: {stats['streak']} days\n"
            )
            await ctx.send(msg)

    @commands.command(name='lifetime', aliases=['l', 'lt'])
    async def lifetime(self, ctx, exercise_name: str = 'pushups'):
        exercise = data_manager.parse_exercise(exercise_name)
        if not exercise:
            await ctx.send(f"Unknown exercise: {exercise_name}. Valid are: {', '.join(data_manager.EXERCISES)}")
            return

        if not data_manager.users:
            await ctx.send('No user data available.')
        else:
            sorted_users = sorted(data_manager.users.items(), key=lambda item: item[1]['exercises'][exercise].get('lifetime', 0), reverse=True)
            top_10 = sorted_users[:10]
            leaderboard = [f"{i+1}. {user}: {stats['exercises'][exercise]['lifetime']}" for i, (user, stats) in enumerate(top_10) if stats['exercises'][exercise]['lifetime'] > 0]
            if not leaderboard:
                await ctx.send(f"No lifetime data for {exercise} yet.")
                return
            await ctx.send(f'**Top 10 for Total {exercise.capitalize()}:**\n' + '\n'.join(leaderboard))

async def setup(bot):
    await bot.add_cog(Exercise(bot))
