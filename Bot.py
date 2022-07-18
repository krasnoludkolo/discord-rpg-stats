import asyncio
import os

from discord.ext import commands

from cogs.abstract_cog import AbstractCog
from cogs.activity_cog import ActivityCog
from cogs.rabbin_cog import RabbinCog
from cogs.stats_cog import StatsCog


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


async def run():
    bot = Bot()
    await bot.start(os.environ.get('DISCORD_TOKEN'))


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!'
        )
        self.add_cog(RabbinCog(self))
        # self.add_cog(StatsCog(self))
        self.add_cog(ActivityCog(self))
        self.add_cog(AbstractCog(self))

    async def on_ready(self):
        print(f'Logged in as {self.user.name} id={self.user.id}')


if __name__ == '__main__':
    main()
