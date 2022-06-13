from typing import List

from db.stats_repository import DbStatsRepository
from logic.model import ReportId, GmId, NewGameReport, Report


class Stats:

    def __init__(self, stats_repository: DbStatsRepository) -> None:
        self.stats_repository = stats_repository

    def report_game(self, game_report: NewGameReport) -> Report:
        return self.stats_repository.save_game(game_report)

    def list_reports(self, gm_id: GmId) -> List[Report]:
        return self.stats_repository.list_all_by_gm(gm_id=gm_id)

    def remove_game_report(self, game_id: ReportId):
        self.stats_repository.remove_game_by_id(game_id)
