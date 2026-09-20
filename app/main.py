"""Serve the résumé document and its stylesheet."""

from flask import Flask, send_from_directory

app = Flask(__name__, static_folder=None)


@app.get("/")
def resume():
    return send_from_directory(app.root_path, "index.html")


@app.get("/style.css")
def stylesheet():
    return send_from_directory(app.root_path, "style.css")


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8000)
