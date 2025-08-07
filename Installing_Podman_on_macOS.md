# Installing and Running Podman on macOS

## Overview
This guide covers how to install Podman on macOS and use it to run a Django application with PostgreSQL using container orchestration.

## Prerequisites
- macOS system with Homebrew installed
- Terminal access
- Docker-style container knowledge (helpful but not required)

## 1. Installing Podman

### Option 1: Using Homebrew (Recommended)
```bash
# Install Podman
brew install podman

# Verify installation
podman --version
```

### Option 2: Using the Official Installer
- Download from: https://podman.io/getting-started/installation
- Follow the macOS installer instructions

## 2. Setting Up Podman Machine

Podman on macOS requires a virtual machine to run Linux containers:

```bash
# Initialize the Podman machine
podman machine init

# Start the Podman machine
podman machine start
```

**Expected Output:**
```
Machine init complete
To start your machine run:
    podman machine start

Starting machine "podman-machine-default"
Machine "podman-machine-default" started successfully
```

## 3. Podman Compose Options

You have two options for running multi-container applications with Podman:

### Option A: Built-in Podman Compose (Recommended)
Podman includes built-in Docker Compose compatibility:
- **No separate installation needed** - `podman compose` is included with Podman
- Compatible with existing `docker-compose.yml` files
- Uses the same syntax and commands as Docker Compose

### Option B: Standalone podman-compose
If you prefer the standalone `podman-compose` tool:

#### Installing podman-compose
```bash
# Install using pip
pip3 install podman-compose

# Or install using pipx (recommended for isolation)
pipx install podman-compose

# Verify installation
podman-compose --version
```

#### Alternative Installation Methods
```bash
# Using Homebrew (if available)
brew install podman-compose

# Using package manager on Linux
# Fedora/RHEL
sudo dnf install podman-compose

# Ubuntu/Debian
sudo apt install podman-compose
```

### Key Differences Between Options

| Feature | `podman compose` | `podman-compose` |
|---------|------------------|------------------|
| Installation | Built-in with Podman | Separate installation required |
| Command format | `podman compose` | `podman-compose` |
| Compatibility | Docker Compose v2 syntax | Docker Compose v1/v2 syntax |
| Maintenance | Maintained by Podman team | Community-maintained |
| Performance | Faster (native integration) | Slightly slower (wrapper) |

## 4. Running Your Application

### Method 1: Using Built-in podman compose (Recommended)

#### Build the Containers
```bash
podman compose -f podman-compose.yml build
```

#### Start the Services
```bash
podman compose -f podman-compose.yml up -d
```

#### Verify Everything is Running
```bash
podman compose -f podman-compose.yml ps
```

### Method 2: Using Standalone podman-compose

#### Build the Containers
```bash
podman-compose -f podman-compose.yml build
```

#### Start the Services
```bash
podman-compose -f podman-compose.yml up -d
```

#### Verify Everything is Running
```bash
podman-compose -f podman-compose.yml ps
```

## 5. Common Commands

### Using Built-in podman compose
```bash
# View application logs
podman compose -f podman-compose.yml logs web

# Stop all containers
podman compose -f podman-compose.yml down

# Start containers (after they've been built)
podman compose -f podman-compose.yml up -d

# Rebuild and restart
podman compose -f podman-compose.yml up -d --build

# View all running containers
podman ps

# Execute commands in running container
podman exec -it django-app bash
```

### Using Standalone podman-compose
```bash
# View application logs
podman-compose -f podman-compose.yml logs web

# Stop all containers
podman-compose -f podman-compose.yml down

# Start containers (after they've been built)
podman-compose -f podman-compose.yml up -d

# Rebuild and restart
podman-compose -f podman-compose.yml up -d --build

# View all running containers
podman ps

# Execute commands in running container
podman exec -it django-app bash
```

### Universal Commands (Work with Both Methods)
```bash
# View all running containers
podman ps

# View container logs directly
podman logs django-app

# Execute commands in running container
podman exec -it django-app bash

# Stop a specific container
podman stop django-app

# Remove containers
podman rm django-app moravian-db-1
```

## 6. Key Differences from Docker

| Feature | Docker | Podman |
|---------|--------|--------|
| Daemon | Requires Docker daemon | Daemonless |
| Root privileges | Often requires sudo | Runs rootless by default |
| Compose command | `docker-compose` or `docker compose` | `podman compose` |
| Machine setup | Docker Desktop | `podman machine` |

## 7. Troubleshooting

### Common Issues and Solutions

**Issue: "podman-compose: command not found"**
- **Solution 1**: Use `podman compose` (built-in, without hyphen) instead of `podman-compose`
- **Solution 2**: Install standalone `podman-compose` using `pip3 install podman-compose`

**Issue: "no configuration file provided"**
- Solution: Always specify the compose file: `-f podman-compose.yml`

**Issue: Permission errors**
- Solution: Ensure Podman machine is running: `podman machine start`

**Issue: Port conflicts**
- Solution: Check if ports are already in use: `lsof -i :8000`

**Issue: "Error: short-name resolution enforced but cannot prompt"**
- Solution: Use full image names in your compose file (e.g., `docker.io/library/postgres:16`)

**Issue: Container fails to start with podman-compose**
- Solution: Try using the built-in `podman compose` instead, as it has better integration

### Which Method Should I Use?

**Use `podman compose` (built-in) if:**
- You want the most stable and well-maintained option
- You're starting a new project
- You want the fastest performance
- You prefer fewer dependencies

**Use `podman-compose` (standalone) if:**
- You're migrating from Docker Compose and need specific compatibility
- Your existing scripts use `podman-compose`
- You need features specific to the standalone version

## 8. Project Structure for This Setup

```
moravian/
├── podman-compose.yml      # Container orchestration
├── Dockerfile             # Django app container definition
├── entrypoint.sh          # Container startup script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── moravian/              # Django project files
    ├── manage.py
    └── ...
```

## 9. Environment Configuration

The application uses these key environment variables (from `.env`):
```env
DB_LOCAL_NAME=moravian
DB_LOCAL_USER=moravianuser
DB_LOCAL_PASS=moravian_test
HOST=db
PORT=5432
DJANGO_SETTINGS_MODULE=moravian.settings.development
```

## 10. Accessing Your Application

Once running:
- **Main Application**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
  - Username: `moravian_admin`
  - Password: `adminpass_test`

## Benefits of Using Podman

1. **Security**: Runs without root privileges
2. **Compatibility**: Drop-in replacement for Docker
3. **No daemon**: Lighter resource usage
4. **Native systemd integration**: Better for production Linux deployments
5. **Pod support**: Kubernetes-like pod functionality