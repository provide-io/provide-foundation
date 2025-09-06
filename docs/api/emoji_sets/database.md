# Database Emoji Set

Visual enhancements for database operations, queries, and data management logging.

## Overview

The Database emoji set provides visual context for database operations, making it easy to identify different types of database activities at a glance. It covers common database operations including queries, transactions, connections, migrations, and performance monitoring.

## Emoji Mappings

### Query Operations
- **SELECT queries**: 🔍 (search/lookup operations)
- **INSERT operations**: ➕ (adding new data)  
- **UPDATE operations**: ✏️ (modifying existing data)
- **DELETE operations**: 🗑️ (removing data)

### Connection Management
- **Connection established**: 🔗 (successful connection)
- **Connection failed**: 🔌 (connection issues)
- **Connection pool**: 🏊 (pooled connections)
- **Connection timeout**: ⏱️ (timeout issues)

### Transaction Operations
- **Transaction started**: 🚀 (begin transaction)
- **Transaction committed**: ✅ (successful commit)
- **Transaction rolled back**: ↩️ (rollback operation)
- **Deadlock detected**: 🔒 (deadlock issues)

### Schema Operations
- **Migration started**: 🔄 (schema migration)
- **Migration completed**: 🎯 (successful migration)  
- **Index created**: 🗂️ (index operations)
- **Table created**: 🗄️ (table management)

## Usage Examples

### Basic Database Logging

```python
from provide.foundation import get_logger

# Create database-specific logger
db_log = get_logger("database")

# Query operations
db_log.debug("query_started", operation="SELECT", table="users")
db_log.info("query_completed", table="users", rows_returned=25, duration_ms=45)
db_log.error("query_failed", table="orders", error="syntax error")

# Connection management
db_log.info("connection_established", host="db.example.com", database="production")
db_log.warning("connection_pool_exhausted", max_connections=20, active=20)

# Transaction operations
db_log.debug("transaction_started", isolation="READ_COMMITTED")
db_log.info("transaction_committed", operations=3, duration_ms=120)
db_log.warning("transaction_rollback", reason="constraint_violation")
```

### ORM Integration

```python
from provide.foundation import get_logger
from sqlalchemy import event

# SQLAlchemy event listener for automatic logging
db_log = get_logger("database.orm")

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    db_log.debug("query_started", 
                statement=statement[:100],  # First 100 chars
                parameters=len(parameters) if parameters else 0)

@event.listens_for(Engine, "after_cursor_execute") 
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    db_log.info("query_completed",
               statement_type=statement.strip().split()[0].upper(),
               duration_ms=context.get_current_parameters().get('duration', 0))
```

### Database Repository Pattern

```python
from provide.foundation import get_logger

class UserRepository:
    def __init__(self):
        self.log = get_logger("database.users")
    
    async def find_by_id(self, user_id: int):
        self.log.debug("query_started", operation="SELECT", table="users", user_id=user_id)
        
        try:
            result = await self.db.fetch_one(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            
            if result:
                self.log.info("query_success", table="users", user_id=user_id, found=True)
                return result
            else:
                self.log.info("query_success", table="users", user_id=user_id, found=False)
                return None
                
        except Exception as e:
            self.log.error("query_failed", table="users", user_id=user_id, error=str(e))
            raise
    
    async def create(self, user_data: dict):
        self.log.debug("insert_started", table="users", fields=list(user_data.keys()))
        
        try:
            result = await self.db.fetch_one(
                "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
                user_data['name'], user_data['email']
            )
            
            self.log.info("insert_success", table="users", user_id=result['id'])
            return result
            
        except Exception as e:
            self.log.error("insert_failed", table="users", error=str(e))
            raise
```

### Database Migration Logging

```python
from provide.foundation import get_logger

class DatabaseMigrator:
    def __init__(self):
        self.log = get_logger("database.migrations")
    
    async def run_migration(self, migration_id: str):
        self.log.info("migration_started", migration_id=migration_id)
        
        try:
            # Run migration steps
            await self._create_tables()
            self.log.debug("migration_step_completed", step="create_tables")
            
            await self._create_indexes() 
            self.log.debug("migration_step_completed", step="create_indexes")
            
            await self._seed_data()
            self.log.debug("migration_step_completed", step="seed_data")
            
            self.log.info("migration_completed", migration_id=migration_id)
            
        except Exception as e:
            self.log.error("migration_failed", migration_id=migration_id, error=str(e))
            # Rollback logic here
            await self._rollback_migration()
            self.log.info("migration_rollback_completed", migration_id=migration_id)
            raise
```

## Performance Monitoring

### Query Performance Tracking

```python
import time
from provide.foundation import get_logger

class PerformanceLogger:
    def __init__(self):
        self.log = get_logger("database.performance")
    
    def log_slow_query(self, query: str, duration_ms: float, threshold_ms: float = 1000):
        if duration_ms > threshold_ms:
            self.log.warning("slow_query_detected",
                           query_type=query.strip().split()[0].upper(),
                           duration_ms=duration_ms,
                           threshold_ms=threshold_ms,
                           query=query[:200])  # Truncate long queries
    
    def log_query_stats(self, operation: str, table: str, rows_affected: int, duration_ms: float):
        self.log.info("query_performance",
                     operation=operation,
                     table=table,
                     rows_affected=rows_affected,
                     duration_ms=duration_ms,
                     rows_per_second=int(rows_affected / (duration_ms / 1000)) if duration_ms > 0 else 0)

# Usage with context manager
class TimedQuery:
    def __init__(self, logger, operation: str, table: str):
        self.logger = logger
        self.operation = operation
        self.table = table
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.debug("query_started", operation=self.operation, table=self.table)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = (time.time() - self.start_time) * 1000
        
        if exc_type:
            self.logger.error("query_failed", 
                            operation=self.operation,
                            table=self.table,
                            duration_ms=duration_ms,
                            error=str(exc_val))
        else:
            self.logger.info("query_completed",
                           operation=self.operation,
                           table=self.table,
                           duration_ms=duration_ms)

# Usage
db_log = get_logger("database")

with TimedQuery(db_log, "SELECT", "users"):
    results = await db.fetch_all("SELECT * FROM users WHERE active = true")
```

## Connection Pool Monitoring

```python
from provide.foundation import get_logger

class ConnectionPoolMonitor:
    def __init__(self, pool):
        self.pool = pool
        self.log = get_logger("database.pool")
    
    def log_pool_stats(self):
        stats = {
            "size": self.pool.size,
            "checked_in": self.pool.checkedin(),
            "checked_out": self.pool.checkedout(),
            "overflow": self.pool.overflow(),
            "invalidated": self.pool.invalidated(),
        }
        
        self.log.info("pool_status", **stats)
        
        # Alert on pool exhaustion
        if stats["checked_out"] >= stats["size"] * 0.9:  # 90% utilization
            self.log.warning("pool_high_utilization",
                           utilization_percent=int((stats["checked_out"] / stats["size"]) * 100))
    
    def log_connection_event(self, event_type: str, connection_id: str = None):
        self.log.debug("connection_event",
                      event=event_type,
                      connection_id=connection_id,
                      pool_size=self.pool.size,
                      active_connections=self.pool.checkedout())

# Periodic monitoring
import asyncio

async def monitor_pool_periodically(monitor: ConnectionPoolMonitor, interval: int = 60):
    while True:
        try:
            monitor.log_pool_stats()
            await asyncio.sleep(interval)
        except Exception as e:
            monitor.log.error("pool_monitoring_failed", error=str(e))
            await asyncio.sleep(interval)
```

## Database Health Checks

```python
from provide.foundation import get_logger

class DatabaseHealthChecker:
    def __init__(self, db_connection):
        self.db = db_connection
        self.log = get_logger("database.health")
    
    async def check_connectivity(self):
        try:
            await self.db.fetch_val("SELECT 1")
            self.log.info("health_check_passed", check="connectivity")
            return True
        except Exception as e:
            self.log.error("health_check_failed", check="connectivity", error=str(e))
            return False
    
    async def check_query_performance(self, threshold_ms: float = 100):
        start_time = time.time()
        
        try:
            await self.db.fetch_val("SELECT COUNT(*) FROM information_schema.tables")
            duration_ms = (time.time() - start_time) * 1000
            
            if duration_ms <= threshold_ms:
                self.log.info("health_check_passed", 
                            check="query_performance", 
                            duration_ms=duration_ms)
                return True
            else:
                self.log.warning("health_check_slow",
                               check="query_performance",
                               duration_ms=duration_ms,
                               threshold_ms=threshold_ms)
                return False
                
        except Exception as e:
            self.log.error("health_check_failed", check="query_performance", error=str(e))
            return False
    
    async def check_table_accessibility(self, tables: list[str]):
        results = {}
        
        for table in tables:
            try:
                await self.db.fetch_val(f"SELECT COUNT(*) FROM {table} LIMIT 1")
                self.log.debug("table_accessible", table=table)
                results[table] = True
            except Exception as e:
                self.log.error("table_not_accessible", table=table, error=str(e))
                results[table] = False
        
        accessible_count = sum(results.values())
        self.log.info("table_accessibility_check",
                     total_tables=len(tables),
                     accessible_tables=accessible_count,
                     success_rate=accessible_count / len(tables))
        
        return results
```

## Configuration

### Enabling Database Emoji Set

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        das_emoji_prefix_enabled=True,
        enabled_emoji_sets=["database"]
    )
)
setup_telemetry(config)
```

### Custom Database Emoji Set

```python
from provide.foundation.logger.emoji.types import EmojiSetConfig

class CustomDatabaseEmojiSet(EmojiSetConfig):
    """Custom database emoji set with additional mappings."""
    
    domain = "database"
    
    def get_emoji(self, action: str, status: str) -> str:
        # Custom mappings for specific database operations
        if action == "backup" and status == "success":
            return "💾✅"
        elif action == "restore" and status == "success":
            return "♻️✅"
        elif action.startswith("replication"):
            return "🔄" if status == "success" else "⚠️"
        elif action.startswith("vacuum"):
            return "🧹" if status == "success" else "❌"
        else:
            # Fallback to standard database emojis
            return super().get_emoji(action, status)

# Use custom emoji set
config = TelemetryConfig(
    logging=LoggingConfig(
        custom_emoji_sets=[CustomDatabaseEmojiSet()]
    )
)
```

## Best Practices

### 1. Log Levels for Database Operations

```python
# DEBUG: Detailed query information, parameter values
db_log.debug("query_started", sql=query, params=params)

# INFO: Successful operations, performance metrics  
db_log.info("query_completed", table="users", duration_ms=45)

# WARNING: Slow queries, high resource usage
db_log.warning("slow_query", duration_ms=2500, threshold_ms=1000)

# ERROR: Failed operations, constraint violations
db_log.error("query_failed", table="orders", error="foreign key constraint")
```

### 2. Sensitive Data Handling

```python
# Good: Log metadata, not sensitive data
db_log.info("user_created", user_id=123, email_domain="example.com")

# Avoid: Logging sensitive information
# db_log.info("user_created", email="user@example.com", password_hash="...")
```

### 3. Structured Context

```python
# Use consistent field names
db_log.info("operation_completed",
           operation="INSERT",
           table="users", 
           duration_ms=67,
           rows_affected=1)
```

## Related Documentation

- [Base Emoji Types](base.md) - Core emoji system interfaces
- [Custom Emoji Sets](custom.md) - Creating custom emoji sets
- [HTTP Emoji Set](http.md) - Web request logging emojis
- [Testing Guide](../../guide/testing.md) - Testing database logging