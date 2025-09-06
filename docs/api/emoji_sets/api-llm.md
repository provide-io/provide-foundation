# LLM Emoji Set

Visual enhancements for AI/ML model interactions, inference operations, and machine learning workflows.

## Overview

The LLM emoji set provides visual context for AI and machine learning operations, making it easy to identify different types of AI/ML activities at a glance. It covers model interactions, inference operations, training processes, and resource management for AI workflows.

## Emoji Mappings

### Model Operations
- **Model loading**: 🤖 (model initialization)
- **Inference/prediction**: 🧠 (thinking/processing)
- **Training started**: 📚 (learning process)
- **Training completed**: 🎓 (graduation/completion)

### Request/Response Flow
- **Prompt processing**: 💭 (thought bubble for prompts)
- **Token generation**: ⚡ (fast generation)
- **Response completed**: ✨ (completion with flair)
- **Streaming response**: 🌊 (continuous flow)

### Performance Metrics
- **Token counting**: 🔢 (numerical tracking)
- **Latency measurement**: ⏱️ (timing operations)
- **Cost tracking**: 💰 (financial monitoring)
- **Rate limiting**: 🚦 (traffic control)

### Error States
- **Model timeout**: ⏰ (timeout issues)
- **Rate limit exceeded**: 🛑 (blocked requests)
- **Model error**: 💥 (processing failures)
- **Context length exceeded**: 📏 (length violations)

## Usage Examples

### Basic LLM Logging

```python
from provide.foundation import get_logger

# Create LLM-specific logger
llm_log = get_logger("llm")

# Model operations
llm_log.info("model_loaded", model="gpt-4", version="0613")
llm_log.debug("inference_started", prompt_tokens=150, model="gpt-4")
llm_log.info("inference_completed", 
             model="gpt-4", 
             prompt_tokens=150, 
             completion_tokens=75,
             duration_ms=1250)

# Error handling
llm_log.error("inference_failed", 
              model="gpt-4", 
              error="rate_limit_exceeded",
              retry_after=60)
```

### OpenAI Integration

```python
from provide.foundation import get_logger
from openai import OpenAI
import time

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI()
        self.log = get_logger("llm.openai")
    
    async def chat_completion(self, messages: list[dict], model: str = "gpt-4"):
        start_time = time.time()
        prompt_tokens = self._estimate_tokens(messages)
        
        self.log.info("chat_request_started",
                     model=model,
                     prompt_tokens=prompt_tokens,
                     message_count=len(messages))
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            
            duration_ms = (time.time() - start_time) * 1000
            
            self.log.info("chat_request_completed",
                         model=model,
                         prompt_tokens=response.usage.prompt_tokens,
                         completion_tokens=response.usage.completion_tokens,
                         total_tokens=response.usage.total_tokens,
                         duration_ms=round(duration_ms, 2))
            
            return response
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            self.log.error("chat_request_failed",
                          model=model,
                          error=str(e),
                          duration_ms=round(duration_ms, 2))
            raise
    
    def _estimate_tokens(self, messages: list[dict]) -> int:
        # Rough token estimation - 4 chars per token average
        total_chars = sum(len(msg.get("content", "")) for msg in messages)
        return total_chars // 4
```

### Anthropic Claude Integration

```python
from provide.foundation import get_logger
import anthropic
import time

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.log = get_logger("llm.claude")
    
    async def message_completion(self, messages: list[dict], model: str = "claude-3-sonnet-20240229"):
        start_time = time.time()
        
        self.log.info("claude_request_started",
                     model=model,
                     message_count=len(messages))
        
        try:
            message = await self.client.messages.create(
                model=model,
                max_tokens=1000,
                messages=messages
            )
            
            duration_ms = (time.time() - start_time) * 1000
            
            self.log.info("claude_request_completed",
                         model=model,
                         input_tokens=message.usage.input_tokens,
                         output_tokens=message.usage.output_tokens,
                         duration_ms=round(duration_ms, 2))
            
            return message
            
        except anthropic.RateLimitError as e:
            self.log.warning("claude_rate_limited",
                           model=model,
                           retry_after=e.retry_after,
                           error=str(e))
            raise
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            self.log.error("claude_request_failed",
                          model=model,
                          error=str(e),
                          error_type=type(e).__name__,
                          duration_ms=round(duration_ms, 2))
            raise
```

### Streaming Response Handling

```python
from provide.foundation import get_logger
import asyncio

class StreamingLLMClient:
    def __init__(self):
        self.log = get_logger("llm.streaming")
    
    async def stream_completion(self, prompt: str, model: str = "gpt-4"):
        start_time = time.time()
        tokens_streamed = 0
        
        self.log.info("stream_started",
                     model=model,
                     prompt_length=len(prompt))
        
        try:
            async for chunk in self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            ):
                if chunk.choices[0].delta.content:
                    tokens_streamed += 1
                    
                    # Log every 50 tokens to avoid spam
                    if tokens_streamed % 50 == 0:
                        self.log.debug("stream_progress",
                                     model=model,
                                     tokens_streamed=tokens_streamed,
                                     elapsed_ms=(time.time() - start_time) * 1000)
            
            duration_ms = (time.time() - start_time) * 1000
            tokens_per_second = tokens_streamed / (duration_ms / 1000) if duration_ms > 0 else 0
            
            self.log.info("stream_completed",
                         model=model,
                         tokens_streamed=tokens_streamed,
                         duration_ms=round(duration_ms, 2),
                         tokens_per_second=round(tokens_per_second, 2))
                         
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            self.log.error("stream_failed",
                          model=model,
                          tokens_streamed=tokens_streamed,
                          error=str(e),
                          duration_ms=round(duration_ms, 2))
            raise
```

### Model Management and Caching

```python
from provide.foundation import get_logger
import hashlib
import json

class LLMModelManager:
    def __init__(self):
        self.log = get_logger("llm.models")
        self.model_cache = {}
    
    async def load_model(self, model_name: str, config: dict = None):
        self.log.info("model_load_started", model=model_name)
        
        try:
            # Simulate model loading
            await asyncio.sleep(2)  # Model loading delay
            
            self.model_cache[model_name] = {
                "loaded_at": time.time(),
                "config": config or {},
                "status": "ready"
            }
            
            self.log.info("model_load_completed", 
                         model=model_name,
                         memory_usage_mb=self._get_model_memory(model_name))
                         
        except Exception as e:
            self.log.error("model_load_failed", 
                          model=model_name, 
                          error=str(e))
            raise
    
    def get_cached_response(self, prompt: str, model: str) -> str | None:
        cache_key = self._generate_cache_key(prompt, model)
        
        if cache_key in self.response_cache:
            self.log.debug("cache_hit", 
                          model=model,
                          cache_key=cache_key[:16])
            return self.response_cache[cache_key]
        else:
            self.log.debug("cache_miss",
                          model=model, 
                          cache_key=cache_key[:16])
            return None
    
    def cache_response(self, prompt: str, model: str, response: str):
        cache_key = self._generate_cache_key(prompt, model)
        self.response_cache[cache_key] = response
        
        self.log.debug("response_cached",
                      model=model,
                      cache_key=cache_key[:16],
                      response_length=len(response))
    
    def _generate_cache_key(self, prompt: str, model: str) -> str:
        return hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()
    
    def _get_model_memory(self, model_name: str) -> int:
        # Simulate memory usage calculation
        return hash(model_name) % 1000 + 500
```

### Cost Tracking and Monitoring

```python
from provide.foundation import get_logger
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class TokenCost:
    prompt_tokens: int
    completion_tokens: int
    prompt_cost_per_1k: Decimal
    completion_cost_per_1k: Decimal
    
    @property
    def total_cost(self) -> Decimal:
        prompt_cost = (self.prompt_tokens / 1000) * self.prompt_cost_per_1k
        completion_cost = (self.completion_tokens / 1000) * self.completion_cost_per_1k
        return prompt_cost + completion_cost

class LLMCostTracker:
    def __init__(self):
        self.log = get_logger("llm.costs")
        self.model_pricing = {
            "gpt-4": {"prompt": Decimal("0.03"), "completion": Decimal("0.06")},
            "gpt-3.5-turbo": {"prompt": Decimal("0.001"), "completion": Decimal("0.002")},
            "claude-3-sonnet": {"prompt": Decimal("0.015"), "completion": Decimal("0.075")}
        }
    
    def track_request_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> Decimal:
        if model not in self.model_pricing:
            self.log.warning("unknown_model_pricing", model=model)
            return Decimal("0")
        
        pricing = self.model_pricing[model]
        cost = TokenCost(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            prompt_cost_per_1k=pricing["prompt"],
            completion_cost_per_1k=pricing["completion"]
        )
        
        total_cost = cost.total_cost
        
        self.log.info("request_cost_calculated",
                     model=model,
                     prompt_tokens=prompt_tokens,
                     completion_tokens=completion_tokens,
                     total_tokens=prompt_tokens + completion_tokens,
                     cost_usd=float(total_cost),
                     cost_per_token_usd=float(total_cost / (prompt_tokens + completion_tokens)))
        
        # Alert on high-cost requests
        if total_cost > Decimal("1.00"):
            self.log.warning("high_cost_request",
                           model=model,
                           cost_usd=float(total_cost),
                           threshold_usd=1.00)
        
        return total_cost
    
    def track_daily_usage(self, user_id: str, total_cost: Decimal, request_count: int):
        self.log.info("daily_usage_summary",
                     user_id=user_id,
                     total_cost_usd=float(total_cost),
                     request_count=request_count,
                     average_cost_per_request=float(total_cost / request_count) if request_count > 0 else 0)
```

### Batch Processing and Queue Management

```python
from provide.foundation import get_logger
import asyncio
from asyncio import Queue

class LLMBatchProcessor:
    def __init__(self, max_concurrent: int = 5):
        self.log = get_logger("llm.batch")
        self.max_concurrent = max_concurrent
        self.request_queue = Queue()
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_batch(self, requests: list[dict]):
        self.log.info("batch_processing_started",
                     request_count=len(requests),
                     max_concurrent=self.max_concurrent)
        
        start_time = time.time()
        
        # Add all requests to queue
        for i, request in enumerate(requests):
            await self.request_queue.put((i, request))
        
        # Process requests concurrently
        tasks = []
        for _ in range(min(len(requests), self.max_concurrent)):
            task = asyncio.create_task(self._process_worker())
            tasks.append(task)
        
        # Wait for all requests to be processed
        await self.request_queue.join()
        
        # Cancel workers
        for task in tasks:
            task.cancel()
        
        duration_ms = (time.time() - start_time) * 1000
        
        self.log.info("batch_processing_completed",
                     request_count=len(requests),
                     duration_ms=round(duration_ms, 2),
                     requests_per_second=round(len(requests) / (duration_ms / 1000), 2))
    
    async def _process_worker(self):
        while True:
            try:
                request_id, request_data = await self.request_queue.get()
                
                async with self.semaphore:
                    await self._process_single_request(request_id, request_data)
                
                self.request_queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.log.error("batch_request_failed",
                              request_id=request_id,
                              error=str(e))
                self.request_queue.task_done()
    
    async def _process_single_request(self, request_id: int, request_data: dict):
        self.log.debug("batch_request_started", request_id=request_id)
        
        try:
            # Simulate LLM request processing
            await asyncio.sleep(1)  # Simulated processing time
            
            self.log.debug("batch_request_completed", request_id=request_id)
            
        except Exception as e:
            self.log.error("batch_request_error", 
                          request_id=request_id,
                          error=str(e))
            raise
```

## Performance Monitoring

### Latency and Throughput Tracking

```python
from provide.foundation import get_logger
import time
from collections import defaultdict, deque
from typing import defaultdict as DefaultDict

class LLMPerformanceMonitor:
    def __init__(self, window_size: int = 100):
        self.log = get_logger("llm.performance")
        self.window_size = window_size
        self.response_times: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=window_size))
        self.request_counts: DefaultDict[str, int] = defaultdict(int)
        self.error_counts: DefaultDict[str, int] = defaultdict(int)
    
    def record_request(self, model: str, duration_ms: float, success: bool = True):
        self.response_times[model].append(duration_ms)
        self.request_counts[model] += 1
        
        if not success:
            self.error_counts[model] += 1
        
        # Calculate and log performance metrics
        if len(self.response_times[model]) >= 10:  # Wait for some data
            self._log_performance_metrics(model)
    
    def _log_performance_metrics(self, model: str):
        times = list(self.response_times[model])
        
        avg_latency = sum(times) / len(times)
        p50_latency = sorted(times)[len(times) // 2]
        p95_latency = sorted(times)[int(len(times) * 0.95)]
        p99_latency = sorted(times)[int(len(times) * 0.99)]
        
        error_rate = (self.error_counts[model] / self.request_counts[model]) * 100
        
        self.log.info("performance_metrics",
                     model=model,
                     request_count=self.request_counts[model],
                     avg_latency_ms=round(avg_latency, 2),
                     p50_latency_ms=round(p50_latency, 2),
                     p95_latency_ms=round(p95_latency, 2),
                     p99_latency_ms=round(p99_latency, 2),
                     error_rate_percent=round(error_rate, 2))
        
        # Alert on performance issues
        if avg_latency > 5000:  # 5 second average
            self.log.warning("high_average_latency",
                           model=model,
                           avg_latency_ms=round(avg_latency, 2),
                           threshold_ms=5000)
        
        if error_rate > 5:  # 5% error rate
            self.log.warning("high_error_rate",
                           model=model,
                           error_rate_percent=round(error_rate, 2),
                           threshold_percent=5)
```

## Configuration

### Enabling LLM Emoji Set

```python
from provide.foundation.logger.config import TelemetryConfig, LoggingConfig
from provide.foundation.setup import setup_telemetry

config = TelemetryConfig(
    logging=LoggingConfig(
        default_level="INFO",
        das_emoji_prefix_enabled=True,
        enabled_emoji_sets=["llm"]
    )
)
setup_telemetry(config)
```

### Custom LLM Emoji Set

```python
from provide.foundation.logger.emoji.types import EmojiSetConfig

class CustomLLMEmojiSet(EmojiSetConfig):
    """Custom LLM emoji set with additional model-specific mappings."""
    
    domain = "llm"
    
    def get_emoji(self, action: str, status: str) -> str:
        # Custom mappings for specific models
        if "gpt-4" in action and status == "success":
            return "🤖✨"
        elif "claude" in action and status == "success":
            return "🧠💫"
        elif "local" in action:  # Local model inference
            return "🏠🤖" if status == "success" else "🏠❌"
        elif action.startswith("fine_tune"):
            return "🎯" if status == "success" else "💥"
        elif action.startswith("embedding"):
            return "📊" if status == "success" else "📉"
        else:
            # Fallback to standard LLM emojis
            return super().get_emoji(action, status)

# Use custom emoji set
config = TelemetryConfig(
    logging=LoggingConfig(
        custom_emoji_sets=[CustomLLMEmojiSet()]
    )
)
```

## Best Practices

### 1. Log Levels for LLM Operations

```python
# DEBUG: Token counts, cache operations, detailed request info
llm_log.debug("token_count", prompt_tokens=150, model="gpt-4")

# INFO: Request completion, model loading, performance metrics
llm_log.info("inference_completed", model="gpt-4", duration_ms=1200)

# WARNING: High costs, slow responses, rate limit warnings
llm_log.warning("high_cost_request", cost_usd=5.50, threshold_usd=1.00)

# ERROR: Failed requests, model errors, timeout issues
llm_log.error("model_timeout", model="gpt-4", timeout_seconds=30)
```

### 2. Sensitive Data Handling

```python
# Good: Log metadata, not sensitive content
llm_log.info("request_completed", 
             model="gpt-4", 
             prompt_length=len(prompt),
             response_length=len(response))

# Avoid: Logging sensitive prompts or responses
# llm_log.info("request_completed", prompt=user_prompt, response=model_response)
```

### 3. Structured Context

```python
# Use consistent field names for LLM operations
llm_log.info("model_inference_completed",
           model="gpt-4",
           prompt_tokens=150,
           completion_tokens=75,
           total_tokens=225,
           duration_ms=1250,
           cost_usd=0.0135)
```

## Related Documentation

- [api-Base Emoji Types](base.md) - Core emoji system interfaces
- [api-Custom Emoji Sets](custom.md) - Creating custom emoji sets
- [api-HTTP Emoji Set](http.md) - Web request logging emojis
- [api-Database Emoji Set](database.md) - Database operation emojis
- [Testing Guide](../../guide/testing.md) - Testing LLM logging