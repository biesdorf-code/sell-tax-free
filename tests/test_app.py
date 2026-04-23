"""TST-010 / TST-011 — Flask integration."""

from io import BytesIO

import pytest

from sell_tax_free.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.secret_key = "test-secret"
    with app.test_client() as c:
        yield c


def test_upload_shows_sections_without_price_in_html(client):
    csv = (
        "Action,Time,ISIN,Ticker,Name,Notes,ID,No. of shares,Price / share\n"
        "Market buy,2024-05-24 18:26:04,US8740391003,TSM,X,,y,10,999.99\n"
    )
    rv = client.post(
        "/",
        data={"csv": (BytesIO(csv.encode()), "t.csv")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert rv.status_code == 200
    text = rv.data.decode("utf-8")
    assert "Tax-free" in text or "Waiting" in text
    assert "999.99" not in text
    assert "TSM" in text
    assert 'id="bubble-timeline"' in text
    assert "bubbles.js" in text


def test_bubble_timeline_one_row_per_lot_same_day_two_tickers(client):
    """REQ-201: two lots on same calendar day → two entries in bubble JSON."""
    csv = (
        "Action,Time,ISIN,Ticker,Name,Notes,ID,No. of shares,Price / share\n"
        "Market buy,2024-05-24 10:00:00,US1,AAA,X,,y,5,1.0\n"
        "Market buy,2024-05-24 15:00:00,US2,BBB,X,,y,3,1.0\n"
    )
    rv = client.post(
        "/",
        data={"csv": (BytesIO(csv.encode()), "t.csv")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert rv.status_code == 200
    text = rv.data.decode("utf-8")
    assert text.count('"ticker": "AAA"') == 1
    assert text.count('"ticker": "BBB"') == 1
    assert text.count('"lot_date": "2024-05-24"') == 2


def test_upload_uses_session_not_filesystem(client, tmp_path, monkeypatch):
    """REQ-102: no persisted upload file; session holds lot payload only."""
    csv = (
        "Action,Time,ISIN,Ticker,Name,Notes,ID,No. of shares,Price / share\n"
        "Market buy,2024-05-24 18:26:04,US8740391003,TSM,X,,y,10,1.0\n"
    )
    monkeypatch.chdir(tmp_path)
    rv = client.post(
        "/",
        data={"csv": (BytesIO(csv.encode()), "t.csv")},
        content_type="multipart/form-data",
        follow_redirects=False,
    )
    assert rv.status_code == 302
    assert not list(tmp_path.glob("**/*"))  # no files written by test cwd
    rv2 = client.get("/results", follow_redirects=False)
    assert rv2.status_code == 200
    assert b"TSM" in rv2.data
