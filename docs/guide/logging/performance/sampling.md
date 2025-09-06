# Sampling Strategies

Log sampling and rate limiting techniques for managing high-volume logging scenarios.

## Rate-Based Sampling

### Simple Rate Limiting

```python
import time
import threading
from typing import Dict, Optional
from provide.foundation import get_logger

class RateLimitedLogger:
    """Logger with rate limiting to prevent log flooding."""
    
    def __init__(self, logger, max_rate: float = 100.0, window_size: float = 60.0):
        """
        Initialize rate limited logger.
        
        Args:
            logger: Base logger instance
            max_rate: Maximum messages per window
            window_size: Time window in seconds
        """
        self.logger = logger
        self.max_rate = max_rate
        self.window_size = window_size
        self._counts: Dict[str, list] = {}
        self._lock = threading.Lock()
    
    def _clean_old_entries(self, key: str, current_time: float):
        """Remove entries outside the time window."""
        cutoff_time = current_time - self.window_size
        self._counts[key] = [t for t in self._counts[key] if t > cutoff_time]
    
    def _should_log(self, key: str) -> bool:
        """Check if we should log based on rate limits."""
        current_time = time.time()
        
        with self._lock:
            if key not in self._counts:
                self._counts[key] = []
            
            # Clean old entries
            self._clean_old_entries(key, current_time)
            
            # Check if under rate limit
            if len(self._counts[key]) < self.max_rate:
                self._counts[key].append(current_time)
                return True
            
            return False
    
    def info(self, message: str, rate_limit_key: Optional[str] = None, **kwargs):
        """Log info message with rate limiting."""
        key = rate_limit_key or message
        
        if self._should_log(key):
            self.logger.info(message, **kwargs)
        elif rate_limit_key:
            # Log rate limit warning occasionally
            warning_key = f"rate_limit_warning:{key}"
            if self._should_log(warning_key):
                self.logger.warning("Log rate limit exceeded", 
                                  rate_limit_key=key,
                                  max_rate=self.max_rate,
                                  window_size=self.window_size)
    
    def error(self, message: str, rate_limit_key: Optional[str] = None, **kwargs):
        """Log error message with rate limiting (always logs errors)."""
        # Errors are typically always logged, but can be rate limited too
        key = rate_limit_key or f"error:{message}"
        
        if self._should_log(key):
            self.logger.error(message, **kwargs)

# Usage
base_logger = get_logger(__name__)
rate_limited = RateLimitedLogger(base_logger, max_rate=50, window_size=60)

# This will be rate limited
for i in range(1000):
    rate_limited.info("High frequency event", 
                     rate_limit_key="high_freq_event",
                     iteration=i)
```

### Adaptive Sampling

```python
import random
import time
import threading
from provide.foundation import get_logger

class AdaptiveSampler:
    """Adaptive sampler that adjusts sampling rate based on load."""
    
    def __init__(self, logger, target_rate: float = 100.0):
        """
        Initialize adaptive sampler.
        
        Args:
            logger: Base logger instance  
            target_rate: Target messages per second
        """
        self.logger = logger
        self.target_rate = target_rate
        self.current_rate = 0.0
        self.sample_probability = 1.0
        self.last_update = time.time()
        self.message_count = 0
        self.dropped_count = 0
        self._lock = threading.Lock()
    
    def _update_sampling_rate(self):
        """Update sampling probability based on current load."""
        current_time = time.time()
        
        with self._lock:
            time_delta = current_time - self.last_update
            
            if time_delta >= 1.0:  # Update every second
                self.current_rate = self.message_count / time_delta
                
                # Adjust sampling probability
                if self.current_rate > self.target_rate:
                    # Too many messages, reduce sampling
                    self.sample_probability *= 0.9
                else:
                    # Under target, increase sampling
                    self.sample_probability = min(1.0, self.sample_probability * 1.1)
                
                # Reset counters
                self.message_count = 0
                self.last_update = current_time
                
                # Log sampling stats occasionally
                if self.dropped_count > 0:
                    self.logger.info("Adaptive sampling stats",
                                   current_rate=round(self.current_rate, 1),
                                   sample_probability=round(self.sample_probability, 3),
                                   dropped_count=self.dropped_count)
                    self.dropped_count = 0
    
    def should_sample(self) -> bool:
        """Determine if current message should be sampled."""
        self._update_sampling_rate()
        
        with self._lock:
            self.message_count += 1
        
        if random.random() <= self.sample_probability:
            return True
        else:
            with self._lock:
                self.dropped_count += 1
            return False
    
    def sample_log(self, level: str, message: str, **kwargs):
        """Log message if it passes sampling."""
        if self.should_sample():
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(message, **kwargs)

# Usage
logger = get_logger("adaptive_sampling")
sampler = AdaptiveSampler(logger, target_rate=50)

# High volume logging with adaptive sampling
for i in range(10000):
    sampler.sample_log("info", "High volume message", iteration=i)
```

## Statistical Sampling

### Reservoir Sampling

```python
import random
from typing import List, Any, Dict
from provide.foundation import get_logger

class ReservoirSampler:
    """Reservoir sampling for maintaining representative log samples."""
    
    def __init__(self, logger, reservoir_size: int = 1000, report_interval: int = 10000):
        """
        Initialize reservoir sampler.
        
        Args:
            logger: Base logger instance
            reservoir_size: Size of sample reservoir
            report_interval: How often to report sample statistics
        """
        self.logger = logger
        self.reservoir_size = reservoir_size
        self.report_interval = report_interval
        self.reservoir: List[Dict[str, Any]] = []
        self.total_count = 0
    
    def add_sample(self, log_data: Dict[str, Any]):
        """Add a log entry to the reservoir sample."""
        self.total_count += 1
        
        if len(self.reservoir) < self.reservoir_size:
            # Fill reservoir
            self.reservoir.append(log_data)
        else:
            # Replace random element with probability k/n
            j = random.randint(0, self.total_count - 1)
            if j < self.reservoir_size:
                self.reservoir[j] = log_data
        
        # Report sample statistics periodically
        if self.total_count % self.report_interval == 0:
            self._report_sample_stats()
    
    def _report_sample_stats(self):
        """Report statistics about the current sample."""
        if not self.reservoir:
            return
        
        # Analyze sample for common patterns
        error_count = sum(1 for entry in self.reservoir 
                         if entry.get('level') == 'error')
        
        users = {entry.get('user_id') for entry in self.reservoir 
                if 'user_id' in entry}
        
        operations = {}
        for entry in self.reservoir:
            op = entry.get('operation', 'unknown')
            operations[op] = operations.get(op, 0) + 1
        
        self.logger.info("Reservoir sample analysis",
                        total_messages=self.total_count,
                        sample_size=len(self.reservoir),
                        error_rate=round(error_count / len(self.reservoir), 3),
                        unique_users=len(users),
                        top_operations=dict(sorted(operations.items(), 
                                                 key=lambda x: x[1], reverse=True)[:5]))
    
    def get_sample(self) -> List[Dict[str, Any]]:
        """Get current reservoir sample."""
        return self.reservoir.copy()

# Usage
logger = get_logger("reservoir_sampling")
sampler = ReservoirSampler(logger, reservoir_size=500)

# Simulate high-volume logging with sampling
for i in range(100000):
    log_entry = {
        'level': 'error' if i % 100 == 0 else 'info',
        'message': f"Message {i}",
        'user_id': f"user_{i % 1000}",
        'operation': random.choice(['read', 'write', 'delete', 'update'])
    }
    
    sampler.add_sample(log_entry)
    
    # Also log normally with sampling
    if sampler.total_count <= sampler.reservoir_size or random.random() < 0.01:
        logger.info(log_entry['message'], **{k: v for k, v in log_entry.items() 
                                           if k != 'message'})
```

### Stratified Sampling

```python
import random
import time
from collections import defaultdict
from typing import Dict, List, Any
from provide.foundation import get_logger

class StratifiedSampler:
    """Stratified sampling to ensure representation across different categories."""
    
    def __init__(self, logger, samples_per_stratum: int = 100):
        """
        Initialize stratified sampler.
        
        Args:
            logger: Base logger instance
            samples_per_stratum: Number of samples per category
        """
        self.logger = logger
        self.samples_per_stratum = samples_per_stratum
        self.strata: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.counts: Dict[str, int] = defaultdict(int)
    
    def add_to_stratum(self, stratum_key: str, log_data: Dict[str, Any]):
        """Add log entry to appropriate stratum."""
        self.counts[stratum_key] += 1
        
        # Reservoir sampling within each stratum
        if len(self.strata[stratum_key]) < self.samples_per_stratum:
            self.strata[stratum_key].append(log_data)
        else:
            # Replace random element
            j = random.randint(0, self.counts[stratum_key] - 1)
            if j < self.samples_per_stratum:
                self.strata[stratum_key][j] = log_data
    
    def sample_by_level(self, level: str, message: str, **kwargs):
        """Sample log messages stratified by log level."""
        log_data = {'level': level, 'message': message, **kwargs}
        
        # Add to stratum
        self.add_to_stratum(level, log_data)
        
        # Determine if we should actually log this message
        stratum_count = self.counts[level]
        
        # Always log first N messages of each level
        if len(self.strata[level]) < min(10, self.samples_per_stratum):
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(message, **kwargs)
        # Then sample probabilistically to maintain representation
        elif stratum_count % max(1, stratum_count // self.samples_per_stratum) == 0:
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(message, stratum_sampled=True, **kwargs)
    
    def sample_by_user(self, user_id: str, message: str, **kwargs):
        """Sample log messages stratified by user."""
        log_data = {'user_id': user_id, 'message': message, **kwargs}
        
        # Group users into buckets to limit number of strata
        user_bucket = f"user_bucket_{hash(user_id) % 10}"
        self.add_to_stratum(user_bucket, log_data)
        
        # Sample based on user bucket
        bucket_count = self.counts[user_bucket]
        if bucket_count <= self.samples_per_stratum or bucket_count % 10 == 0:
            self.logger.info(message, user_id=user_id, **kwargs)
    
    def get_stratum_stats(self) -> Dict[str, Dict]:
        """Get statistics for each stratum."""
        stats = {}
        for stratum, samples in self.strata.items():
            stats[stratum] = {
                'total_count': self.counts[stratum],
                'sample_count': len(samples),
                'sample_rate': len(samples) / max(1, self.counts[stratum])
            }
        return stats

# Usage
logger = get_logger("stratified_sampling")
sampler = StratifiedSampler(logger, samples_per_stratum=50)

# Simulate logging with different levels
for i in range(10000):
    if i % 100 == 0:
        sampler.sample_by_level('error', f"Error message {i}", error_code="E001")
    elif i % 50 == 0:
        sampler.sample_by_level('warning', f"Warning message {i}")
    else:
        sampler.sample_by_level('info', f"Info message {i}")
    
    # Also sample by user
    sampler.sample_by_user(f"user_{i % 500}", f"User action {i}", action="click")

# Report stratum statistics
stats = sampler.get_stratum_stats()
logger.info("Stratified sampling stats", stratum_stats=stats)
```

## Content-Based Sampling

### Error Rate Sampling

```python
import time
from collections import deque
from provide.foundation import get_logger

class ErrorRateSampler:
    """Sample based on error rates to maintain visibility during high error periods."""
    
    def __init__(self, logger, window_size: int = 1000, error_threshold: float = 0.1):
        """
        Initialize error rate sampler.
        
        Args:
            logger: Base logger instance
            window_size: Size of sliding window
            error_threshold: Error rate threshold for increased sampling
        """
        self.logger = logger
        self.window_size = window_size
        self.error_threshold = error_threshold
        self.recent_events = deque(maxlen=window_size)
        self.error_count = 0
    
    def _update_error_rate(self, is_error: bool):
        """Update error rate tracking."""
        # Add new event
        self.recent_events.append(is_error)
        if is_error:
            self.error_count += 1
        
        # Remove old events that fall out of window
        if len(self.recent_events) == self.window_size:
            # The event that was pushed out
            removed_event = len(self.recent_events) == self.window_size
            if removed_event and len(self.recent_events) > 0:
                # Count errors in current window
                self.error_count = sum(1 for event in self.recent_events if event)
    
    def get_error_rate(self) -> float:
        """Get current error rate."""
        if not self.recent_events:
            return 0.0
        return self.error_count / len(self.recent_events)
    
    def should_sample(self, is_error: bool) -> bool:
        """Determine sampling based on error rate."""
        self._update_error_rate(is_error)
        error_rate = self.get_error_rate()
        
        if is_error:
            # Always sample errors when error rate is high
            if error_rate > self.error_threshold:
                return True
            # Sample some errors even when rate is low
            return len(self.recent_events) % 10 == 0
        else:
            # Sample fewer non-errors when error rate is high
            if error_rate > self.error_threshold:
                return len(self.recent_events) % 50 == 0
            # Normal sampling for non-errors
            return len(self.recent_events) % 10 == 0
    
    def adaptive_log(self, level: str, message: str, **kwargs):
        """Log with adaptive sampling based on error rates."""
        is_error = level in ('error', 'critical')
        
        if self.should_sample(is_error):
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(message, 
                      error_rate=round(self.get_error_rate(), 3),
                      adaptive_sampled=True,
                      **kwargs)

# Usage
logger = get_logger("error_rate_sampling")
sampler = ErrorRateSampler(logger, window_size=500, error_threshold=0.05)

# Simulate varying error rates
for i in range(5000):
    # Simulate error bursts
    if 1000 <= i <= 1200:  # Error burst period
        is_error_period = True
        level = 'error' if i % 5 == 0 else 'warning'
    else:
        is_error_period = False
        level = 'error' if i % 100 == 0 else 'info'
    
    sampler.adaptive_log(level, f"Message {i}", 
                        period="error_burst" if is_error_period else "normal")
```

### Business Logic Sampling

```python
import random
import hashlib
from typing import Set, Dict, Any
from provide.foundation import get_logger

class BusinessLogicSampler:
    """Sample based on business logic importance."""
    
    def __init__(self, logger):
        self.logger = logger
        self.high_priority_users: Set[str] = set()
        self.important_operations: Set[str] = {'payment', 'auth', 'security'}
        self.user_sample_rates: Dict[str, float] = {}
    
    def set_high_priority_user(self, user_id: str):
        """Mark user as high priority (always sample their logs)."""
        self.high_priority_users.add(user_id)
    
    def set_user_sample_rate(self, user_id: str, rate: float):
        """Set custom sample rate for specific user."""
        self.user_sample_rates[user_id] = rate
    
    def _get_user_hash_bucket(self, user_id: str, num_buckets: int = 100) -> int:
        """Get consistent hash bucket for user."""
        hash_obj = hashlib.md5(user_id.encode())
        return int(hash_obj.hexdigest(), 16) % num_buckets
    
    def should_sample_for_user(self, user_id: str, operation: str) -> bool:
        """Determine if we should sample for this user/operation."""
        
        # Always sample high priority users
        if user_id in self.high_priority_users:
            return True
        
        # Always sample important operations
        if operation in self.important_operations:
            return True
        
        # Check custom sample rate
        if user_id in self.user_sample_rates:
            return random.random() < self.user_sample_rates[user_id]
        
        # Default: sample based on user hash bucket
        # This ensures consistent sampling for the same user
        bucket = self._get_user_hash_bucket(user_id)
        return bucket < 10  # 10% sample rate
    
    def business_log(self, level: str, message: str, user_id: str = None, 
                    operation: str = None, **kwargs):
        """Log with business logic-based sampling."""
        
        # Determine importance
        is_important = (
            level in ('error', 'warning') or
            operation in self.important_operations or
            (user_id and user_id in self.high_priority_users)
        )
        
        should_log = (
            is_important or 
            (user_id and self.should_sample_for_user(user_id, operation or 'default'))
        )
        
        if should_log:
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(message, 
                      user_id=user_id,
                      operation=operation,
                      business_priority=is_important,
                      **kwargs)

# Usage
logger = get_logger("business_sampling")
sampler = BusinessLogicSampler(logger)

# Configure business rules
sampler.set_high_priority_user("premium_user_123")
sampler.set_user_sample_rate("test_user_456", 1.0)  # Always sample test user

# Simulate business operations
operations = ['read', 'write', 'payment', 'auth', 'delete']
users = [f"user_{i}" for i in range(100)]

for i in range(10000):
    user_id = random.choice(users)
    operation = random.choice(operations)
    level = 'error' if i % 500 == 0 else 'info'
    
    sampler.business_log(level, f"Operation {i}", 
                        user_id=user_id,
                        operation=operation,
                        success=random.random() > 0.1)
```

## Advanced Sampling Patterns

### Multi-Dimensional Sampling

```python
import random
import time
from typing import Dict, Tuple, Any
from provide.foundation import get_logger

class MultiDimensionalSampler:
    """Sample based on multiple dimensions simultaneously."""
    
    def __init__(self, logger):
        self.logger = logger
        self.dimension_rates = {
            'level': {'debug': 0.01, 'info': 0.1, 'warning': 0.5, 'error': 1.0},
            'operation': {'read': 0.05, 'write': 0.2, 'delete': 0.5, 'auth': 1.0},
            'user_tier': {'free': 0.01, 'premium': 0.1, 'enterprise': 1.0}
        }
        self.base_sample_rate = 0.1
    
    def calculate_sample_probability(self, **dimensions) -> float:
        """Calculate sampling probability based on multiple dimensions."""
        probability = self.base_sample_rate
        
        for dimension, value in dimensions.items():
            if dimension in self.dimension_rates:
                dimension_rates = self.dimension_rates[dimension]
                rate = dimension_rates.get(str(value).lower(), self.base_sample_rate)
                # Multiply probabilities (intersection)
                probability *= (rate / self.base_sample_rate)
        
        return min(1.0, probability)  # Cap at 100%
    
    def multi_sample_log(self, level: str, message: str, **kwargs):
        """Log with multi-dimensional sampling."""
        
        # Extract dimensions from kwargs
        dimensions = {}
        for key in ['operation', 'user_tier', 'priority']:
            if key in kwargs:
                dimensions[key] = kwargs[key]
        
        dimensions['level'] = level
        
        # Calculate sampling probability
        prob = self.calculate_sample_probability(**dimensions)
        
        if random.random() < prob:
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(message, 
                      sample_probability=round(prob, 4),
                      dimensions=dimensions,
                      **kwargs)

# Usage
logger = get_logger("multi_dimensional_sampling")  
sampler = MultiDimensionalSampler(logger)

# Simulate multi-dimensional logging
for i in range(5000):
    level = random.choice(['debug', 'info', 'warning', 'error'])
    operation = random.choice(['read', 'write', 'delete', 'auth'])
    user_tier = random.choice(['free', 'premium', 'enterprise'])
    
    sampler.multi_sample_log(level, f"Multi-dimensional message {i}",
                           operation=operation,
                           user_tier=user_tier,
                           user_id=f"user_{i % 100}")
```

## Sampling Integration

### Framework Integration

```python
from provide.foundation import get_logger
from provide.foundation.logger.custom_processors import StructlogProcessor

def create_sampling_processor(sample_rate: float = 0.1) -> StructlogProcessor:
    """Create a processor that samples log messages."""
    
    import random
    
    def sampling_processor(logger, method_name, event_dict):
        """Processor that samples messages based on configured rate."""
        
        # Check if this message should be sampled
        if random.random() > sample_rate:
            # Drop this message by returning None or empty dict
            return None
        
        # Add sampling metadata
        event_dict["sampled"] = True
        event_dict["sample_rate"] = sample_rate
        
        return event_dict
    
    return sampling_processor

# Integration example (would be added to processor chain)
def setup_sampling_logging():
    """Setup logging with integrated sampling."""
    from provide.foundation.setup import setup_telemetry
    from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
    
    config = TelemetryConfig(
        logging=LoggingConfig(
            default_level="INFO",
            console_formatter="json"
        )
    )
    
    setup_telemetry(config)
    
    # Would add sampling processor to the processor chain
    sampling_proc = create_sampling_processor(0.1)
    # (Integration with processor chain would be implementation specific)

# Usage would be transparent to application code
logger = get_logger("sampled_app")
for i in range(1000):
    logger.info("This message may be sampled", iteration=i)
```