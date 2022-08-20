import os
from dataclasses import dataclass
from datetime import datetime, date

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, VARCHAR, inspect, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP

from logic.model import PlayerId


@dataclass
class ActivityDB:
    player_id: str
    day: date
    voice_activity: int
    text_activity: int
    last_activity: datetime
    is_bot: bool


class DbActivityRepository:

    def __init__(self) -> None:
        self.db = {}
        url = self.__read_url()
        self.engine = create_engine(url, echo=True)
        meta = MetaData(bind=self.engine)
        MetaData.reflect(meta)
        self.activity_table = Table(
            'activity', meta,
            Column('player_id', VARCHAR, primary_key=True),
            Column('day', TIMESTAMP(timezone=True), primary_key=True),
            Column('voice_activity', Integer),
            Column('text_activity', Integer),
            Column('last_activity', TIMESTAMP(timezone=True)),
            Column('is_bot', Boolean, default=False),
            extend_existing=True
        )
        meta.create_all(self.engine)
        self.primary_keys = [key.name for key in inspect(self.activity_table).primary_key]

    def __read_url(self):
        url_from_env = os.environ['DATABASE_URL']
        final_url = url_from_env.replace('postgres', 'postgresql')
        return final_url

    def add_voice_activity(self, player_id: PlayerId, is_bot: bool):
        self.__save_activity(player_id, new_voice_activity=1, is_bot=is_bot)

    def add_text_activity(self, player_id: PlayerId, is_bot: bool):
        self.__save_activity(player_id, new_text_activity=1, is_bot=is_bot)

    def __save_activity(self, player_id: PlayerId, is_bot: bool, new_voice_activity: int = 0,
                        new_text_activity: int = 0):
        activity_db = ActivityDB(
            player_id=str(player_id),
            day=date.today(),
            voice_activity=new_voice_activity,
            text_activity=new_text_activity,
            last_activity=datetime.now(),
            is_bot=is_bot
        )
        activity_table = self.activity_table

        statement = sqlalchemy.dialects.postgresql.insert(activity_table).values(**activity_db.__dict__)
        statement = statement \
            .on_conflict_do_update(
            index_elements=self.primary_keys,
            set_=dict(
                voice_activity=statement.excluded.voice_activity + activity_table.c.voice_activity,
                text_activity=statement.excluded.text_activity + activity_table.c.text_activity,
                last_activity=statement.excluded.last_activity,
                is_bot=statement.excluded.is_bot
            )
        )
        self.engine.execute(statement)
