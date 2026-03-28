from src.schemas.riot.base import RiotBaseDto


class StatusBaseDto(RiotBaseDto):
    pass


class ContentDto(StatusBaseDto):
    locale: str
    content: str


class UpdateDto(StatusBaseDto):
    id: int
    author: str
    publish: bool
    publish_locations: list[str]
    translations: list[ContentDto]
    created_at: str
    updated_at: str


class StatusDto(StatusBaseDto):
    id: int
    maintenance_status: str
    incident_severity: str
    titles: list[ContentDto]
    updates: list[UpdateDto]
    created_at: str
    archive_at: str | None = None
    updated_at: str | None = None
    platforms: list[str]


class PlatformDataDto(StatusBaseDto):
    id: str
    name: str
    locales: list[str]
    maintenances: list[StatusDto]
    incidents: list[StatusDto]
