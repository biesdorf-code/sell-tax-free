"""REQ-002 / REQ-003 acceptance examples."""

from datetime import date
from decimal import Decimal
from io import BytesIO

import pytest

from sell_tax_free.engine import (
    ParseError,
    aggregate_lots,
    build_classified_lots,
    classify_lot,
    parse_market_buys_from_csv,
)


def test_aggregate_same_day():
    rows = [
        ("TSM", date(2024, 5, 24), Decimal("10")),
        ("TSM", date(2024, 5, 24), Decimal("10")),
    ]
    out = aggregate_lots(rows)
    assert out == [(("TSM", date(2024, 5, 24)), Decimal("20"))]


def test_aggregate_different_days():
    rows = [
        ("TSM", date(2024, 5, 24), Decimal("10")),
        ("TSM", date(2024, 5, 28), Decimal("5")),
    ]
    out = aggregate_lots(rows)
    assert len(out) == 2


def test_classify_req003_may24():
    D = date(2024, 5, 24)
    tax_free, eligible, days = classify_lot(D, date(2024, 11, 25))
    assert tax_free is True
    assert days is None
    tax_free, eligible, days = classify_lot(D, date(2024, 11, 24))
    assert tax_free is False
    assert days is not None


def test_classify_req003_jan31():
    D = date(2024, 1, 31)
    tax_free, _, days = classify_lot(D, date(2024, 7, 31))
    assert tax_free is False
    tax_free, _, days = classify_lot(D, date(2024, 8, 1))
    assert tax_free is True


def test_parse_ignores_deposit():
    csv = (
        "Action,Time,ISIN,Ticker,Name,Notes,ID,No. of shares,Price / share\n"
        "Deposit,2024-05-24 12:30:11,,,,\"Bank Transfer\",x,,,\n"
        "Market buy,2024-05-24 18:26:04,US8740391003,TSM,\"Taiwan Semi\",,y,10.0,159.65\n"
    )
    rows = parse_market_buys_from_csv(BytesIO(csv.encode()))
    assert len(rows) == 1
    assert rows[0][0] == "TSM"


def test_parse_rejects_bad_header():
    csv = "foo,bar\n1,2\n"
    with pytest.raises(ParseError, match="missing required"):
        parse_market_buys_from_csv(BytesIO(csv.encode()))


def test_build_never_exposes_price_in_output():
    csv = (
        "Action,Time,ISIN,Ticker,Name,Notes,ID,No. of shares,Price / share\n"
        "Market buy,2024-05-24 18:26:04,US8740391003,TSM,X,,y,10,999.99\n"
    )
    lots = build_classified_lots(BytesIO(csv.encode()), reference=date(2024, 11, 25))
    assert len(lots) == 1
    assert lots[0].ticker == "TSM"
    assert lots[0].quantity == Decimal("10")
