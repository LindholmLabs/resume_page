"""Serve the résumé document and its stylesheet."""

from datetime import date

from flask import Flask, render_template, send_from_directory
from markupsafe import Markup

app = Flask(__name__, static_folder=None, template_folder=".")


@app.get("/")
def resume():
    return render_template("index.html", duration=duration)


@app.get("/style.css")
def stylesheet():
    return send_from_directory(app.root_path, "style.css")


def duration(start, end=None):
    start = date.fromisoformat(f"{start}-01")
    finish = date.fromisoformat(f"{end}-01") if end else date.today()

    months = (finish.year - start.year) * 12 + finish.month - start.month + 1
    years, months = divmod(months, 12)

    parts = [
        f"{years} year{'s' if years != 1 else ''}" if years else "",
        f"{months} month{'s' if months != 1 else ''}" if months else "",
    ]
    length = ", ".join(filter(None, parts))

    return Markup(f'<time datetime="{start:%Y-%m}">{start.year}</time> · {length}')


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8000)
