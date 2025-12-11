# NetBox SCION Plugin - Advanced Deployment Guide

This guide covers advanced installation methods, custom Docker builds, local development, and detailed troubleshooting.

> **Prerequisites:** Before using this guide, complete the basic installation from the main [README.md](../README.md).

This guide is for users who need:
- Local development with custom wheel files
- Alternative installation methods (pip fallback)
- Detailed troubleshooting and debugging
- Custom Docker image builds
- Development and testing workflows

## Advanced Deployment Methods

### Method 1: Local Development with Wheel File

For testing local changes or unreleased versions.

#### Setup:

**1. Copy your wheel file:**
```bash
# Copy your built wheel to plugins/ directory
# Replace X.Y with your actual version number
cp netbox_scion-X.Y-py3-none-any.whl plugins/
```

**2. Use local Dockerfile:**
```dockerfile
# Dockerfile.netbox-local
FROM netboxcommunity/netbox:latest

COPY plugins/*.whl /tmp/
RUN /usr/local/bin/uv pip install /tmp/*.whl
```

**3. Build and run:**
```bash
docker build -f Dockerfile.netbox-local -t netbox-scion-dev .
# Update your docker-compose to use this image
```

### Method 2: Alternative with pip (Fallback)

If the `uv` package manager is not available in your NetBox Docker image:

```dockerfile
# Dockerfile.netbox-pip
FROM netboxcommunity/netbox:latest

USER root
RUN apt-get update && apt-get install -y python3-pip && \
    rm -rf /var/lib/apt/lists/*
RUN pip install netbox-scion==X.Y
```

Then rebuild your containers:
```bash
docker-compose build
docker-compose up -d
```

## Development and Testing

### Local Development Setup

**1. Clone and setup:**
```bash
git clone https://github.com/anapaya/netbox-scion.git
cd netbox-scion

# Install in development mode
pip install -e .
```

**2. Build wheel for testing:**
```bash
python setup.py bdist_wheel
cp dist/netbox_scion-*.whl deployment/plugins/
```

**3. Test with local deployment:**
```bash
# Copy deployment files to your netbox-docker
cp -r deployment/* /path/to/your/netbox-docker/

# Use local development Dockerfile
cd /path/to/your/netbox-docker
docker-compose -f docker-compose.yml -f docker-compose.override.yml build
docker-compose up -d
```

### Testing Changes

**Quick test cycle:**
```bash
# Make changes to plugin code
# Rebuild wheel
python setup.py bdist_wheel && cp dist/netbox_scion-*.whl deployment/plugins/

# Rebuild and restart containers
cd /path/to/your/netbox-docker
docker-compose build netbox netbox-worker
docker-compose restart netbox netbox-worker
```

## Advanced Troubleshooting

> For basic troubleshooting, see the main [README.md](../README.md).

### Deep Debugging

**Check Python import chain:**
```bash
docker exec netbox python -c "import netbox_scion; print(netbox_scion.__version__)"
```

**Inspect loaded plugins:**
```bash
docker exec netbox python /opt/netbox/netbox/manage.py shell -c "from django.conf import settings; print(settings.PLUGINS)"
```

**View detailed logs:**
```bash
# Docker: Full logs with timestamps
docker logs --tail=100 -f netbox 2>&1 | grep -i "scion\|plugin\|error"

# System: Journal logs with plugin context
sudo journalctl -u netbox -n 100 -f | grep -i "scion\|plugin"
```

### Common Advanced Issues

**1. Database migration conflicts:**
```bash
# Show all migrations
docker exec netbox python /opt/netbox/netbox/manage.py showmigrations

# Fake a specific migration if needed (use with caution)
docker exec netbox python /opt/netbox/netbox/manage.py migrate netbox_scion --fake

# Rollback to specific migration
docker exec netbox python /opt/netbox/netbox/manage.py migrate netbox_scion 0017
```

**2. Plugin version mismatches:**
```bash
# Check installed vs required version
docker exec netbox pip list | grep netbox-scion
docker exec netbox cat /opt/netbox/plugin_requirements.txt | grep netbox-scion

# Force reinstall specific version
docker exec netbox pip install --force-reinstall netbox-scion==X.Y
```

**3. Custom field conflicts:**
```bash
# Inspect custom fields
docker exec netbox python /opt/netbox/netbox/manage.py shell -c \
  "from extras.models import CustomField; print(list(CustomField.objects.filter(name__icontains='scion').values()))"
```

**4. API endpoint not responding:**
```bash
# Test API endpoint directly
curl -H "Authorization: Token YOUR_TOKEN" \
     -H "Accept: application/json" \
     http://your-netbox/api/plugins/scion/organizations/

# Check Django URL patterns
docker exec netbox python /opt/netbox/netbox/manage.py show_urls | grep scion
```

## Support

**For issues:**
- [GitHub Issues](https://github.com/anapaya/netbox-scion/issues)
- [GitHub Discussions](https://github.com/anapaya/netbox-scion/discussions)
- [Main README](../README.md)

**Legacy Installation Cleanup:**
If upgrading from older versions:
```bash
# Remove old installations
pip uninstall netbox-scion
pip install netbox-scion==X.Y

# Clear Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

## 📚 API Documentation

For complete API documentation including authentication, request/response examples, filtering, error handling, and Python code samples, see:

**➡️ [API.md](../API.md)** - Comprehensive REST API Documentation

The API.md file includes:
- Complete endpoint reference for Organizations, ISD-ASes, and SCION Links
- Authentication methods (Token and Session)
- Full request/response examples with curl
- Filtering and search parameters
- Pagination and export formats
- Error handling and validation rules
- Python code examples using requests library

---

**For standard installation, see the main [README.md](../README.md).**
