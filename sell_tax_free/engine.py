"""
Lot aggregation and Luxembourg >6 calendar months classification.

Reference date R: server local date (date.today()). Documented in REQ-003.
Tax-free iff R > (D + relativedelta(months=6)) where D is lot acquisition date.
"""

from __future__ import annotations

import csv
import io
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import BinaryIO

from dateutil.relativedelta import relativedelta

# Expected CSV columns (broker export). Only these + Action/Time are read for logic.
MARKET_BUY = "Market buy"
REQUIRED_COLUMNS = (
    "Action",
    "Time",
    "Ticker",
    "No. of shares",
)


class ParseError(Exception):
    """User-facing parse validation error."""


@dataclass(frozen=True)
class Lot:
    ticker: str
    lot_date: date
    quantity: Decimal
    tax_free: bool
    """True iff reference_date > (lot_date + 6 calendar months)."""
    eligible_on: date
    """First calendar day on which R > six_month_anniversary (for messaging)."""
    days_until_tax_free: int | None
    """None if already tax-free; else days from reference to eligible_on (inclusive of eligible_on)."""


def _parse_time(value: str) -> datetime:
    value = (value or "").strip()
    if not value:
        raise ParseError("Market buy row missing Time.")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ParseError(f"Cannot parse Time: {value!r}")


def _parse_quantity(raw: str) -> Decimal:
    raw = (raw or "").strip()
    if not raw:
        raise ParseError("Market buy row missing No. of shares.")
    try:
        q = Decimal(raw)
    except InvalidOperation as e:
        raise ParseError(f"Invalid quantity: {raw!r}") from e
    if q <= 0:
        raise ParseError(f"Quantity must be positive: {raw!r}")
    return q


def six_month_anniversary(lot_date: date) -> date:
    return lot_date + relativedelta(months=6)


def first_eligible_date(lot_date: date) -> date:
    """First date R such that R > six_month_anniversary(lot_date)."""
    return six_month_anniversary(lot_date) + timedelta(days=1)


def classify_lot(lot_date: date, reference: date) -> tuple[bool, date, int | None]:
    """
    Returns (tax_free, eligible_on, days_until_or_none).
    """
    ann = six_month_anniversary(lot_date)
    tax_free = reference > ann
    eligible = first_eligible_date(lot_date)
    if tax_free:
        return True, eligible, None
    days = (eligible - reference).days
    if days < 0:
        days = 0
    return False, eligible, days


def parse_market_buys_from_csv(
    fileobj: BinaryIO,
    *,
    encoding: str = "utf-8-sig",
) -> list[tuple[str, date, Decimal]]:
    """
    Read CSV; return list of (ticker, lot_datetime.date(), quantity) per Market buy row
    before aggregation. Raises ParseError on bad header or invalid rows.
    """
    text = fileobj.read().decode(encoding)
    f = io.StringIO(text)
    reader = csv.DictReader(f)
    if reader.fieldnames is None:
        raise ParseError("CSV has no header row.")
    header = [h.strip() if h else "" for h in reader.fieldnames]
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing:
        raise ParseError(f"CSV missing required columns: {', '.join(missing)}")

    rows: list[tuple[str, date, Decimal]] = []
    for i, row in enumerate(reader, start=2):
        action = (row.get("Action") or "").strip()
        if action != MARKET_BUY:
            continue
        ticker = (row.get("Ticker") or "").strip()
        if not ticker:
            raise ParseError(f"Line {i}: Market buy missing Ticker.")
        dt = _parse_time(row.get("Time") or "")
        qty = _parse_quantity(row.get("No. of shares") or "")
        rows.append((ticker, dt.date(), qty))
    return rows


def aggregate_lots(
    rows: list[tuple[str, date, Decimal]],
) -> list[tuple[str, date, Decimal]]:
    """Merge same (ticker, calendar day); sum quantities."""
    acc: dict[tuple[str, date], Decimal] = defaultdict(lambda: Decimal(0))
    for ticker, d, qty in rows:
        acc[(ticker, d)] += qty
    return sorted(acc.items(), key=lambda x: (x[0][0], x[0][1]))


def build_classified_lots(
    fileobj: BinaryIO,
    *,
    reference: date | None = None,
    encoding: str = "utf-8-sig",
) -> list[Lot]:
    reference = reference or date.today()
    raw = parse_market_buys_from_csv(fileobj, encoding=encoding)
    merged = aggregate_lots(raw)
    lots: list[Lot] = []
    for (ticker, lot_date), qty in merged:
        tax_free, eligible_on, days_left = classify_lot(lot_date, reference)
        lots.append(
            Lot(
                ticker=ticker,
                lot_date=lot_date,
                quantity=qty,
                tax_free=tax_free,
                eligible_on=eligible_on,
                days_until_tax_free=days_left,
            )
        )
    return lots


def lots_to_session_dicts(lots: list[Lot]) -> list[dict]:
    """JSON/session-safe dicts — never includes price fields."""
    return [
        {
            "ticker": l.ticker,
            "lot_date": l.lot_date.isoformat(),
            "quantity": format(l.quantity.normalize(), "f"),
            "tax_free": l.tax_free,
            "eligible_on": l.eligible_on.isoformat(),
            "days_until_tax_free": l.days_until_tax_free,
        }
        for l in lots
    ]


def session_dicts_to_lots(data: list[dict]) -> list[Lot]:
    out: list[Lot] = []
    for d in data:
        out.append(
            Lot(
                ticker=d["ticker"],
                lot_date=date.fromisoformat(d["lot_date"]),
                quantity=Decimal(d["quantity"]),
                tax_free=d["tax_free"],
                eligible_on=date.fromisoformat(d["eligible_on"]),
                days_until_tax_free=d.get("days_until_tax_free"),
            )
        )
    return out
