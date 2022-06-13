import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime

from db.stats_repository import DbStatsRepository
from logic.model import ReportId, PlayerId
from logic.stats import Stats
from logic.model import NewGameReport, Report

date_format = "%Y-%m-%d %H:%M"


class StatsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.stats = Stats(stats_repository=DbStatsRepository())

    @commands.command()
    async def report(self,
                     ctx: Context,
                     members: commands.Greedy[discord.Member],
                     game_name: str,
                     from_date_raw: str,
                     to_date_raw: str,
                     # game_type: str
                     ):
        print('Recieved command !stats from ' + ctx.author.name + ', processing...')
        from_date = datetime.strptime(from_date_raw, date_format)
        to_date = datetime.strptime(to_date_raw, date_format)

        game_report = NewGameReport(
            players_ids=[member.id for member in members],
            game_name=game_name,
            gm_id=ctx.author.id,
            from_date=from_date,
            to_date=to_date,
            game_type="TODO"
        )
        report = self.stats.report_game(game_report)
        report_summary = await self.__game_summary(report)
        await ctx.send(report_summary)

    @commands.command()
    async def list(self, ctx: Context):
        reports = self.stats.list_reports(ctx.author.id)
        if len(reports) == 0:
            await ctx.send("Brak zgłoszonych gier")
        else:
            reports_str = "\n".join([await self.__game_summary(report) for report in reports])
            await ctx.send(reports_str)

    async def __game_summary(self, report: Report) -> str:
        return f"""
Id: {report.id}
System: {report.game_name}
Gracze: {[await self.__get_user_name(user_id) for user_id in report.players_ids]}
Data: {report.from_date}-{report.to_date}
"""

    @commands.command()
    async def remove(self, ctx: Context, game_id: ReportId):
        self.stats.remove_game_report(game_id=game_id)
        await ctx.send("Usunięto")

    async def __get_user_name(self, user_id: PlayerId) -> str:
        user = await self.bot.fetch_user(user_id)
        return user.name
