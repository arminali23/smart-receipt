from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models.receipt import Receipt, ReceiptItem
from app.models.schemas import DashboardOut, DailySpending, CategorySpending

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardOut)
async def get_dashboard(db: AsyncSession = Depends(get_db)):
    now = datetime.now(timezone.utc)

    # Total receipts & spent
    total_result = await db.execute(
        select(func.count(Receipt.id), func.coalesce(func.sum(Receipt.total_amount), 0.0))
    )
    row = total_result.one()
    total_receipts = row[0]
    total_spent = round(row[1], 2)

    # Daily spending (last 30 days)
    thirty_days_ago = now - timedelta(days=30)
    daily_result = await db.execute(
        select(
            func.date(Receipt.created_at).label("day"),
            func.sum(Receipt.total_amount).label("total"),
        )
        .where(Receipt.created_at >= thirty_days_ago)
        .group_by(func.date(Receipt.created_at))
        .order_by(func.date(Receipt.created_at))
    )
    daily_spending = [
        DailySpending(date=str(r[0]), total=round(r[1], 2))
        for r in daily_result.all()
    ]

    # Monthly spending (last 12 months)
    twelve_months_ago = now - timedelta(days=365)
    monthly_result = await db.execute(
        select(
            func.strftime("%Y-%m", Receipt.created_at).label("month"),
            func.sum(Receipt.total_amount).label("total"),
        )
        .where(Receipt.created_at >= twelve_months_ago)
        .group_by(func.strftime("%Y-%m", Receipt.created_at))
        .order_by(func.strftime("%Y-%m", Receipt.created_at))
    )
    monthly_spending = [
        DailySpending(date=str(r[0]), total=round(r[1], 2))
        for r in monthly_result.all()
    ]

    # Category spending
    cat_result = await db.execute(
        select(
            ReceiptItem.category,
            func.sum(ReceiptItem.total_price).label("total"),
        )
        .group_by(ReceiptItem.category)
        .order_by(func.sum(ReceiptItem.total_price).desc())
    )
    category_spending = [
        CategorySpending(category=r[0], total=round(r[1], 2))
        for r in cat_result.all()
    ]

    return DashboardOut(
        daily_spending=daily_spending,
        monthly_spending=monthly_spending,
        category_spending=category_spending,
        total_receipts=total_receipts,
        total_spent=total_spent,
    )
