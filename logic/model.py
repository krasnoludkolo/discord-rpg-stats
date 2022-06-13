from dataclasses import dataclass
from datetime import datetime
from typing import List

ReportId = int
PlayerId = int
GmId = str


@dataclass
class Report:
    id: ReportId
    players_ids: List[PlayerId]
    game_name: str
    gm_id: GmId
    from_date: datetime
    to_date: datetime
    game_type: str


@dataclass
class NewGameReport:
    players_ids: List[PlayerId]
    game_name: str
    gm_id: GmId
    from_date: datetime
    to_date: datetime
    game_type: str
