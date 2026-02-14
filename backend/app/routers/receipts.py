import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.receipt import Receipt, ReceiptItem
from app.models.schemas import ReceiptOut
from app.services.ocr_service import extract_text, parse_receipt
from app.ml.categorizer import categorizer

router = APIRouter(prefix="/receipts", tags=["receipts"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/scan", response_model=ReceiptOut)
async def scan_receipt(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()

    # Save image
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # OCR
    raw_text = extract_text(image_bytes)

    # Parse
    parsed = parse_receipt(raw_text)

    # Create receipt
    receipt = Receipt(
        store_name=parsed["store_name"],
        total_amount=parsed["total_amount"],
        image_path=filepath,
    )
    db.add(receipt)
    await db.flush()

    # Create items with ML categorization
    for item_data in parsed["items"]:
        category = categorizer.categorize(item_data["product_name"])
        item = ReceiptItem(
            receipt_id=receipt.id,
            product_name=item_data["product_name"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"],
            total_price=item_data["total_price"],
            category=category,
        )
        db.add(item)

    await db.commit()

    # Reload with items
    result = await db.execute(
        select(Receipt).options(selectinload(Receipt.items)).where(Receipt.id == receipt.id)
    )
    receipt = result.scalar_one()
    return receipt


@router.get("/", response_model=list[ReceiptOut])
async def list_receipts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Receipt).options(selectinload(Receipt.items)).order_by(Receipt.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{receipt_id}", response_model=ReceiptOut)
async def get_receipt(receipt_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Receipt).options(selectinload(Receipt.items)).where(Receipt.id == receipt_id)
    )
    receipt = result.scalar_one_or_none()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@router.delete("/{receipt_id}")
async def delete_receipt(receipt_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Receipt).where(Receipt.id == receipt_id))
    receipt = result.scalar_one_or_none()
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    await db.delete(receipt)
    await db.commit()
    return {"detail": "Deleted"}
