from app.crud.base import CRUDBase
from app.models.speaker import Speaker
from app.schemas.speaker import SpeakerCreate, SpeakerUpdate


class CRUDSpeaker(CRUDBase[Speaker, SpeakerCreate, SpeakerUpdate]):
    pass


speaker_crud = CRUDSpeaker(Speaker) 