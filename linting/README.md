# Linting

From the repository root, build the tools once:

```sh
docker build -t resume-lint linting
```

Run in PowerShell:

```powershell
docker run --rm --network none -v "${PWD}:/workspace:ro" resume-lint
```

Run in Linux or macOS:

```sh
docker run --rm --network none -v "$PWD:/workspace:ro" resume-lint
```

Rebuild when tool dependencies change. Checks run offline, mount the source
read-only, and require no Docker socket. The first image build needs internet.
GitHub Actions runs these same commands for pushes and pull requests.

| Content | Check |
| --- | --- |
| HTML | HTMLHint: structure, attributes, duplicate IDs, alternative text |
| CSS | Stylelint recommended correctness rules |
| Python | Ruff: errors, imports, common bugs |
| English in HTML | CSpell spelling and write-good prose/style suggestions |
| Compose | Docker Compose configuration validation plus yamllint |
| Dockerfiles | Hadolint |
| Shell scripts | ShellCheck |
| Other YAML, including the workflow | yamllint |

All checks run even if an earlier check fails; any failure produces a nonzero
exit status. Each check lists its source files and prints PASS or FAIL with its
exit code. The final summary counts checks and unique files, and lists files
without a configured lint check so coverage is explicit. English checks list
the original HTML file whose extracted prose is checked.

Files are discovered recursively, excluding Git metadata, Python
virtual environments, bytecode, and node_modules. Dockerfiles use `Dockerfile`
or `*.Dockerfile`; Compose files use the standard compose/docker-compose names.

English checks extract visible HTML text, image alternative text, titles,
accessibility labels, and meta descriptions. They omit template expressions,
scripts, styles, and code blocks. Reported prose line numbers match the HTML
source. These are spelling and style checks, not a complete grammar checker.
Add legitimate names and technical terms to `cspell.json`; review prose
suggestions rather than automatically rewriting the document.
The subjective adverb and weasel-word checks are disabled so qualifiers such as
"approximately 55%" remain valid. Other write-good checks retain their defaults.

Configuration and tool dependencies live in this directory. The workflow itself
lives in `.github/workflows/`, as required by GitHub Actions. These tools are
development dependencies and are not installed in the website image.
