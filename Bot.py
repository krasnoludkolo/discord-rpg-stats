import asyncio
import os

from discord.ext import commands

from cogs.RabbinCog import RabbinCog
from cogs.StatsCog import StatsCog


async def run():
    bot = Bot()
    await bot.start(os.environ.get('DISCORD_TOKEN'))


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!'
        )
        self.add_cog(RabbinCog(self))
        self.add_cog(StatsCog(self))

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
