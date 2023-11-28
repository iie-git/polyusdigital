from pydantic import BaseModel, UUID4


class ItemOut(BaseModel):
    id: UUID4

class Msg(BaseModel):
    msg: str