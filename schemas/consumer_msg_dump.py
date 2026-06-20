from pydantic import BaseModel


class ConsumerMsgCreate(BaseModel):
    event_name: str
    event_data: dict


class ConsumerMsgResponse(BaseModel):
    id: int
    event_name: str
    event_data: dict

    model_config = {"from_attributes": True}
