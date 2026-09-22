"""Run all checks, report every failure, and leave the checkout unchanged."""

import re
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path.cwd()
CONFIG = ROOT / "linting"
EXCLUDED = {".git", ".venv", "node_modules", "__pycache__"}


class Prose(HTMLParser):
    """Preserve source line numbers while extracting text and accessible labels."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.lines = [""] * (source.count("\n") + 1)
        self.hidden = 0
        self.feed(re.sub(r"{{.*?}}|{%.*?%}|{#.*?#}",
                         lambda m: "\n" * m[0].count("\n"), source, flags=re.S))

    def add(self, value):
        for offset, line in enumerate(value.split("\n")):
            self.lines[self.getpos()[0] - 1 + offset] += " " + line

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "code", "pre"}:
            self.hidden += 1
        if not self.hidden:
            for key, value in attrs:
                if value and key in {"alt", "title", "aria-label"}:
                    self.add(value)
            attributes = dict(attrs)
            if tag == "meta" and attributes.get("name") == "description":
                self.add(attributes.get("content", ""))

    def handle_endtag(self, tag):
        if tag in {"script", "style", "code", "pre"}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden:
            self.add(data)


def main():
    files = sorted(path.relative_to(ROOT) for path in ROOT.rglob("*")
                   if path.is_file() and not EXCLUDED.intersection(path.parts))
    failed = []
    checked = set()
    checks = 0

    def check(label, command, sources):
        nonlocal checks
        checks += 1
        checked.update(sources)
        print(f"\n--- {label} ---", flush=True)
        print(f"Checking {len(sources)} file(s):", flush=True)
        for source in sources:
            print(f"  {source.as_posix()}", flush=True)
        result = subprocess.run([str(arg) for arg in command], check=False)
        if result.returncode:
            failed.append(label)
        print(f"{'FAIL' if result.returncode else 'PASS'}: {label} "
              f"(exit {result.returncode})", flush=True)

    def matching(suffix):
        return [path for path in files if path.suffix == suffix]

    html = matching(".html")
    if html:
        check("HTML", ["htmlhint", "--config", CONFIG / "htmlhint.json", *html], html)
    if css := matching(".css"):
        check("CSS", ["stylelint", "--config", CONFIG / "stylelint.json", *css], css)
    if python := matching(".py"):
        check("Python", ["ruff", "check", "--no-cache", "--config",
                         CONFIG / "ruff.toml", *python], python)
    with tempfile.TemporaryDirectory() as directory:
        for path in html:
            prose = Path(directory) / "prose.txt"
            prose.write_text("\n".join(Prose(path.read_text(encoding="utf-8")).lines),
                             encoding="utf-8")
            print(f"\nEnglish source: {path} (line numbers match HTML)", flush=True)
            check(f"Spelling: {path}", ["cspell", "--config", CONFIG / "cspell.json",
                                       "--root", directory, "--no-progress", prose], [path])
            check(f"English style: {path}", ["write-good", "--parse",
                                           "--no-adverb", "--no-weasel", prose], [path])
    yaml = matching(".yml") + matching(".yaml")
    if yaml:
        check("YAML", ["yamllint", "-c", CONFIG / "yamllint.yml", *yaml], yaml)
    for path in yaml:
        if path.name in {"compose.yml", "compose.yaml", "docker-compose.yml",
                         "docker-compose.yaml"}:
            check(f"Compose: {path}", ["docker", "compose", "-f", path,
                                      "config", "--quiet", "--no-path-resolution"], [path])
    for path in files:
        if path.name == "Dockerfile" or path.name.endswith(".Dockerfile"):
            check(f"Dockerfile: {path}", ["hadolint", path], [path])
    if shell := matching(".sh"):
        check("Shell", ["shellcheck", "--external-sources", *shell], shell)
    print(f"\nRan {checks} checks across {len(checked)} unique files.", flush=True)
    unchecked = sorted(set(files) - checked)
    if unchecked:
        print("Files without a configured lint check:", flush=True)
        for path in unchecked:
            print(f"  {path.as_posix()}", flush=True)
    print("\n" + ("Failed: " + ", ".join(failed) if failed else "All checks passed."))
    return bool(failed)


if __name__ == "__main__":
    raise SystemExit(main())
