import re
from functools import partial
from http.server import HTTPServer

import click

from .cache_manager import CacheManager
from .server import ProxyServer


def validate_origin(ctx, param, value):
    if value and not re.match(r'https?://', value):
        raise click.BadParameter(
            "origin must start with http:// or https://",
        )

    return value


@click.command()
@click.option("--port", type=click.IntRange(1, 65535))
@click.option("--origin", type=str, callback=validate_origin)
@click.option("--clear-cache", is_flag=True, default=False)
def main(port, origin, clear_cache):
    if clear_cache:
        CacheManager().clear()
        click.echo("cache cleared")
        return

    if not port or not origin:
        raise click.UsageError(
            "Both --port and --origin are required to start the server.\n"
            "Example: caching-proxy --port 3000 --origin http://dummyjson.com"
        )

    cache = CacheManager()
    handler = partial(ProxyServer, origin, cache)
    httpd = HTTPServer(("", port), handler)
    click.echo(f"Starting caching proxy on port {port}...")
    click.echo(f"Forwarding requests to {origin}")
    httpd.serve_forever()
