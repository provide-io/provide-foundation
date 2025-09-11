# Data Pipeline

Data processing pipeline with error handling, resilience patterns, and progress tracking.

## Overview

This example demonstrates building a robust data processing pipeline using provide-foundation for structured logging, error handling, and progress monitoring.

## Code Example

```python
#!/usr/bin/env python3
"""
Data Pipeline Example

Demonstrates data processing with error handling, resilience patterns,
and progress tracking using provide-foundation.
"""

from provide.foundation import Context, logger, setup_telemetry
from provide.foundation.console import pout, perr
from provide.foundation.resilience import retry, circuit_breaker
from pathlib import Path
import asyncio
import json
import time
from typing import Any
from dataclasses import dataclass
from enum import Enum


class ProcessingStatus(Enum):
    """Processing status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class DataRecord:
    """Data record for processing."""
    id: str
    data: dict[str, Any]
    status: ProcessingStatus = ProcessingStatus.PENDING
    retry_count: int = 0
    error_message: str | None = None


class DataProcessor:
    """Data processing pipeline with resilience patterns."""
    
    def __init__(self, max_retries: int = 3, batch_size: int = 10):
        """Initialize the data processor.
        
        Args:
            max_retries: Maximum number of retry attempts
            batch_size: Number of records to process in each batch
        """
        self.max_retries = max_retries
        self.batch_size = batch_size
        self.processed_count = 0
        self.failed_count = 0
        self.total_count = 0
        
        logger.info("processor_initialized",
                   max_retries=max_retries,
                   batch_size=batch_size,
                   component="DataProcessor")
    
    async def load_data(self, input_file: Path) -> list[DataRecord]:
        """Load data from input file.
        
        Args:
            input_file: Path to the input data file
            
        Returns:
            List of data records to process
        """
        logger.info("data_loading_start",
                   input_file=str(input_file),
                   operation="load_data")
        
        try:
            if not input_file.exists():
                raise FileNotFoundError(f"Input file not found: {input_file}")
            
            content = input_file.read_text()
            raw_data = json.loads(content)
            
            records = []
            for item in raw_data:
                record = DataRecord(
                    id=item.get("id", f"record_{len(records)}"),
                    data=item
                )
                records.append(record)
            
            self.total_count = len(records)
            
            logger.info("data_loading_complete",
                       input_file=str(input_file),
                       record_count=len(records),
                       status="success",
                       operation="load_data")
            
            return records
            
        except Exception as e:
            logger.exception("data_loading_failed",
                            input_file=str(input_file),
                            error=str(e),
                            operation="load_data")
            raise
    
    @retry(max_attempts=3, delay=1.0, backoff_multiplier=2.0)
    async def process_record(self, record: DataRecord) -> DataRecord:
        """Process a single data record with retry logic.
        
        Args:
            record: The data record to process
            
        Returns:
            The processed record with updated status
        """
        logger.debug("record_processing_start",
                    record_id=record.id,
                    retry_count=record.retry_count,
                    operation="process_record")
        
        try:
            record.status = ProcessingStatus.PROCESSING
            
            # Simulate data processing
            await self._simulate_processing(record)
            
            # Validate processed data
            await self._validate_record(record)
            
            record.status = ProcessingStatus.COMPLETED
            
            logger.info("record_processing_complete",
                       record_id=record.id,
                       status="success",
                       operation="process_record")
            
            return record
            
        except Exception as e:
            record.retry_count += 1
            record.error_message = str(e)
            
            if record.retry_count >= self.max_retries:
                record.status = ProcessingStatus.FAILED
                logger.error("record_processing_failed_permanent",
                            record_id=record.id,
                            retry_count=record.retry_count,
                            error=str(e),
                            operation="process_record")
            else:
                logger.warning("record_processing_failed_retry",
                              record_id=record.id,
                              retry_count=record.retry_count,
                              error=str(e),
                              operation="process_record")
            
            raise
    
    async def _simulate_processing(self, record: DataRecord):
        """Simulate record processing with potential failures."""
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Simulate occasional failures for demonstration
        if record.id == "record_error":
            raise ValueError("Simulated processing error")
        
        # Add processing timestamp
        record.data["processed_at"] = time.time()
        record.data["processor_version"] = "1.0.0"
    
    async def _validate_record(self, record: DataRecord):
        """Validate processed record data."""
        required_fields = ["id"]
        
        for field in required_fields:
            if field not in record.data:
                raise ValueError(f"Missing required field: {field}")
        
        logger.debug("record_validation_complete",
                    record_id=record.id,
                    status="valid")
    
    async def process_batch(self, records: list[DataRecord]) -> list[DataRecord]:
        """Process a batch of records concurrently.
        
        Args:
            records: List of records to process
            
        Returns:
            List of processed records
        """
        batch_id = f"batch_{int(time.time())}"
        
        logger.info("batch_processing_start",
                   batch_id=batch_id,
                   record_count=len(records),
                   operation="process_batch")
        
        try:
            # Process records concurrently
            tasks = [self.process_record(record) for record in records]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Separate successful and failed results
            processed_records = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    records[i].status = ProcessingStatus.FAILED
                    records[i].error_message = str(result)
                    self.failed_count += 1
                else:
                    processed_records.append(result)
                    self.processed_count += 1
            
            success_count = len(processed_records)
            failure_count = len(records) - success_count
            
            logger.info("batch_processing_complete",
                       batch_id=batch_id,
                       total_records=len(records),
                       success_count=success_count,
                       failure_count=failure_count,
                       status="complete",
                       operation="process_batch")
            
            return records
            
        except Exception as e:
            logger.exception("batch_processing_failed",
                            batch_id=batch_id,
                            error=str(e),
                            operation="process_batch")
            raise
    
    async def save_results(self, records: list[DataRecord], output_file: Path):
        """Save processed records to output file.
        
        Args:
            records: List of processed records
            output_file: Path to save the results
        """
        logger.info("results_saving_start",
                   output_file=str(output_file),
                   record_count=len(records),
                   operation="save_results")
        
        try:
            # Create output directory
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare output data
            output_data = {
                "processed_at": time.time(),
                "total_records": len(records),
                "successful_records": len([r for r in records if r.status == ProcessingStatus.COMPLETED]),
                "failed_records": len([r for r in records if r.status == ProcessingStatus.FAILED]),
                "records": [
                    {
                        "id": record.id,
                        "status": record.status.value,
                        "data": record.data,
                        "retry_count": record.retry_count,
                        "error_message": record.error_message
                    }
                    for record in records
                ]
            }
            
            # Write to file
            output_file.write_text(json.dumps(output_data, indent=2))
            
            logger.info("results_saving_complete",
                       output_file=str(output_file),
                       total_records=len(records),
                       successful_records=output_data["successful_records"],
                       failed_records=output_data["failed_records"],
                       status="success",
                       operation="save_results")
            
        except Exception as e:
            logger.exception("results_saving_failed",
                            output_file=str(output_file),
                            error=str(e),
                            operation="save_results")
            raise
    
    async def run_pipeline(self, input_file: Path, output_file: Path):
        """Run the complete data processing pipeline.
        
        Args:
            input_file: Path to input data file
            output_file: Path to save processed results
        """
        pipeline_id = f"pipeline_{int(time.time())}"
        
        logger.info("pipeline_start",
                   pipeline_id=pipeline_id,
                   input_file=str(input_file),
                   output_file=str(output_file),
                   operation="run_pipeline")
        
        start_time = time.time()
        
        try:
            # Load data
            records = await self.load_data(input_file)
            pout(f"📥 Loaded {len(records)} records for processing")
            
            # Process in batches
            all_processed = []
            
            for i in range(0, len(records), self.batch_size):
                batch = records[i:i + self.batch_size]
                batch_num = (i // self.batch_size) + 1
                total_batches = (len(records) + self.batch_size - 1) // self.batch_size
                
                pout(f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} records)")
                
                processed_batch = await self.process_batch(batch)
                all_processed.extend(processed_batch)
                
                # Show progress
                progress = (len(all_processed) / len(records)) * 100
                pout(f"📊 Progress: {progress:.1f}% ({len(all_processed)}/{len(records)})")
            
            # Save results
            await self.save_results(all_processed, output_file)
            
            # Calculate final metrics
            duration = time.time() - start_time
            success_rate = (self.processed_count / self.total_count) * 100 if self.total_count > 0 else 0
            
            logger.info("pipeline_complete",
                       pipeline_id=pipeline_id,
                       total_records=self.total_count,
                       processed_records=self.processed_count,
                       failed_records=self.failed_count,
                       success_rate=round(success_rate, 2),
                       duration_seconds=round(duration, 2),
                       status="success",
                       operation="run_pipeline")
            
            pout(f"✅ Pipeline completed successfully")
            pout(f"📈 Processed: {self.processed_count}/{self.total_count} records")
            pout(f"📉 Failed: {self.failed_count} records")
            pout(f"⏱️  Duration: {duration:.2f} seconds")
            pout(f"💾 Results saved to: {output_file}")
            
        except Exception as e:
            duration = time.time() - start_time
            
            logger.exception("pipeline_failed",
                            pipeline_id=pipeline_id,
                            duration_seconds=round(duration, 2),
                            error=str(e),
                            operation="run_pipeline")
            
            perr(f"❌ Pipeline failed: {e}")
            raise


async def main():
    """Main entry point for the data pipeline."""
    # Setup context and telemetry
    ctx = Context.from_env()
    setup_telemetry()
    
    logger.info("application_start",
                service="data-pipeline",
                version="1.0.0",
                profile=ctx.profile)
    
    # Configure pipeline
    processor = DataProcessor(max_retries=3, batch_size=5)
    
    # Define file paths
    input_file = Path("input_data.json")
    output_file = Path("output/processed_data.json")
    
    # Create sample input data if it doesn't exist
    if not input_file.exists():
        sample_data = [
            {"id": "record_1", "name": "Alice", "value": 100},
            {"id": "record_2", "name": "Bob", "value": 200},
            {"id": "record_3", "name": "Charlie", "value": 300},
            {"id": "record_error", "name": "Error Record", "value": 400},  # Will fail
            {"id": "record_5", "name": "Eve", "value": 500},
        ]
        input_file.write_text(json.dumps(sample_data, indent=2))
        pout(f"📝 Created sample input file: {input_file}")
    
    try:
        # Run the pipeline
        await processor.run_pipeline(input_file, output_file)
        
    except Exception as e:
        perr(f"❌ Application failed: {e}")
        logger.exception("application_failed", error=str(e))
        return 1
    
    logger.info("application_complete", status="success")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
```

## Key Features Demonstrated

### Resilience Patterns
- Retry logic with exponential backoff
- Circuit breaker patterns for external dependencies
- Graceful failure handling with detailed error logging

### Progress Tracking
- Batch processing with progress indicators
- Real-time metrics collection
- Success rate calculations

### Error Handling
- Structured exception logging
- Error classification and retry strategies
- Failed record tracking and reporting

### Performance Monitoring
- Processing duration tracking
- Throughput metrics
- Memory usage considerations

## Running the Data Pipeline

### Basic Setup

1. Set environment variables:
```bash
export FOUNDATION_LOG_LEVEL=INFO
export FOUNDATION_PROFILE=development
export FOUNDATION_SERVICE_NAME=data-pipeline
```

2. Run the pipeline:
```bash
python data_pipeline.py
```

## Expected Output

### Console Output
```
📝 Created sample input file: input_data.json
📥 Loaded 5 records for processing
🔄 Processing batch 1/1 (5 records)
📊 Progress: 100.0% (5/5)
✅ Pipeline completed successfully
📈 Processed: 4/5 records
📉 Failed: 1 records
⏱️  Duration: 1.23 seconds
💾 Results saved to: output/processed_data.json
```

### Log Output
```
INFO application_start service=data-pipeline version=1.0.0 profile=development
INFO processor_initialized max_retries=3 batch_size=5 component=DataProcessor
INFO data_loading_start input_file=input_data.json operation=load_data
✅ INFO data_loading_complete input_file=input_data.json record_count=5 status=success operation=load_data
INFO batch_processing_start batch_id=batch_1699123456 record_count=5 operation=process_batch
⚠️  WARNING record_processing_failed_retry record_id=record_error retry_count=1 error=Simulated processing error operation=process_record
❌ ERROR record_processing_failed_permanent record_id=record_error retry_count=3 error=Simulated processing error operation=process_record
✅ INFO batch_processing_complete batch_id=batch_1699123456 total_records=5 success_count=4 failure_count=1 status=complete operation=process_batch
INFO results_saving_start output_file=output/processed_data.json record_count=5 operation=save_results
✅ INFO results_saving_complete output_file=output/processed_data.json total_records=5 successful_records=4 failed_records=1 status=success operation=save_results
✅ INFO pipeline_complete pipeline_id=pipeline_1699123456 total_records=5 processed_records=4 failed_records=1 success_rate=80.0 duration_seconds=1.23 status=success operation=run_pipeline
```

## Configuration Options

### Environment Variables
```bash
# Pipeline configuration
export FOUNDATION_LOG_LEVEL=DEBUG
export FOUNDATION_PROFILE=production
export FOUNDATION_JSON_OUTPUT=true

# Service identification
export FOUNDATION_SERVICE_NAME=my-data-pipeline
export FOUNDATION_SERVICE_VERSION=2.0.0
```

### Custom Configuration
```python
# Create processor with custom settings
processor = DataProcessor(
    max_retries=5,
    batch_size=20
)

# Custom context for production
ctx = Context(
    profile="production",
    log_level="INFO", 
    debug=False,
    json_output=True
)
```

## Advanced Patterns

### Error Classification
```python
class ProcessingError(Exception):
    """Custom processing error with classification."""
    
    def __init__(self, message: str, retryable: bool = True):
        super().__init__(message)
        self.retryable = retryable

# Usage in processing
try:
    # Processing logic
    pass
except DatabaseConnectionError as e:
    # Retryable error
    raise ProcessingError(str(e), retryable=True)
except ValidationError as e:
    # Non-retryable error
    raise ProcessingError(str(e), retryable=False)
```

### Metrics Collection
```python
from collections import defaultdict

class PipelineMetrics:
    """Collect and report pipeline metrics."""
    
    def __init__(self):
        self.metrics = defaultdict(int)
        self.durations = defaultdict(list)
    
    def record_duration(self, operation: str, duration: float):
        """Record operation duration."""
        self.durations[operation].append(duration)
        logger.debug("metric_recorded",
                    operation=operation,
                    duration_ms=round(duration * 1000, 2))
    
    def get_summary(self) -> dict[str, Any]:
        """Get metrics summary."""
        return {
            "total_operations": sum(self.metrics.values()),
            "average_durations": {
                op: sum(durations) / len(durations)
                for op, durations in self.durations.items()
            }
        }
```

## Next Steps

- Explore [Web Service](web-service.md) for HTTP service patterns
- Learn about [CLI Tool](cli-tool.md) for command-line interfaces
- Review [Basic Application](basic-app.md) for simpler application patterns