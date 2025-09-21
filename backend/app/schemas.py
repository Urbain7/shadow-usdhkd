from pydantic import BaseModel
from datetime import date

class UsdHkdRateBase(BaseModel):
    rate: float
    date: date

class UsdhkdRate(UsdHkdRateBase):
    id: int
    class Config:
        from_attributes = True

class AggregateBalanceBase(BaseModel):
    balance: float
    date: date

class AggregateBalance(AggregateBalanceBase):
    id: int
    class Config:
        from_attributes = True

class HiborRateBase(BaseModel):
    rate: float
    period: str
    date: date

class HiborRate(HiborRateBase):
    id: int
    class Config:
        from_attributes = True