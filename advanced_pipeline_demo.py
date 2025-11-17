#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2025 provide.io llc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Advanced Data Processing Pipeline - Comprehensive Foundation Example

This example demonstrates a production-ready data processing pipeline using
advanced features of provide.foundation:

- Async/await throughout the pipeline
- HTTP transport simulation with retries
- Distributed tracing context propagation
- File operations with atomic writes
- Archive creation with checksums
- Multiple resilience patterns (retry, circuit breaker)
- Metrics collection
- Cryptographic hashing
- Comprehensive error handling

Features demonstrated:
✨ 10+ advanced patterns in a realistic data pipeline
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from attrs import define

from provide.foundation import (
    BackoffStrategy,
    circuit_breaker,
    logger,
    perr,
    pout,
    retry,
)
from provide.foundation.archive import TarArchive
from provide.foundation.concurrency import async_gather
from provide.foundation.config import env_field
from provide.foundation.config.env import RuntimeConfig
from provide.foundation.crypto import hash_file
from provide.foundation.file import (
    atomic_write_text,
    ensure_dir,
)
from provide.foundation.metrics import counter, gauge, histogram
from provide.foundation.tracer import with_span


# Configuration
@define
class PipelineConfig(RuntimeConfig):
    """Data pipeline configuration."""

    pipeline_name: str = env_field(env_var="PIPELINE_NAME", default="data-processor")
    batch_size: int = env_field(env_var="BATCH_SIZE", default=10)
    output_dir: str = env_field(env_var="OUTPUT_DIR", default="/tmp/pipeline-output")


# Metrics
items_processed = counter("pipeline.items.processed", "Total items processed")
items_failed = counter("pipeline.items.failed", "Total items failed")
processing_time = histogram("pipeline.processing.duration", "Processing duration")
archive_size = gauge("pipeline.archive.size_bytes", "Archive size")


# Data models
@define
class DataItem:
    """A data item to process."""

    id: str
    content: str
    metadata: dict[str, Any]


@define
class ProcessingResult:
    """Result of processing."""

    item_id: str
    success: bool
    output_file: str | None = None
    checksum: str | None = None
    error: str | None = None


class DataSource:
    """Simulates data fetching with retries."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self._request_count = 0

    @retry(max_attempts=3, backoff=BackoffStrategy.EXPONENTIAL, base_delay=0.5)
    async def fetch_batch(self, batch_id: int) -> list[DataItem]:
        """Fetch a batch of data with automatic retry."""
        with with_span("fetch_data") as span:
            span.set_tag("batch_id", batch_id)

            logger.info("Fetching data batch", batch_id=batch_id)

            # Simulate network delay
            await asyncio.sleep(0.1)

            # Simulate occasional failures (triggers retry)
            self._request_count += 1
            if self._request_count % 5 == 0 and batch_id > 0:
                logger.warning("Simulated timeout", attempt=self._request_count)
                raise TimeoutError("Network timeout")

            # Generate synthetic data
            items = []
            for i in range(self.config.batch_size):
                item_id = f"item_{batch_id:03d}_{i:03d}"
                items.append(
                    DataItem(
                        id=item_id,
                        content=f"Data content for {item_id}",
                        metadata={"batch": batch_id, "index": i},
                    )
                )

            logger.info("Batch fetched", item_count=len(items))
            return items


class DataProcessor:
    """Processes data items with async workers."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self.output_dir = Path(config.output_dir)
        ensure_dir(str(self.output_dir))

    async def process_item(self, item: DataItem) -> ProcessingResult:
        """Process a single item with tracing."""
        with with_span("process_item") as span:
            span.set_tag("item.id", item.id)

            try:
                logger.debug("Processing item", item_id=item.id)

                # Simulate processing
                await asyncio.sleep(0.05)

                # Transform data
                processed = {
                    "id": item.id,
                    "processed_content": item.content.upper(),
                    "metadata": item.metadata,
                }

                # Write atomically
                output_file = self.output_dir / f"{item.id}.json"
                atomic_write_text(str(output_file), json.dumps(processed, indent=2))

                # Calculate checksum
                checksum = hash_file(str(output_file), algorithm="sha256")

                items_processed.inc()

                return ProcessingResult(
                    item_id=item.id,
                    success=True,
                    output_file=str(output_file),
                    checksum=checksum,
                )

            except Exception as e:
                items_failed.inc()
                logger.exception("Failed to process", item_id=item.id)
                return ProcessingResult(item_id=item.id, success=False, error=str(e))

    async def process_batch(self, items: list[DataItem]) -> list[ProcessingResult]:
        """Process batch concurrently."""
        with with_span("process_batch"):
            logger.info("Processing batch", item_count=len(items))

            # Process concurrently
            tasks = [self.process_item(item) for item in items]
            results = await async_gather(*tasks, return_exceptions=True)

            # Handle exceptions
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(
                        ProcessingResult(
                            item_id=items[i].id,
                            success=False,
                            error=str(result),
                        )
                    )
                else:
                    processed_results.append(result)

            successful = sum(1 for r in processed_results if r.success)
            logger.info("Batch complete", successful=successful, failed=len(items) - successful)

            return processed_results


class ArchiveManager:
    """Creates archives with checksums."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config

    def create_archive(self, source_dir: str, archive_path: str) -> tuple[str, int, str]:
        """Create archive with checksum."""
        with with_span("create_archive"):
            logger.info("Creating archive", source=source_dir)

            # Create archive from source directory
            archive = TarArchive()
            archive.create(Path(source_dir), Path(archive_path))

            # Count files in archive
            files_added = len(archive.list_contents(Path(archive_path)))

            logger.info("Archive created", files=files_added)

            # Checksum
            checksum = hash_file(archive_path, algorithm="sha256")
            size_bytes = Path(archive_path).stat().st_size
            archive_size.set(size_bytes)

            logger.info(
                "Archive finalized",
                size_bytes=size_bytes,
                checksum=checksum[:16],
            )

            return archive_path, size_bytes, checksum


class UploadService:
    """Handles uploads with circuit breaker."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self._upload_count = 0

    @circuit_breaker(failure_threshold=5, recovery_timeout=60.0)
    async def upload_archive(self, archive_path: str, checksum: str) -> bool:
        """Upload with circuit breaker protection."""
        logger.info("Uploading archive", checksum=checksum[:16])

        await asyncio.sleep(0.2)

        # Simulate occasional failures
        self._upload_count += 1
        if self._upload_count > 3 and self._upload_count % 3 == 0:
            logger.error("Upload failed", reason="service_unavailable")
            raise RuntimeError("Upload service unavailable")

        logger.info("Upload successful")
        return True


class DataPipeline:
    """Main pipeline orchestrator."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self.data_source = DataSource(config)
        self.processor = DataProcessor(config)
        self.archive_manager = ArchiveManager(config)
        self.upload_service = UploadService(config)

    async def run(self, num_batches: int = 3) -> dict[str, Any]:
        """Run the complete pipeline."""
        with with_span("run_pipeline"):
            logger.info("Starting pipeline", batches=num_batches)

            all_results = []
            start_time = asyncio.get_event_loop().time()

            try:
                # Phase 1: Fetch and process
                for batch_id in range(num_batches):
                    logger.info("Processing batch", batch=batch_id + 1, total=num_batches)

                    items = await self.data_source.fetch_batch(batch_id)
                    results = await self.processor.process_batch(items)
                    all_results.extend(results)

                # Phase 2: Create archive
                archive_path = str(Path(self.config.output_dir) / "results.tar.gz")
                archive_path, size_bytes, checksum = self.archive_manager.create_archive(
                    self.config.output_dir,
                    archive_path,
                )

                # Phase 3: Upload
                await self.upload_service.upload_archive(archive_path, checksum)

                # Summary
                elapsed = asyncio.get_event_loop().time() - start_time
                processing_time.observe(elapsed)

                successful = sum(1 for r in all_results if r.success)

                summary = {
                    "total_items": len(all_results),
                    "successful": successful,
                    "failed": len(all_results) - successful,
                    "archive_size_bytes": size_bytes,
                    "checksum": checksum,
                    "elapsed_seconds": round(elapsed, 2),
                }

                logger.info("Pipeline completed", **summary)
                return summary

            except Exception:
                logger.exception("Pipeline failed")
                raise


async def main() -> None:
    """Run the advanced pipeline demo."""
    pout("\n" + "=" * 70)
    pout("🏗️  Advanced Data Processing Pipeline")
    pout("=" * 70)
    pout("\n✨ Features Demonstrated:")
    pout("  • Async/await throughout")
    pout("  • Automatic retries with exponential backoff")
    pout("  • Distributed tracing with span propagation")
    pout("  • Concurrent worker pool processing")
    pout("  • Atomic file writes")
    pout("  • Archive creation with checksums")
    pout("  • Circuit breaker protection")
    pout("  • Metrics collection")
    pout("  • Structured logging with context")
    pout("=" * 70)

    config = PipelineConfig.from_env()
    pout(f"\n📋 Configuration: {config.pipeline_name}")
    pout(f"   Batch Size: {config.batch_size}")
    pout(f"   Output: {config.output_dir}\n")

    pipeline = DataPipeline(config)

    try:
        pout("🚀 Starting pipeline...\n")

        summary = await pipeline.run(num_batches=3)

        pout("\n" + "=" * 70)
        pout("✨ Pipeline Summary")
        pout("=" * 70)
        pout(f"  Total Items: {summary['total_items']}")
        pout(f"  Successful: {summary['successful']}")
        pout(f"  Failed: {summary['failed']}")
        pout(f"  Archive Size: {summary['archive_size_bytes']:,} bytes")
        pout(f"  Checksum: {summary['checksum'][:32]}...")
        pout(f"  Duration: {summary['elapsed_seconds']}s")
        pout("=" * 70)

        pout("\n📊 Metrics:")
        pout(f"  Processed: {items_processed._value}")
        pout(f"  Failed: {items_failed._value}")
        pout(f"  Archive Size: {archive_size._value:,} bytes")

        pout("\n✅ Pipeline completed successfully!")

    except Exception as e:
        perr(f"\n❌ Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
