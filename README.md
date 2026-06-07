# caching-server

A CLI tool that starts a caching proxy server. It forwards requests to an origin server and caches the responses — subsequent identical requests are served from cache instead of hitting the origin.

> Based on the [Caching Server](https://roadmap.sh/projects/caching-server) project from [roadmap.sh](https://roadmap.sh).

## How it works

```
client → caching-proxy → origin server
                ↓
            cache store
```

On the first request to a path, the proxy forwards it to the origin and stores the response (`X-Cache: MISS`). On any repeat request to the same path, it returns the stored response directly (`X-Cache: HIT`).

## Usage

```bash
# Start the proxy
caching-proxy --port <number> --origin <url>

# Example
caching-proxy --port 3000 --origin http://dummyjson.com

# Clear the cache
caching-proxy --clear-cache
```

### Options

| Flag            | Required | Description                              |
|-----------------|----------|------------------------------------------|
| `--port`        | Yes      | Port the proxy will listen on (1–65535)  |
| `--origin`      | Yes      | Origin URL to forward requests to        |
| `--clear-cache` | No       | Clear all cached responses and exit      |

### Response headers

Every response includes an `X-Cache` header indicating whether it was served from cache:

```
X-Cache: HIT   # served from cache
X-Cache: MISS  # forwarded to origin and cached
```

## Project setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Install

```bash
# Clone the repo
git clone <repo-url>
cd caching-server

# Install the package and dependencies
uv sync

# Verify the CLI is available
caching-proxy --help
```

### Install git hooks

This project uses [pre-commit](https://pre-commit.com/) to manage hooks. Install them once after cloning:

```bash
pre-commit install --hook-type pre-commit --hook-type commit-msg
```

This installs two hooks:

- `pre-commit` — checks for trailing whitespace and large files on every commit
- `commit-msg` — validates your commit message format (see Commit convention below)

## Project structure

```
caching-server/
├── src/
│   └── caching_proxy/
│       ├── __init__.py
│       ├── cli.py        # CLI entry point
│       ├── server.py     # HTTP server and request forwarding
│       ├── cache.py      # Cache read/write/clear logic
│       └── logger.py     # Logging setup
├── .githooks/
│   ├── pre-commit
│   └── commit-msg
├── .pre-commit-config.yaml
└── pyproject.toml
```

## Commit convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/). The `commit-msg` hook will reject any message that does not match the format.

### Format

```
<type>(<scope>): <subject>
```

The scope is optional:

```
<type>: <subject>
```

### Types

| Type       | When to use                              |
|------------|------------------------------------------|
| `feat`     | A new feature                            |
| `fix`      | A bug fix                                |
| `docs`     | Documentation changes only               |
| `style`    | Formatting, no logic change              |
| `refactor` | Code change that is not a fix or feature |
| `perf`     | Performance improvement                  |
| `test`     | Adding or updating tests                 |
| `chore`    | Build process or tooling changes         |
| `ci`       | CI/CD configuration changes              |
| `revert`   | Reverts a previous commit                |

### Rules

- Use imperative mood: `add`, `fix`, `update` — not `added`, `fixed`, `updates`
- Do not capitalize the first letter after the type
- Do not end with a period
- Subject must be between 1 and 50 characters

### Examples

```bash
# Good
git commit -m "feat: add cache expiration support"
git commit -m "fix(cache): resolve key collision on query strings"
git commit -m "docs: update README with commit convention"
git commit -m "refactor(server): extract request handler into own module"
git commit -m "test(cli): add tests for --clear-cache flag"
git commit -m "chore: add pre-commit hooks"

# Bad — will be rejected by the hook
git commit -m "added caching"           # no type
git commit -m "Fix: something"          # capitalized subject
git commit -m "feat: Added new feature" # past tense, capitalized
git commit -m "WIP"                     # no type or format
```
