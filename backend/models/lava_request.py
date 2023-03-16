from pydantic import BaseModel


class LavaRequest(BaseModel):
    invoice_id: str
    status: str
    pay_time: str
    amount: str
    order_id: str
    pay_service: str
    payer_details: str
    custom_fields: str
    type: int
    credited: str