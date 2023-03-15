from pydantic import BaseModel


class PrivilegeInfo(BaseModel):
    uid: int
    link: str
    name: str
    desc: str
    img_link: str
    is_big_img: int|bool|None = 0
    img_reverse_side: int|bool|None = 0