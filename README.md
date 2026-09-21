# Start the container

Install Docker with Docker Compose v2.23.0 or newer. From this directory, run:

```sh
docker compose up -d
```

Open <http://localhost:8000>.

To start with automatic application updates during development, run:

```sh
docker compose watch
```

# Git frontend

Add one public HTTPS clone URL per line to `stagit/repos.txt`. Repository names
must be unique. Run `docker compose up -d --build`, then open <http://localhost>.
The same pages are served at <https://git.lindholmlabs.com> in production.

The stagit container clones or fetches immediately, generates static pages, then
sleeps for 24 hours. Restart it with `docker compose restart stagit` to sync now.
Mirrors and generated pages persist in named volumes. Unavailable remotes keep
their last local copy; removing a URL does not delete its mirror. Caddy serves the
completed output read-only; stagit exposes no ports.

The Git pages use local copies of Codemadness's
[stylesheet](https://codemadness.org/git/style.css),
[favicon](https://codemadness.org/git/favicon.png), and
[logo](https://codemadness.org/git/logo.png).

# Software Requirements Specification

## Personal Résumé Website

### 1. Intent

Build a permanent, lightweight résumé website for a software developer.

Treat the site as a document published on the Web, not as a web application.

### 2. Application

**REQ-01 — Runtime**\
Use Python and Flask. Keep all Flask logic in `cv/main.py`.

**REQ-02 — Page**\
The application shall contain exactly one page. Serve the résumé at `/`. Keep HTML in `cv/index.html` and CSS in `cv/style.css`.

**REQ-03 — JavaScript**\
Do not use JavaScript.

### 3. Project Layout

**REQ-04 — Files**\
Use this structure:
```
/
├── .gitignore
├── .gitattributes
├── README.md
├── compose.yml
├── caddy/
│   └── Caddyfile
├── stagit/
│   ├── Dockerfile
│   ├── sync.sh
│   ├── repos.txt
│   ├── style.css
│   ├── favicon.png
│   └── logo.png
└── cv/
    ├── main.py
    ├── Dockerfile
    ├── requirements.txt
    ├── index.html
    ├── robots.txt
    ├── sitemap.xml
    └── style.css
```

Do not add directories.

**REQ-05 — README**\
The README shall contain only:

1. Instructions to start the container.
2. Git frontend instructions.
3. This SRS.

Place the start instructions first.

### 4. Container

**REQ-06 — Operation**\
Package the application with Docker. `docker compose up -d` shall start the site. Restarting the container shall restore normal operation.

**REQ-07 — Compose Watch**\
Configure `develop.watch` in `compose.yml`. `docker compose watch` shall detect changes to application files and update or rebuild the service as required.

**REQ-08 — Runtime Dependencies**\
Do not require external CDNs, hosted fonts, analytics, databases, build systems, JavaScript packages, or third-party runtime services.

### 5. Visual Design

**REQ-09 — Direction**\
Use the visual restraint of long-lived FOSS and Unix websites. Suitable references include CRUX Linux, kernel.org, OpenBSD, NetBSD, suckless.org, SQLite, musl libc, BusyBox, Alpine Linux, and SourceHut. Do not copy a reference site.

Do not imitate a terminal. Do not use fake prompts, simulated commands, or monospace text as decoration.

**REQ-10 — Palette**\
Use this palette:
```less
Accent blue      #007acc
Light highlight  #d4d4d4
Primary text     #333333
Dark highlight   #252525
Dark background  #1e1e1e
```

Declare colors as custom properties in `:root`. Reference those properties throughout the stylesheet. Use accent blue mainly for links and small accents.

**REQ-11 — Typography**\
Use system or web-safe fonts only. Declare each font stack once as a custom property in `:root`.

**REQ-12 — Style**\
Use typography, spacing, and hierarchy to structure the page. Avoid gradients, shadows, glass effects, animation, oversized hero sections, card grids, carousels, and decorative image galleries.

### 6. Content and Layout

**REQ-13 — Sections**\
Include:

- Introduction
- Work experience
- Education
- Selected projects
- Technical skills
- Contact and external links

Present experience and projects as concise text with ordinary links.

**REQ-14 — Responsive Layout**\
Use a restrained maximum width on large displays. Use one readable column on small displays. Require no JavaScript for responsive behavior.

### 7. Document Quality

**REQ-15 — HTML**\
Use semantic HTML5 and a logical heading order. The document shall remain readable without CSS.

**REQ-16 — CSS**\
Keep the stylesheet small and conventional. Prefer standard layout methods over frameworks or design-system abstractions.

**REQ-17 — Priorities**\
Prioritize, in order:

1. Maintainability
2. Accessibility
3. Readability
4. Browser compatibility
5. Load time
6. Visual character

When several solutions meet a requirement, use the simplest one.
