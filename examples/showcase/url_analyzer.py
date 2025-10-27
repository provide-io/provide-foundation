import asyncio
import os
import time
from attrs import define, field
from provide.foundation import (
    get_hub,
    get_logger,
    pout,
    perr,
)
from provide.foundation.cli.decorators import logging_options, output_options
from provide.foundation.config import RuntimeConfig
from provide.foundation.config.converters import parse_bool_extended, parse_comma_list
from provide.foundation.config.loader import RuntimeConfigLoader
from provide.foundation.config.manager import get_config, load_config, register_config
from provide.foundation.resilience.decorators import retry
from provide.foundation.hub import register_command
from provide.foundation.metrics import counter, histogram
from provide.foundation.concurrency import async_gather
from provide.foundation.crypto.hashing import hash_data
from provide.foundation.file import atomic_write
from provide.foundation.transport import UniversalClient

# Initialize logger
logger = get_logger(__name__)


# 1. Metrics Definitions
analyses_total = counter(
    "url_analyzer_analyses_total",
    "Total number of URLs processed.",
)
analysis_outcomes_total = counter(
    "url_analyzer_analysis_outcomes_total",
    "Total number of analysis outcomes by status.",
    ["status"],
)
fetch_duration_seconds = histogram(
    "url_analyzer_fetch_duration_seconds",
    "Duration of URL fetch requests in seconds.",
)


# 2. Custom Configuration
@define
class URLAnalyzerConfig(RuntimeConfig):
    """Configuration for the URL Analyzer."""
    output_dir: str = field(
        default="analyzer_output",
        metadata={
            "description": "Directory to save analysis results.",
            "env_var": "ANALYZER_OUTPUT_DIR",
        },
    )
    timeout: int = field(
        default=30,
        metadata={
            "description": "Request timeout in seconds.",
            "env_var": "ANALYZER_TIMEOUT",
        },
    )
    hash_algorithms: list[str] = field(
        default=["md5", "sha256"],
        metadata={
            "description": "Comma-separated list of hash algorithms to use.",
            "env_var": "ANALYZER_HASH_ALGORITHMS",
            "env_parser": parse_comma_list,
        },
    )
    retries: int = field(
        default=3,
        metadata={
            "description": "Number of times to retry a failed request.",
            "env_var": "ANALYZER_RETRIES",
            "env_parser": int,
        },
    )
    metrics_enabled: bool = field(
        default=True,
        metadata={
            "description": "Enable or disable metrics collection.",
            "env_var": "ANALYZER_METRICS_ENABLED",
            "env_parser": parse_bool_extended,
        },
    )


# 2. Core Logic and CLI Command
async def _process_single_url(url: str, hub, config, json_output: bool):
    if config.metrics_enabled:
        analyses_total.inc()

    from provide.foundation.transport.errors import HTTPResponseError, TransportError

    @retry(TransportError, max_attempts=config.retries)
    async def fetch_url_content():
        async with UniversalClient(hub=hub) as client:
            logger.debug("Fetching URL content", url=url, timeout=config.timeout)
            start_time = time.time()
            response = await client.get(url, timeout=config.timeout)
            if config.metrics_enabled:
                duration = time.time() - start_time
                fetch_duration_seconds.observe(duration)
            response.raise_for_status()
            return response

    logger.info("Starting URL analysis", url=url, output_dir=config.output_dir, algorithms=config.hash_algorithms)

    try:
        response = await fetch_url_content()
        content = response.body
    except TransportError as e:
        if config.metrics_enabled:
            analysis_outcomes_total.inc(1, status="failure")
        if isinstance(e, HTTPResponseError):
            logger.error("HTTP error occurred", status_code=e.status_code, url=url)
            perr(f"❌ HTTP Error: {e.status_code} for URL {url}")
        else:
            logger.error("Transport error occurred", error=str(e), url=url)
            perr(f"❌ Transport Error: {e}")
        return
    except Exception as e:
        if config.metrics_enabled:
            analysis_outcomes_total.inc(1, status="failure")
        logger.error("An unexpected error occurred", error=str(e))
        perr(f"❌ Unexpected Error: {e}")
        return

    if config.metrics_enabled:
        analysis_outcomes_total.inc(1, status="success")

    # Use the Crypto module
    hashes = {
        algo: hash_data(content, algorithm=algo)
        for algo in config.hash_algorithms
    }
    logger.info("Content hashes calculated", url=url, hashes=hashes)

    # Prepare results
    results = {
        "url": url,
        "status_code": response.status,
        "headers": dict(response.headers),
        "hashes": hashes,
    }

    if not json_output:
        # Ensure output directory exists
        os.makedirs(config.output_dir, exist_ok=True)
        # Use the File module for atomic write
        sha256_hash = hashes.get("sha256", "no-sha256-hash")
        filename = f"{sha256_hash}.json"
        filepath = os.path.join(config.output_dir, filename)

        output_content = results
        output_content["content"] = content.decode('utf-8', errors='ignore')

        from provide.foundation.serialization import json_dumps
        atomic_write(filepath, json_dumps(output_content, indent=2).encode("utf-8"))
        logger.info("Analysis result saved", url=url, filepath=filepath)
        pout(f"✅ Analysis complete for {url}. Result saved to: {filepath}")

    return results

async def analyze_url_async(
    urls: tuple[str, ...],
    config_file: str = None,
    log_level: str = None,
    log_file: str = None,
    log_format: str = None,
    json_output: bool = False,
    no_color: bool = False,
    no_emoji: bool = False,
) -> None:
    """
    Async implementation of the URL analysis.
    """
    hub = get_hub()
    config = get_config(URLAnalyzerConfig.__name__)

    if log_level:
        logger.setLevel(log_level)

    tasks = [_process_single_url(url, hub, config, json_output) for url in urls]
    results = await async_gather(*tasks)

    if json_output:
        # Filter out None results from failed analyses
        pout([res for res in results if res])



import click

@register_command("analyze", help="Analyze one or more URLs.")
@click.argument("url", nargs=-1)
@logging_options
@output_options
def analyze_url(
    url: tuple[str, ...],
    config_file: str = None,
    log_level: str = None,
    log_file: str = None,
    log_format: str = None,
    json_output: bool = False,
    no_color: bool = False,
    no_emoji: bool = False,
) -> None:
    """
    Fetches a URL, calculates its content hash, and saves the result.
    """
    asyncio.run(
        analyze_url_async(
            url,
            config_file,
            log_level,
            log_file,
            log_format,
            json_output=json_output,
            no_color=no_color,
            no_emoji=no_emoji,
        )
    )


# 7. Main entry point
if __name__ == "__main__":
    config_name = URLAnalyzerConfig.__name__
    register_config(
        config_name,
        loader=RuntimeConfigLoader(),
        defaults=URLAnalyzerConfig().to_dict(),
    )
    load_config(config_name, URLAnalyzerConfig)
    cli = get_hub().create_cli(help="URL Analyzer CLI")
    cli()
