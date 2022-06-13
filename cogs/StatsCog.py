import discord
from discord.ext import commands
from discord.ext.commands import Context

class StatsCog(commands.Cog):

    def __init__(self, bot, **kwargs):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx: Context,members: commands.Greedy[discord.Member]):
        print('Recieved command !stats from ' + ctx.author.name + ', processing...')
        message = "\n".join([f"{member.id}: {member.name}" for member in members])
        await ctx.send(message)

