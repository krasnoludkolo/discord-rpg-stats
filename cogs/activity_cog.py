from discord import DMChannel
from discord.ext import commands

from db.activity_repository import DbActivityRepository


class ActivityCog(commands.Cog):

    def __init__(self, bot, **kwargs):
        self.bot = bot
        self.activityRepository = DbActivityRepository()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        new_channel = after.channel
        old_channel = before.channel
        if new_channel:
            log = new_channel.name
            if old_channel is None:
                log = f'joined {new_channel}'
                self.activityRepository.add_voice_activity(member.id)
            if old_channel and new_channel.name == old_channel.name:
                log = f'{new_channel} - status updated'
        else:
            log = f"disconnected from {old_channel.name}"
        print(f"{member}: {log}")

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        if type(channel) == DMChannel:
            print(f"DM: {message.author}:{message.content}")
        else:
            print(f"{channel.name} {message.author}")
            self.activityRepository.add_text_activity(message.author.id)
