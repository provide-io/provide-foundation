# Database Integration

Integration patterns for database operations and ORM frameworks.

### SQLAlchemy Integration

```python
import time
from typing import Any, Optional
from sqlalchemy import event, Engine
from sqlalchemy.engine import Connection
from sqlalchemy.pool import Pool

from provide.foundation import get_logger

class SQLAlchemyLoggingIntegration:
    """Comprehensive SQLAlchemy logging integration."""
    
    def __init__(self, logger_name: str = "database.sqlalchemy"):
        self.logger = get_logger(logger_name)
        self.query_times: dict[str, float] = {}
    
    def setup_engine_logging(self, engine: Engine):
        """Setup logging for SQLAlchemy engine events."""
        
        # Connection events
        event.listen(engine, "connect", self._on_connect)
        event.listen(engine, "checkout", self._on_checkout)
        event.listen(engine, "checkin", self._on_checkin)
        
        # Statement execution events  
        event.listen(engine, "before_cursor_execute", self._before_cursor_execute)
        event.listen(engine, "after_cursor_execute", self._after_cursor_execute)
        
        # Pool events
        if hasattr(engine.pool, 'size'):
            event.listen(engine.pool, "connect", self._on_pool_connect)
            event.listen(engine.pool, "checkout", self._on_pool_checkout)
            event.listen(engine.pool, "checkin", self._on_pool_checkin)
    
    def _on_connect(self, dbapi_connection, connection_record):
        """Handle new database connections."""
        self.logger.info("Database connection established",
            domain="database",
            action="connect",
            status="success",
            connection_id=id(dbapi_connection)
        )
    
    def _on_checkout(self, dbapi_connection, connection_record, connection_proxy):
        """Handle connection checkout from pool."""
        self.logger.debug("Connection checked out from pool",
            domain="database", 
            action="checkout",
            status="success",
            connection_id=id(dbapi_connection),
            pool_size=getattr(connection_record.info, 'pool_size', 'unknown'),
            checked_out_connections=getattr(connection_record.info, 'checked_out', 'unknown')
        )
    
    def _on_checkin(self, dbapi_connection, connection_record):
        """Handle connection checkin to pool."""
        self.logger.debug("Connection returned to pool",
            domain="database",
            action="checkin", 
            status="success",
            connection_id=id(dbapi_connection)
        )
    
    def _before_cursor_execute(self, conn: Connection, cursor, statement: str, 
                             parameters, context, executemany: bool):
        """Log before SQL execution."""
        
        # Generate unique execution ID
        execution_id = f"{id(cursor)}_{time.time()}"
        
        # Store start time
        self.query_times[execution_id] = time.time()
        
        # Parse query type
        query_type = self._extract_query_type(statement)
        
        # Log query start
        self.logger.debug("SQL query starting",
            domain="database",
            action="query",
            status="started",
            execution_id=execution_id,
            query_type=query_type,
            statement=self._sanitize_statement(statement)[:500],  # Truncate long queries
            parameter_count=len(parameters) if parameters else 0,
            executemany=executemany
        )
        
        # Store execution context
        context.execution_id = execution_id
        context.query_type = query_type
    
    def _after_cursor_execute(self, conn: Connection, cursor, statement: str,
                            parameters, context, executemany: bool):
        """Log after SQL execution."""
        
        execution_id = getattr(context, 'execution_id', 'unknown')
        query_type = getattr(context, 'query_type', 'unknown')
        
        # Calculate duration
        start_time = self.query_times.pop(execution_id, time.time())
        duration = time.time() - start_time
        
        # Get row count if available
        try:
            row_count = cursor.rowcount if cursor.rowcount >= 0 else None
        except:
            row_count = None
        
        # Determine if query was slow
        is_slow = duration > 1.0  # Configurable threshold
        log_level = "warning" if is_slow else "debug"
        
        # Log query completion
        getattr(self.logger, log_level)("SQL query completed",
            domain="database",
            action="query",
            status="success",
            execution_id=execution_id,
            query_type=query_type,
            duration_ms=round(duration * 1000, 2),
            row_count=row_count,
            is_slow=is_slow,
            executemany=executemany
        )
    
    def _on_pool_connect(self, dbapi_connection, connection_record):
        """Handle pool connection events."""
        self.logger.debug("Pool connection created",
            domain="database",
            action="pool_connect",
            status="success",
            connection_id=id(dbapi_connection)
        )
    
    def _on_pool_checkout(self, dbapi_connection, connection_record, connection_proxy):
        """Handle pool checkout events."""
        pool = connection_record.pool
        
        self.logger.debug("Pool connection checkout", 
            domain="database",
            action="pool_checkout",
            status="success",
            connection_id=id(dbapi_connection),
            pool_size=pool.size(),
            checked_out=pool.checkedout(),
            overflow=pool.overflow(),
            checked_in=pool.checkedin()
        )
    
    def _on_pool_checkin(self, dbapi_connection, connection_record):
        """Handle pool checkin events."""
        self.logger.debug("Pool connection checkin",
            domain="database", 
            action="pool_checkin",
            status="success",
            connection_id=id(dbapi_connection)
        )
    
    def _extract_query_type(self, statement: str) -> str:
        """Extract query type from SQL statement."""
        statement_upper = statement.strip().upper()
        
        if statement_upper.startswith('SELECT'):
            return 'select'
        elif statement_upper.startswith('INSERT'):
            return 'insert'
        elif statement_upper.startswith('UPDATE'):
            return 'update'
        elif statement_upper.startswith('DELETE'):
            return 'delete'
        elif statement_upper.startswith('CREATE'):
            return 'create'
        elif statement_upper.startswith('DROP'):
            return 'drop'
        elif statement_upper.startswith('ALTER'):
            return 'alter'
        else:
            return 'other'
    
    def _sanitize_statement(self, statement: str) -> str:
        """Sanitize SQL statement for logging."""
        # Remove excessive whitespace
        import re
        statement = re.sub(r'\\s+', ' ', statement.strip())
        
        # Could add more sanitization here
        # (e.g., mask sensitive data in queries)
        
        return statement

# Usage example
def setup_database_logging():
    """Setup database with comprehensive logging."""
    from sqlalchemy import create_engine
    
    # Create engine
    engine = create_engine(
        "postgresql://user:pass@localhost/mydb",
        pool_size=10,
        pool_pre_ping=True,
        echo=False  # Disable SQLAlchemy's built-in logging
    )
    
    # Setup Foundation logging
    db_logging = SQLAlchemyLoggingIntegration()
    db_logging.setup_engine_logging(engine)
    
    return engine
```

