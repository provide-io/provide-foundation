#!/usr/bin/env python3
"""Test script to debug OTLP headers."""

from provide.foundation.integrations.openobserve.config import OpenObserveConfig
from provide.foundation.integrations.openobserve.otlp_adapter import (
    OpenObserveOTLPClient,
    build_openobserve_headers,
)
from provide.foundation.logger.config.telemetry import TelemetryConfig

# Load configs
oo_config = OpenObserveConfig.from_env()
telemetry_config = TelemetryConfig.from_env()

print("=== OpenObserve Config ===")
print(f"URL: {oo_config.url}")
print(f"Org: {oo_config.org}")
print(f"User: {oo_config.user}")
print(f"Password: {'***' if oo_config.password else None}")
print(f"Stream: {oo_config.stream}")
print(f"Is configured: {oo_config.is_configured()}")

print("\n=== Headers from build_openobserve_headers ===")
headers = build_openobserve_headers(oo_config)
for key, value in headers.items():
    if "auth" in key.lower():
        print(f"{key}: {value[:20]}..." if len(value) > 20 else f"{key}: {value}")
    else:
        print(f"{key}: {value}")

print("\n=== Client Creation ===")
try:
    client = OpenObserveOTLPClient.from_env()
    if client:
        print(f"Client created successfully")
        print(f"Endpoint: {client.endpoint}")
        print(f"Headers: {list(client.headers.keys())}")
        for key, value in client.headers.items():
            if "auth" in key.lower():
                print(f"  {key}: {value[:20]}..." if len(value) > 20 else f"  {key}: {value}")
            else:
                print(f"  {key}: {value}")
    else:
        print("Client is None")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
