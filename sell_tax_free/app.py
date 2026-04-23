"""
Flask app: CSV upload (ephemeral), tax-free / waiting list only.
No buy prices are ever passed to templates or stored in session beyond lot facts.
"""

from __future__ import annotations

import io
import os
from datetime import date

from flask import Flask, redirect, render_template, request, session, url_for

from sell_tax_free.engine import ParseError, build_classified_lots, lots_to_session_dicts, session_dicts_to_lots

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(
    __name__,
    template_folder=os.path.join(_ROOT, "templates"),
    static_folder=os.path.join(_ROOT, "static"),
)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-in-production")


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    reference = date.today()

    if request.method == "POST":
        f = request.files.get("csv")
        if not f or not f.filename:
            error = "Please choose a CSV file."
        else:
            try:
                data = f.read()
                lots = build_classified_lots(io.BytesIO(data), reference=reference)
                session["lots"] = lots_to_session_dicts(lots)
                session["reference"] = reference.isoformat()
                return redirect(url_for("results"))
            except ParseError as e:
                error = str(e)
            except UnicodeDecodeError:
                error = "File could not be read as UTF-8. Save the CSV as UTF-8 and try again."

    return render_template("index.html", error=error, reference=reference)


@app.route("/results")
def results():
    raw = session.get("lots")
    ref_s = session.get("reference")
    if not raw or not ref_s:
        return redirect(url_for("index"))

    lots = session_dicts_to_lots(raw)
    reference = date.fromisoformat(ref_s)
    tax_free = [l for l in lots if l.tax_free]
    waiting = [l for l in lots if not l.tax_free]
    lots_sorted = sorted(lots, key=lambda l: (l.lot_date, l.ticker))
    lots_bubble = lots_to_session_dicts(lots_sorted)

    return render_template(
        "results.html",
        reference=reference,
        tax_free=tax_free,
        waiting=waiting,
        lots_bubble=lots_bubble,
    )


@app.route("/deploy", methods=["GET", "POST"])
def deploy():
    """NFR-005: human gate before following NFR-006 (Coolify / Hetzner)."""
    if request.method == "POST":
        choice = (request.form.get("choice") or "").strip()
        if choice == "not_now":
            session.pop("deploy_show_steps", None)
            return redirect(url_for("index"))
        if choice == "yes":
            session["deploy_show_steps"] = True
            return redirect(url_for("deploy"))
        if choice == "hide_steps":
            session.pop("deploy_show_steps", None)
            return redirect(url_for("deploy"))
    show_steps = bool(session.get("deploy_show_steps"))
    return render_template("deploy.html", show_steps=show_steps)


@app.route("/clear", methods=["POST"])
def clear():
    session.pop("lots", None)
    session.pop("reference", None)
    return redirect(url_for("index"))
