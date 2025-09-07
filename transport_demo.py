#!/usr/bin/env python3
"""
Transport system demonstration.
"""

import asyncio
import os

# Set environment variables for configuration
os.environ["TRANSPORT_TIMEOUT"] = "10.0"
os.environ["HTTP_POOL_CONNECTIONS"] = "5"


async def demo():
    """Demonstrate the transport system."""
    from provide.foundation.transport import get, post, UniversalClient
    from provide.foundation.transport import list_registered_transports
    from provide.foundation.logger import get_logger
    
    log = get_logger("transport-demo")
    
    print("\n🚀 Transport System Demo\n")
    
    # Show registered transports
    print("📋 Registered Transports:")
    transports = list_registered_transports()
    for name, info in transports.items():
        schemes = ", ".join(info["schemes"])
        print(f"  • {name}: {schemes}")
    
    print("\n🌐 Making HTTP requests...")
    
    try:
        # Simple GET request using convenience function
        print("Making GET request to httpbin.org...")
        response = await get("https://httpbin.org/get", params={"test": "value"})
        print(f"✅ Status: {response.status}")
        data = response.json()
        print(f"   URL called: {data['url']}")
        
        # POST request with JSON body
        print("\nMaking POST request...")
        response = await post(
            "https://httpbin.org/post",
            body={"message": "Hello from provide.foundation.transport!", "demo": True},
            headers={"User-Agent": "ProvideFoundation/1.0"}
        )
        print(f"✅ Status: {response.status}")
        data = response.json()
        print(f"   Received: {data['json']['message']}")
        
        # Using UniversalClient for multiple requests
        print("\n🔄 Using client for multiple requests...")
        async with UniversalClient() as client:
            # Multiple requests with connection reuse
            for i in range(3):
                response = await client.get(f"https://httpbin.org/delay/{i}")
                print(f"   Request {i+1}: {response.status} ({response.elapsed_ms:.0f}ms)")
        
        print("\n✨ Transport system demo completed successfully!")
        
    except Exception as e:
        log.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    asyncio.run(demo())