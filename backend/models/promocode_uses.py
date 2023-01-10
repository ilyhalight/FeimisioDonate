from pydantic import BaseModel


class PromocodeUses(BaseModel):
    uid: int
    key: str
    user: str
    target_uid: int
    timestamp: int