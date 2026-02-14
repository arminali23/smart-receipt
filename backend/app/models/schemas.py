from pydantic import BaseModel
from datetime import datetime


class ReceiptItemOut(BaseModel):
    id: int
    product_name: str
    quantity: float
    unit_price: float
    total_price: float
    category: str

    model_config = {"from_attributes": True}


class ReceiptOut(BaseModel):
    id: int
    store_name: str
    total_amount: float
    created_at: datetime
    items: list[ReceiptItemOut]

    model_config = {"from_attributes": True}


class DailySpending(BaseModel):
    date: str
    total: float


class CategorySpending(BaseModel):
    category: str
    total: float


class DashboardOut(BaseModel):
    daily_spending: list[DailySpending]
    monthly_spending: list[DailySpending]
    category_spending: list[CategorySpending]
    total_receipts: int
    total_spent: float
