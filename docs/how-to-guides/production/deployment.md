# Deployment Patterns

Learn best practices for deploying Foundation applications to production environments with Docker, Kubernetes, and cloud platforms.

## Overview

Deploying Foundation applications to production requires careful consideration of configuration management, secret handling, logging, health checks, and scaling. This guide provides battle-tested deployment patterns for containerized environments, cloud platforms, and orchestration systems.

**What you'll learn:**
- Build production Docker images
- Deploy to Kubernetes with best practices
- Manage secrets securely
- Configure multi-environment deployments
- Implement zero-downtime deployments
- Set up auto-scaling
- Handle graceful shutdown
- Monitor deployments

**Key Features:**
- 🐳 **Docker**: Optimized multi-stage builds
- ☸️ **Kubernetes**: Production-focused manifests
- 🔒 **Secret Management**: Secure secret handling
- 🌍 **Multi-Environment**: Dev, staging, production configs
- 🚀 **Zero-Downtime**: Rolling updates and health checks
- 📈 **Auto-Scaling**: HPA and resource management
- 🛡️ **Security**: Non-root users, minimal images

## Prerequisites

```bash
# Required tools
docker --version
kubectl version --client
helm version

# Foundation with production extras
uv add provide-foundation[production]
```

## Docker Deployment

### Production Dockerfile

Build optimized Docker images:

```dockerfile
# Multi-stage build for smaller images
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy dependency files
WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.11-slim

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ /app/src/
COPY examples/ /app/examples/

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PROVIDE_LOG_LEVEL=INFO \
    PROVIDE_LOG_FORMAT=json

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health/live')"

# Run application
CMD ["python", "-m", "myapp"]
```

### Docker Compose for Local Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder  # Use builder stage for development
    volumes:
      - ./src:/app/src:ro
      - ./examples:/app/examples:ro
    environment:
      PROVIDE_LOG_LEVEL: DEBUG
      PROVIDE_LOG_FORMAT: console
      PROVIDE_SERVICE_NAME: myapp-dev
      DATABASE_URL: postgresql://user:pass@db:5432/myapp
      REDIS_URL: redis://redis:6379/0
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    command: python -m myapp

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Building and Publishing Images

```bash
# Build production image
docker build -t myapp:1.0.0 -t myapp:latest .

# Tag for registry
docker tag myapp:1.0.0 registry.example.com/myapp:1.0.0

# Push to registry
docker push registry.example.com/myapp:1.0.0
docker push registry.example.com/myapp:latest

# Scan for vulnerabilities
docker scan myapp:1.0.0
```

## Kubernetes Deployment

### Production Deployment Manifest

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime deployments
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      # Use service account with minimal permissions
      serviceAccountName: myapp

      # Run as non-root user
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      containers:
      - name: app
        image: registry.example.com/myapp:1.0.0
        imagePullPolicy: Always

        # Resource limits and requests
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

        # Environment variables
        env:
        - name: PROVIDE_LOG_LEVEL
          value: "INFO"
        - name: PROVIDE_LOG_FORMAT
          value: "json"
        - name: PROVIDE_SERVICE_NAME
          value: "myapp"
        - name: ENVIRONMENT
          value: "production"
        - name: APP_VERSION
          value: "1.0.0"

        # Secrets from Kubernetes secrets
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database_url
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: api_key

        # ConfigMap values
        - name: FEATURE_FLAGS
          valueFrom:
            configMapKeyRef:
              name: myapp-config
              key: feature_flags

        # Application port
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP

        # Liveness probe - is the app alive?
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 10
          periodSeconds: 30
          timeoutSeconds: 3
          failureThreshold: 3

        # Readiness probe - is the app ready for traffic?
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 2

        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]

        # Mount volumes
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
        - name: secrets
          mountPath: /app/secrets
          readOnly: true

      volumes:
      - name: config
        configMap:
          name: myapp-config
      - name: secrets
        secret:
          secretName: myapp-secrets

      # Image pull secrets
      imagePullSecrets:
      - name: registry-credentials

      # Spread pods across nodes
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp
              topologyKey: kubernetes.io/hostname
```

### Service and Ingress

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
spec:
  type: ClusterIP
  ports:
  - name: http
    port: 80
    targetPort: 8000
    protocol: TCP
  - name: metrics
    port: 9090
    targetPort: 9090
    protocol: TCP
  selector:
    app: myapp

---
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp
            port:
              number: 80
```

### Horizontal Pod Autoscaler

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Max
```

## Secret Management

### Kubernetes Secrets

```yaml
# secrets.yaml (encrypted with Sealed Secrets or SOPS)
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
  namespace: production
type: Opaque
stringData:
  database_url: "postgresql://user:password@postgres:5432/myapp"
  api_key: "sk_live_abc123xyz"
  redis_url: "redis://:password@redis:6379/0"
```

### Using file:// Prefix for Secrets

Foundation supports reading secrets from files:

```python
# Application code
import os

# Kubernetes mounts secrets as files
os.environ["DATABASE_PASSWORD"] = "file:///run/secrets/db_password"
os.environ["API_KEY"] = "file:///run/secrets/api_key"

# Foundation automatically reads from files
from provide.foundation.utils.environment import get_str

db_password = get_str("DATABASE_PASSWORD")  # Reads from /run/secrets/db_password
api_key = get_str("API_KEY")  # Reads from /run/secrets/api_key
```

### External Secrets Operator

```yaml
# external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: ClusterSecretStore
  target:
    name: myapp-secrets
    creationPolicy: Owner
  data:
  - secretKey: database_url
    remoteRef:
      key: prod/myapp/database_url
  - secretKey: api_key
    remoteRef:
      key: prod/myapp/api_key
```

## Multi-Environment Configuration

### Environment-Specific Configs

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

commonLabels:
  app: myapp
  environment: production

resources:
- deployment.yaml
- service.yaml
- ingress.yaml
- hpa.yaml

configMapGenerator:
- name: myapp-config
  literals:
  - PROVIDE_LOG_LEVEL=INFO
  - PROVIDE_LOG_FORMAT=json
  - FEATURE_FLAGS={"new_ui":true,"beta":false}

secretGenerator:
- name: myapp-secrets
  files:
  - database_url=secrets/prod/database_url
  - api_key=secrets/prod/api_key

images:
- name: registry.example.com/myapp
  newTag: 1.0.0

replicas:
- name: myapp
  count: 5
```

### Overlays for Environments

```bash
# Directory structure
k8s/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── production/
        └── kustomization.yaml

# Deploy to staging
kubectl apply -k k8s/overlays/staging

# Deploy to production
kubectl apply -k k8s/overlays/production
```

## Zero-Downtime Deployments

### Rolling Update Strategy

```python
# In your application
from provide.foundation import get_hub, logger
import signal
import sys

hub = get_hub()

def graceful_shutdown(signum, frame):
    """Handle graceful shutdown."""
    logger.info("shutdown_signal_received", signal=signum)

    # Stop accepting new requests
    logger.info("stopping_http_server")
    http_server.stop()

    # Wait for in-flight requests to complete
    logger.info("waiting_for_requests", timeout=30)
    http_server.wait_for_completion(timeout=30)

    # Cleanup resources
    logger.info("cleaning_up_resources")
    hub.shutdown()

    logger.info("shutdown_complete")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

logger.info("application_started", version=os.getenv("APP_VERSION"))
```

### PreStop Hook

```yaml
# In deployment.yaml
lifecycle:
  preStop:
    exec:
      # Sleep to allow load balancer to remove pod
      command: ["/bin/sh", "-c", "sleep 15"]
```

## Helm Charts

### Chart Structure

```yaml
# Chart.yaml
apiVersion: v2
name: myapp
description: My Foundation Application
version: 1.0.0
appVersion: "1.0.0"

---
# values.yaml
replicaCount: 3

image:
  repository: registry.example.com/myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

env:
  PROVIDE_LOG_LEVEL: INFO
  PROVIDE_LOG_FORMAT: json
  PROVIDE_SERVICE_NAME: myapp
```

### Installing with Helm

```bash
# Install
helm install myapp ./myapp-chart \
  --namespace production \
  --create-namespace \
  --values values-prod.yaml

# Upgrade
helm upgrade myapp ./myapp-chart \
  --namespace production \
  --values values-prod.yaml

# Rollback if needed
helm rollback myapp 1 --namespace production
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Registry
        uses: docker/login-action@v2
        with:
          registry: registry.example.com
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Extract version
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            registry.example.com/myapp:${{ steps.version.outputs.VERSION }}
            registry.example.com/myapp:latest
          cache-from: type=registry,ref=registry.example.com/myapp:buildcache
          cache-to: type=registry,ref=registry.example.com/myapp:buildcache,mode=max

      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/production/deployment.yaml
            k8s/production/service.yaml
          images: registry.example.com/myapp:${{ steps.version.outputs.VERSION }}
          kubectl-version: latest
```

## Best Practices

### ✅ DO: Use Non-Root Users

```dockerfile
# ✅ GOOD: Run as non-root
RUN useradd -m -u 1000 appuser
USER appuser
```

### ❌ DON'T: Run as Root

```dockerfile
# ❌ BAD: Security risk
USER root  # Don't run containers as root!
```

### ✅ DO: Set Resource Limits

```yaml
# ✅ GOOD: Define resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### ❌ DON'T: Omit Resource Limits

```yaml
# ❌ BAD: No limits can cause node instability
resources: {}  # Missing limits!
```

### ✅ DO: Implement Health Checks

```yaml
# ✅ GOOD: Both liveness and readiness
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
```

### ❌ DON'T: Skip Health Checks

```yaml
# ❌ BAD: No way to detect unhealthy pods
# Missing probes!
```

### ✅ DO: Use Multi-Stage Builds

```dockerfile
# ✅ GOOD: Smaller final image
FROM python:3.11-slim as builder
# ... build steps ...

FROM python:3.11-slim
COPY --from=builder /app/.venv /app/.venv
```

### ❌ DON'T: Include Build Tools in Production

```dockerfile
# ❌ BAD: Unnecessarily large image
FROM python:3.11
RUN apt-get install build-essential  # Not needed in production!
```

### ✅ DO: Version Your Images

```bash
# ✅ GOOD: Semantic versioning
docker tag myapp:1.2.3 registry.example.com/myapp:1.2.3
```

### ❌ DON'T: Use Only 'latest'

```bash
# ❌ BAD: Can't rollback or track versions
docker tag myapp registry.example.com/myapp:latest  # Only using latest!
```

### ✅ DO: Manage Secrets Securely

```yaml
# ✅ GOOD: Use Kubernetes secrets
env:
- name: API_KEY
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: api_key
```

### ❌ DON'T: Hardcode Secrets

```yaml
# ❌ BAD: Secrets in plain text
env:
- name: API_KEY
  value: "sk_live_abc123"  # NEVER do this!
```

### ✅ DO: Configure Graceful Shutdown

```python
# ✅ GOOD: Handle SIGTERM gracefully
def graceful_shutdown(signum, frame):
    logger.info("shutting_down")
    server.stop()
    cleanup_resources()
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)
```

### ❌ DON'T: Ignore Shutdown Signals

```python
# ❌ BAD: Abrupt shutdown can lose data
# No signal handling = killed immediately
```

## Next Steps

### Related Guides
- **[Monitoring & Observability](monitoring.md)**: Monitor production deployments
- **[Basic Logging](../logging/basic-logging.md)**: Production logging setup
- **[Configuration](../configuration/env-variables.md)**: Environment configuration

### Examples
- See `examples/deployment/` for deployment templates
- See `examples/production/10_graceful_shutdown.py` for shutdown patterns

### API Reference
- **[Hub API](../../reference/provide/foundation/hub/index.md)**: Application lifecycle
- **[Config API](../../reference/provide/foundation/config/index.md)**: Configuration management

---

**Tip**: Start with Docker Compose for local development, then move to Kubernetes for production. Always use health checks, resource limits, and graceful shutdown. Implement rolling updates for zero-downtime deployments. Keep secrets in secure stores, never in code or config files.
