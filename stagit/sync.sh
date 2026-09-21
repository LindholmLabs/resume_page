#!/bin/sh
set -eu
export GIT_TERMINAL_PROMPT=0
mkdir -p /git /www
rm -rf /git/.clone

while :; do
    echo 'Synchronizing repositories'
    tr -d '\r' < /config/repos.txt > /tmp/repos.txt
    while IFS= read -r url || [ -n "$url" ]; do
        case "$url" in ''|'#'*) continue ;; esac
        name=${url##*/}
        name=${name%.git}
        case "$name" in ''|.*|*[!a-zA-Z0-9._-]*) echo "Invalid name: $name"; continue ;; esac
        mirror="/git/$name.git"
        if [ -d "$mirror" ]; then
            if git --git-dir="$mirror" fetch --atomic --prune origin; then
                echo "Updated $name"
            else
                echo "Unavailable: $name; keeping local mirror"
            fi
        elif git clone --mirror "$url" /git/.clone; then
            mv /git/.clone "$mirror"
            : > "$mirror/description"
            echo "Cloned $name"
        else
            rm -rf /git/.clone
            echo "Could not clone $name; skipping"
        fi
    done < /tmp/repos.txt

    echo 'Generating stagit pages'
    # Build in the inactive directory, then switch Caddy to the finished site.
    build=/www/a
    [ "$(readlink /www/current || true)" != a ] || build=/www/b
    rm -rf "$build"
    mkdir "$build"
    cp /assets/* "$build/"
    for mirror in /git/*.git; do
        [ -d "$mirror" ] || continue
        name=${mirror##*/}
        mkdir "$build/${name%.git}"
        (cd "$build/${name%.git}" && stagit "$mirror" &&
            ln -s log.html index.html &&
            ln -s ../style.css ../favicon.png ../logo.png .)
    done
    set -- /git/*.git
    if [ -d "$1" ]; then
        stagit-index "$@" > "$build/index.html"
    else
        echo '<!doctype html><title>Repositories</title><link rel="stylesheet" href="style.css"><link rel="icon" href="favicon.png"><img src="logo.png" alt=""><p>No repositories configured.</p>' > "$build/index.html"
    fi
    ln -sfn "${build##*/}" /www/current.new
    mv -Tf /www/current.new /www/current
    echo 'Site published; next synchronization in 24 hours'
    sleep 86400 &
    wait "$!"
done
