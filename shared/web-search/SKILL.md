---
name: web-search
description: "Use when searching the web, reading a public web page, or capturing a screenshot of
  one, and when the harness's own web tools come back empty, blocked or without the content a
  browser would show. Tries the harness's tools first, then curl, then Context.dev. Not for pages
  behind a login."
metadata:
  type: procedure
---

# Contract

## Input Contract

- A search query, a page URL, or a page to capture as an image.
- For Context.dev, an API key in `$CONTEXT_DEV_API_KEY` or `~/.config/context-dev/api_key`.

## Output Contract

- The search results with their URLs, the page's text, or the image saved as a file, each with
  the URL it came from.

# Entrypoint

## Stage 1: The harness's own tools

Search and fetch with the web tools the harness provides; they cost nothing. When they return the
content you came for, you are done. Go to Stage 2 when a fetch comes back empty, as a bot
challenge, or as a page shell that needs JavaScript to fill in. Go to Stage 3 for a search or a
screenshot the harness has no tool for.

## Stage 2: curl

Save the original and read it from the file:

```sh
curl -sSL --max-time 60 -o page.html 'https://example.com/page'
```

curl runs no JavaScript, so a page that arrives as an empty shell or a challenge goes to Stage 3.

## Stage 3: Context.dev

Context.dev loads the page in a real browser behind its own proxies, and runs web searches. It
sees what a logged-out visitor sees.

Read the key into a variable so it never prints:

```sh
K=${CONTEXT_DEV_API_KEY:-$(cat ~/.config/context-dev/api_key)}
ctx() { curl -sS --max-time 90 "https://api.context.dev/v1/$1" \
  -H "Authorization: Bearer $K" -H 'Content-Type: application/json' -d "$2"; }
```

| Need | Call | Answer in | Credits |
| --- | --- | --- | --- |
| Search | `ctx web/search '{"query": "...", "numResults": 10}'` | `results[]`: `title`, `url`, `description` | 1 per 10 results |
| Page text | `ctx web/scrape '{"url": "...", "formats": {"markdown": true}}'` | `markdown.data` | 1 |
| Screenshot | `ctx web/scrape '{"url": "...", "formats": {"screenshot": true}, "screenshotParams": {"area": "fullPage"}}'` | `screenshot.data`, a base64 data URL | 1 |

`area` is `viewport` by default, `fullPage`, or `{"selector": "main"}` for one element. Set the
window size with `"sharedParams": {"viewport": {"width": 1440, "height": 900}}`. Save a
screenshot to a file:

```sh
ctx web/scrape '{"url": "https://example.com", "formats": {"screenshot": true}}' |
  python3 -c 'import sys, json, base64
d = json.load(sys.stdin)["screenshot"]["data"]
open(sys.argv[1], "wb").write(base64.b64decode(d.split(",", 1)[1]))' shot.png
```
