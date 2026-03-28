from ..base import RiotBaseDto


class AccountDto(RiotBaseDto):
    puuid: str
    game_name: str | None = None
    tag_line: str | None = None
