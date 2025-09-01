#!/bin/bash
# Run act with Colima-specific configuration
# This script ensures act works properly with Colima's Docker socket

# Set the Docker host to Colima's socket location
export DOCKER_HOST="unix:///Users/tim/.colima/default/docker.sock"

# Run act with disabled daemon socket mounting
# The --container-daemon-socket "" flag prevents act from trying to mount the Docker socket
# which causes issues with Colima's virtualization layer
exec act --container-daemon-socket "" "$@"