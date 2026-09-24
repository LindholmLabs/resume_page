"""Serve the résumé document and its stylesheet."""

from datetime import date

from flask import Flask, render_template, send_from_directory
from markupsafe import Markup

app = Flask(__name__, static_folder=None, template_folder=".")


@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; style-src 'self'; img-src 'self'; "
        "script-src https://cloudflare.com https://*.cloudflare.com "
        "https://cloudflareinsights.com https://*.cloudflareinsights.com; "
        "connect-src https://cloudflareinsights.com https://*.cloudflareinsights.com; "
        "base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
    )
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.get("/")
def resume():
    return render_template("index.html", duration=duration, current_year=date.today().year)


@app.get("/style.css")
def stylesheet():
    return send_from_directory(app.root_path, "style.css")


@app.get("/robots.txt")
def robots():
    return send_from_directory(app.root_path, "robots.txt", mimetype="text/plain")


@app.get("/favicon.svg")
def favicon():
    return send_from_directory(app.root_path, "favicon.svg", mimetype="image/svg+xml")


@app.get("/sitemap.xml")
def sitemap():
    return send_from_directory(app.root_path, "sitemap.xml", mimetype="application/xml")


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

    if end is None:
        return Markup(f'<time datetime="{start:%Y-%m}">{start.strftime("%B")} {start.year}</time> – Present · {length}')

    return Markup(f'<time datetime="{start:%Y-%m}">{start.strftime("%B")} {start.year}</time> – <time datetime="{finish:%Y-%m}">{finish.strftime("%B")} {finish.year}</time> · {length}')


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8000)
