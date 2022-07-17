import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, VARCHAR
from sqlalchemy.dialects.postgresql import TIMESTAMP

from logic.model import GmId, ReportId
from logic.model import Report, NewGameReport


@dataclass
class ReportDB:
    players_ids: str
    game_name: str
    gm_id: GmId
    from_date: datetime
    to_date: datetime
    game_type: str

    def to_report(self, report_id: ReportId) -> Report:
        return Report(
            id=report_id,
            players_ids=[int(i) for i in self.players_ids.split(",")],
            game_name=self.game_name,
            gm_id=self.gm_id,
            from_date=self.from_date,
            to_date=self.to_date,
            game_type=self.game_type
        )


class DbStatsRepository:

    def __init__(self) -> None:
        self.db = {}
        url = self.__read_url()
        self.engine = create_engine(url)
        meta = MetaData(bind=self.engine)
        MetaData.reflect(meta)
        self.report_table = Table(
            'report', meta,
            Column('players_ids', VARCHAR),
            Column('game_name', VARCHAR),
            Column('gm_id', VARCHAR),
            Column('from_date', TIMESTAMP(timezone=True)),
            Column('to_date', TIMESTAMP(timezone=True)),
            Column('game_type', VARCHAR),
            Column('id', Integer, primary_key=True),
            extend_existing=True
        )
        meta.create_all(self.engine)

    def __read_url(self):
        url_from_env = os.environ['DATABASE_URL']
        final_url = url_from_env.replace('postgres', 'postgresql')
        return final_url

    def save_game(self, report: NewGameReport) -> Report:
        db_report = self.__map_to_db_report(report)
        statement = self.report_table.insert().values(**db_report.__dict__)
        new_id = self.engine.execute(statement).inserted_primary_key[0]
        return db_report.to_report(new_id)

    def list_all_by_gm(self, gm_id: GmId) -> List[Report]:
        queue = self.report_table.select().where(self.report_table.columns.gm_id == str(gm_id))
        result = []
        for row in self.engine.execute(queue):
            values = dict(row)
            report_id = values["id"]
            values.pop("id")
            r = ReportDB(**values)
            result.append(r.to_report(report_id))
        return result

    def remove_game_by_id(self, game_id: ReportId) -> bool:
        # TODO
        print(f"DbStatsRepository.remove_game_by_id not implemented")
        return False

    @staticmethod
    def __map_to_db_report(game_report: NewGameReport) -> ReportDB:
        return ReportDB(
            players_ids=",".join(map(str, game_report.players_ids)),
            game_name=game_report.game_name,
            gm_id=game_report.gm_id,
            from_date=game_report.from_date,
            to_date=game_report.to_date,
            game_type=game_report.game_type
        )
