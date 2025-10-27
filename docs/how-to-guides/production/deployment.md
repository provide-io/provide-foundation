# Deployment Patterns

Learn best practices for deploying Foundation applications to production.

## Overview

Foundation applications are designed for production deployment with proper logging, configuration, and error handling.

## Container Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Set production environment
ENV PROVIDE_LOG_LEVEL=INFO
ENV PROVIDE_LOG_FORMAT=json

CMD ["python", "app.py"]
```

## Environment Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      PROVIDE_LOG_LEVEL: INFO
      PROVIDE_LOG_FORMAT: json
      PROVIDE_SERVICE_NAME: my-app
      DATABASE_URL: file:///run/secrets/db_url
    secrets:
      - db_url

secrets:
  db_url:
    file: ./secrets/database_url.txt
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: app
        image: my-app:latest
        env:
        - name: PROVIDE_LOG_LEVEL
          value: "INFO"
        - name: PROVIDE_LOG_FORMAT
          value: "json"
        - name: DB_PASSWORD
          value: "file:///secrets/db_password"
        volumeMounts:
        - name: secrets
          mountPath: /secrets
          readOnly: true
      volumes:
      - name: secrets
        secret:
          secretName: app-secrets
```

## Next Steps

- **[Monitoring & Observability](monitoring.md)** - Production monitoring
- **[Secret Management](../configuration/secrets.md)** - Handle secrets
