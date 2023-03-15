from pydantic import BaseModel


class LavaRequest(BaseModel):
    invoice_id: str
    order_id: str
    status: str
    pay_time: str
    amount: int|float
    custom_fields: str
    credited: str
    pay_service: str
    payer_details: str