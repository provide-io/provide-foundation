#!/bin/bash
# Run act with Colima-specific configuration
# This script ensures act works properly with Colima's Docker socket

# Set Docker host to the actual Colima socket location
export DOCKER_HOST="unix:///Users/tim/.colima/default/docker.sock"

# Run act without trying to mount the Docker socket into containers
# The "-" value disables bind mounting the socket per act documentation
exec act --container-daemon-socket - "$@"