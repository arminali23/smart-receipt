import pytesseract
from PIL import Image
import io
import re


def extract_text(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text


def parse_receipt(raw_text: str) -> dict:
    """Parse OCR text into structured receipt data."""
    lines = raw_text.strip().split("\n")
    items = []
    store_name = "Unknown"
    total_amount = 0.0

    # Try to extract store name from first non-empty line
    for line in lines:
        cleaned = line.strip()
        if cleaned and not re.match(r"^[\d\s\.\,\$\-\*]+$", cleaned):
            store_name = cleaned
            break

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match patterns like: "Product Name  2 x $3.99  $7.98"
        # or "Product Name  $3.99"
        # or "Product Name  3.99"
        # or "2x Product Name  7.98"

        # Check for total line
        total_match = re.match(
            r"(?:total|grand\s*total|amount\s*due|balance|sum)\s*[:\s]*\$?\s*([\d]+[.,]\d{2})",
            line, re.IGNORECASE,
        )
        if total_match:
            total_amount = float(total_match.group(1).replace(",", "."))
            continue

        # Skip header/footer lines
        if re.match(r"(?:subtotal|tax|change|cash|card|visa|master|date|time|tel|phone|thank|receipt)", line, re.IGNORECASE):
            continue

        # Pattern: qty x product price  or  product qty price
        item = _parse_item_line(line)
        if item:
            items.append(item)

    # If no total found, sum up items
    if total_amount == 0.0 and items:
        total_amount = sum(i["total_price"] for i in items)

    return {
        "store_name": store_name,
        "total_amount": round(total_amount, 2),
        "items": items,
    }


def _parse_item_line(line: str) -> dict | None:
    """Try to parse a single item line from a receipt."""

    # Pattern: "2 x Product Name  $7.98" or "2x Product Name 7.98"
    match = re.match(
        r"(\d+)\s*[xX]\s+(.+?)\s+\$?([\d]+[.,]\d{2})\s*$", line
    )
    if match:
        qty = float(match.group(1))
        name = match.group(2).strip()
        total = float(match.group(3).replace(",", "."))
        return {
            "product_name": name,
            "quantity": qty,
            "unit_price": round(total / qty, 2) if qty > 0 else total,
            "total_price": total,
        }

    # Pattern: "Product Name  2  $3.99  $7.98" (name, qty, unit, total)
    match = re.match(
        r"(.+?)\s{2,}(\d+)\s+\$?([\d]+[.,]\d{2})\s+\$?([\d]+[.,]\d{2})\s*$", line
    )
    if match:
        name = match.group(1).strip()
        qty = float(match.group(2))
        unit = float(match.group(3).replace(",", "."))
        total = float(match.group(4).replace(",", "."))
        return {
            "product_name": name,
            "quantity": qty,
            "unit_price": unit,
            "total_price": total,
        }

    # Pattern: "Product Name  $3.99" (single item)
    match = re.match(r"(.+?)\s{2,}\$?([\d]+[.,]\d{2})\s*$", line)
    if match:
        name = match.group(1).strip()
        price = float(match.group(2).replace(",", "."))
        if len(name) >= 2 and not name.isdigit():
            return {
                "product_name": name,
                "quantity": 1.0,
                "unit_price": price,
                "total_price": price,
            }

    # Pattern: "Product Name 3.99" (no dollar sign, at least 2 spaces or tab before)
    match = re.match(r"(.+?)\s+([\d]+[.,]\d{2})\s*$", line)
    if match:
        name = match.group(1).strip()
        price = float(match.group(2).replace(",", "."))
        if len(name) >= 3 and not re.match(r"^\d", name):
            return {
                "product_name": name,
                "quantity": 1.0,
                "unit_price": price,
                "total_price": price,
            }

    return None
