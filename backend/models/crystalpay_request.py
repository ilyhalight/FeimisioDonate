from pydantic import BaseModel


class CrystalPayRequest(BaseModel):
    signature: str
    id: str
    url: str
    state: str
    type: str
    method: str
    required_method: str
    currency: str
    service_commission: int|float
    extra_commission: int|float
    amount: int|float
    pay_amount: int|float
    remaining_amount: int|float
    balance_amount: int|float
    description: str
    redirect_url: str
    callback_url: str
    extra: str
    created_at: str
    expired_at: str