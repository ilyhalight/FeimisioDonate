from pydantic import BaseModel


class PaymentSystem(BaseModel):
    name: str
    disabled: int = 0