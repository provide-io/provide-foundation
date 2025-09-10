# Archive API

Archive and backup functionality for data preservation and disaster recovery.

## Overview

The `archive` module provides comprehensive archiving and backup capabilities for applications, including data compression, encryption, versioning, and automated backup strategies. It's designed for both operational backups and long-term data preservation.

## Key Features

- **Multiple Archive Formats**: ZIP, TAR, 7Z support with compression options
- **Encryption**: AES-256 encryption for sensitive data
- **Incremental Backups**: Efficient incremental and differential backups
- **Versioning**: Automatic versioning with retention policies
- **Cloud Storage**: Integration with AWS S3, Google Cloud, Azure
- **Scheduling**: Automated backup scheduling and monitoring

## Basic Usage

### Simple Archiving

```python
from provide.foundation.archive import archiver

# Create archive
archive = archiver.create_archive("backup.zip", source_path="./data/")

# Extract archive
archiver.extract_archive("backup.zip", destination="./restored/")

# List archive contents
contents = archiver.list_archive("backup.zip")
for item in contents:
    print(f"{item.name}: {item.size} bytes")
```

### Compressed Archives

```python
# Create compressed archive
compressed_archive = archiver.create_archive(
    "backup.tar.gz",
    source_path="./data/",
    compression="gzip",
    compression_level=9
)

# Various compression formats
formats = {
    "zip": archiver.create_zip("data.zip", "./data/"),
    "tar_gz": archiver.create_tar_gz("data.tar.gz", "./data/"),
    "tar_xz": archiver.create_tar_xz("data.tar.xz", "./data/"),
    "7z": archiver.create_7z("data.7z", "./data/")
}
```

## Advanced Archiving

### Encrypted Archives

```python
from provide.foundation.archive import encrypted_archiver

# Create encrypted archive
encrypted_archive = encrypted_archiver.create_encrypted_archive(
    "secure_backup.zip.enc",
    source_path="./sensitive_data/",
    password="secure_password_123",
    encryption_algorithm="AES-256-GCM"
)

# Extract encrypted archive
encrypted_archiver.extract_encrypted_archive(
    "secure_backup.zip.enc",
    destination="./restored/",
    password="secure_password_123"
)

# Key-based encryption
key = encrypted_archiver.generate_key()
encrypted_archiver.create_archive_with_key(
    "backup.enc",
    source_path="./data/",
    encryption_key=key
)
```

### Incremental Backups

```python
from provide.foundation.archive import backup_manager

# Initialize backup manager
backup_mgr = backup_manager.BackupManager(
    backup_location="./backups/",
    source_directories=["./data/", "./config/"]
)

# Create initial full backup
full_backup = await backup_mgr.create_full_backup("initial_backup")

# Create incremental backup (only changed files)
incremental_backup = await backup_mgr.create_incremental_backup(
    "daily_increment_001",
    base_backup=full_backup
)

# Create differential backup (changes since last full backup)
differential_backup = await backup_mgr.create_differential_backup(
    "weekly_differential_001",
    base_backup=full_backup
)
```

## Cloud Storage Integration

### AWS S3 Backup

```python
from provide.foundation.archive import cloud_backup

# Configure S3 backup
s3_backup = cloud_backup.S3BackupManager(
    bucket="my-app-backups",
    region="us-west-2",
    credentials={
        "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
        "aws_secret_access_key": "secret_key"
    }
)

# Upload backup to S3
await s3_backup.upload_backup(
    local_path="backup.tar.gz",
    s3_key="backups/2024/01/15/backup.tar.gz",
    storage_class="GLACIER"  # For long-term storage
)

# Download backup from S3
await s3_backup.download_backup(
    s3_key="backups/2024/01/15/backup.tar.gz",
    local_path="./restored/backup.tar.gz"
)
```

### Multi-Cloud Backup

```python
# Configure multiple cloud providers
multi_cloud = cloud_backup.MultiCloudManager([
    cloud_backup.S3BackupManager(bucket="aws-backups"),
    cloud_backup.GCSBackupManager(bucket="gcp-backups"),
    cloud_backup.AzureBlobManager(container="azure-backups")
])

# Upload to all providers
await multi_cloud.upload_to_all(
    local_path="backup.tar.gz",
    remote_path="backups/daily/backup.tar.gz"
)

# Verify backup integrity across providers
integrity_report = await multi_cloud.verify_integrity("backups/daily/backup.tar.gz")
```

## Backup Strategies

### Automated Backup Scheduling

```python
from provide.foundation.archive import backup_scheduler

# Configure backup schedule
scheduler = backup_scheduler.BackupScheduler(
    backup_manager=backup_mgr,
    cloud_manager=s3_backup
)

# Daily incremental backups
scheduler.schedule_incremental(
    frequency="daily",
    time="02:00",
    retention_days=30
)

# Weekly full backups
scheduler.schedule_full_backup(
    frequency="weekly",
    day_of_week="sunday",
    time="01:00",
    retention_weeks=12
)

# Monthly archive to cold storage
scheduler.schedule_archive(
    frequency="monthly",
    day_of_month=1,
    storage_class="DEEP_ARCHIVE",
    retention_years=7
)

# Start scheduler
await scheduler.start()
```

### Retention Policies

```python
from provide.foundation.archive import retention

# Configure retention policy
policy = retention.RetentionPolicy([
    retention.Rule("daily", keep_for_days=30),
    retention.Rule("weekly", keep_for_weeks=12),
    retention.Rule("monthly", keep_for_months=24),
    retention.Rule("yearly", keep_for_years=7)
])

# Apply retention policy
cleanup_report = await policy.apply(backup_location="./backups/")
logger.info("retention_applied",
           deleted_files=cleanup_report.deleted_count,
           space_freed=cleanup_report.space_freed_gb)
```

## Data Validation

### Backup Integrity

```python
from provide.foundation.archive import integrity

# Create backup with checksum
integrity_checker = integrity.IntegrityChecker()

backup_with_checksum = await archiver.create_archive(
    "backup.tar.gz",
    source_path="./data/",
    generate_checksum=True
)

# Verify backup integrity
is_valid = await integrity_checker.verify_archive("backup.tar.gz")
if not is_valid:
    logger.error("backup_corrupted", archive="backup.tar.gz")

# Deep integrity check
detailed_report = await integrity_checker.deep_verify(
    "backup.tar.gz",
    verify_contents=True,
    check_file_hashes=True
)
```

### Restore Verification

```python
# Test restore process
restore_tester = integrity.RestoreTester()

# Perform test restore
test_result = await restore_tester.test_restore(
    archive="backup.tar.gz",
    test_location="./test_restore/",
    verify_data_integrity=True
)

if test_result.success:
    logger.info("restore_test_passed", 
               files_restored=test_result.file_count,
               duration_seconds=test_result.duration)
else:
    logger.error("restore_test_failed", 
                errors=test_result.errors)
```

## Performance Optimization

### Parallel Processing

```python
from provide.foundation.archive import parallel_archiver

# Create archives in parallel
parallel_arch = parallel_archiver.ParallelArchiver(
    max_workers=4,
    chunk_size="100MB"
)

# Process multiple directories concurrently
archive_tasks = [
    parallel_arch.create_archive("data1.tar.gz", "./data1/"),
    parallel_arch.create_archive("data2.tar.gz", "./data2/"),
    parallel_arch.create_archive("data3.tar.gz", "./data3/")
]

archives = await asyncio.gather(*archive_tasks)
```

### Streaming Archives

```python
# Stream large archives without loading into memory
streaming_archiver = archiver.StreamingArchiver()

# Create streaming archive
async with streaming_archiver.create_stream("large_backup.tar.gz") as stream:
    async for file_path in large_file_source():
        await stream.add_file(file_path)

# Extract streaming archive
async with streaming_archiver.extract_stream("large_backup.tar.gz") as stream:
    async for extracted_file in stream:
        await process_extracted_file(extracted_file)
```

## Monitoring and Alerting

### Backup Monitoring

```python
from provide.foundation.archive import monitoring

# Monitor backup operations
backup_monitor = monitoring.BackupMonitor(
    alert_on_failure=True,
    alert_on_duration_threshold="1h",
    alert_channels=["email", "slack"]
)

# Monitor scheduled backups
@backup_monitor.monitor_backup
async def monitored_backup():
    # Backup operation is automatically monitored
    result = await backup_mgr.create_full_backup("monitored_backup")
    return result

# Check backup health
health_report = await backup_monitor.health_check()
logger.info("backup_health",
           last_successful_backup=health_report.last_success,
           failed_backups_count=health_report.recent_failures)
```

### Alerting Configuration

```python
# Configure alerting
alerting_config = monitoring.AlertingConfig(
    email_config={
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "alerts@company.com",
        "password": "app_password"
    },
    slack_config={
        "webhook_url": "https://hooks.slack.com/services/...",
        "channel": "#infrastructure-alerts"
    }
)

# Set up alerts
backup_monitor.configure_alerting(alerting_config)
```

## Database Backup Integration

### Database-Specific Backups

```python
from provide.foundation.archive import db_backup

# PostgreSQL backup
pg_backup = db_backup.PostgreSQLBackup(
    connection_string="postgresql://user:pass@localhost/mydb"
)

# Create database backup
db_archive = await pg_backup.create_backup(
    output_path="db_backup.sql.gz",
    compress=True,
    include_schema=True,
    include_data=True
)

# MongoDB backup
mongo_backup = db_backup.MongoDBBackup(
    connection_string="mongodb://localhost:27017/mydb"
)

# Create MongoDB backup
mongo_archive = await mongo_backup.create_backup(
    output_path="mongo_backup.bson.gz",
    compress=True
)
```

## Disaster Recovery

### Recovery Planning

```python
from provide.foundation.archive import disaster_recovery

# Create disaster recovery plan
dr_plan = disaster_recovery.DisasterRecoveryPlan(
    backup_locations=[
        "s3://primary-backups/",
        "gs://secondary-backups/",
        "/mnt/local-backup/"
    ],
    recovery_priority=[
        {"component": "database", "rto": "15m", "rpo": "1h"},
        {"component": "application_data", "rto": "30m", "rpo": "4h"},
        {"component": "user_uploads", "rto": "2h", "rpo": "24h"}
    ]
)

# Execute disaster recovery
recovery_result = await dr_plan.execute_recovery(
    target_environment="production",
    recovery_point="2024-01-15T10:00:00Z"
)
```

## Testing and Validation

### Backup Testing

```python
from provide.foundation.archive.testing import BackupTestCase

class TestBackupRestore(BackupTestCase):
    async def test_full_backup_restore(self):
        """Test complete backup and restore cycle."""
        # Create test data
        test_data = self.create_test_data()
        
        # Create backup
        backup_path = await self.backup_manager.create_full_backup("test_backup")
        
        # Simulate data loss
        self.simulate_data_loss()
        
        # Restore from backup
        restore_result = await self.backup_manager.restore_backup(backup_path)
        
        # Verify restoration
        self.assert_data_restored(test_data)
```

## Best Practices

### Backup Strategy
```python
# 3-2-1 Backup Rule: 3 copies, 2 different media, 1 offsite
backup_strategy = {
    "local_backup": "./backups/",           # 1st copy - local
    "network_backup": "//nas/backups/",     # 2nd copy - network storage
    "cloud_backup": "s3://offsite-backup/" # 3rd copy - cloud (offsite)
}

# Regular testing
await backup_tester.run_monthly_test()
```

### Security
```python
# Always encrypt sensitive backups
if contains_sensitive_data:
    archiver_config.encryption = "AES-256-GCM"
    archiver_config.password_strength = "strong"

# Use key rotation
key_manager.rotate_encryption_keys(frequency="quarterly")
```

### Performance
```python
# Use appropriate compression for your data
compression_settings = {
    "text_data": "gzip",      # Good compression ratio
    "media_files": "store",    # Already compressed
    "databases": "lz4"         # Fast compression/decompression
}
```

## API Reference

::: provide.foundation.archive

## Related Documentation

- [Security Guide](../../guide/security/index.md) - Backup security best practices
- [Configuration Guide](../../guide/config/index.md) - Archive configuration
- [File API](../file/api-index.md) - File system operations