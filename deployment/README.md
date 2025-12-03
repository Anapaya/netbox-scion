# NetBox SCION Plugin - Advanced Deployment Guide

This guide covers advanced installation methods, custom Docker builds, local development, and detailed troubleshooting for the NetBox SCION plugin.

**For simple installation, see the main [README.md](../README.md) first.**

## 🚀 Deployment Methods

### Method 1: Production Deployment (Recommended)

This is the recommended production approach using a custom Dockerfile.

#### Files Required:
- `Dockerfile-Plugins` - Main production Dockerfile
- `plugin_requirements.txt` - Plugin dependencies
- `docker-compose.override.yml` - Docker compose overrides

#### Setup:

**1. Create plugin requirements file:**
```bash
# Create plugin_requirements.txt in your netbox-docker directory
echo "netbox-scion==1.3.2" > plugin_requirements.txt
```

**2. Create Dockerfile-Plugins:**
```dockerfile
FROM netboxcommunity/netbox:latest

COPY plugin_requirements.txt /opt/netbox/
RUN /usr/local/bin/uv pip install -r /opt/netbox/plugin_requirements.txt
```

**3. Configure plugins:**
```python
# Edit configuration/plugins.py
PLUGINS = [
    'netbox_scion',
    # Your other plugins...
]
```

**4. Create docker-compose.override.yml:**
```yaml
services:
  netbox:
    build:
      context: .
      dockerfile: Dockerfile-Plugins
  netbox-worker:
    build:
      context: .
      dockerfile: Dockerfile-Plugins
```

**5. Build and deploy:**
```bash
docker-compose build
docker-compose up -d
```

### Method 2: Local Development with Wheel File

For testing local changes or unreleased versions.

#### Setup:

**1. Copy your wheel file:**
```bash
# Copy your built wheel to plugins/ directory
cp netbox_scion-1.3-py3-none-any.whl plugins/
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

### Method 3: Alternative with pip (Fallback)

If uv package manager is not available in your NetBox image.

#### Setup:
```dockerfile
# Dockerfile.netbox-pip
FROM netboxcommunity/netbox:latest

USER root
RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

## 🔧 Development and Testing

### Local Development Setup

**1. Clone and setup:**
```bash
git clone https://github.com/aciupac/netbox-scion.git
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

## 📁 Files Included

### Docker Files:
- `Dockerfile-Plugins` - Production deployment with PyPI installation
- `Dockerfile.netbox-local` - Local development with wheel files
- `Dockerfile.netbox-pip` - Alternative using pip instead of uv

### Configuration Files:
- `plugin_requirements.txt` - Plugin dependencies
- `configuration.py.example` - Example NetBox configuration
- `netbox.env.example` - Example environment variables
- `docker-compose.yml` - Example Docker Compose setup

### Plugin Files:
- `plugins/netbox_scion-1.3-py3-none-any.whl` - Current plugin wheel

## 🐛 Troubleshooting

### Plugin Not Loading

**Check installation:**
```bash
# Docker
docker exec netbox pip show netbox-scion

# System
/opt/netbox/venv/bin/pip show netbox-scion
```

**Check configuration:**
```bash
# Verify plugin is in PLUGINS list
docker exec netbox grep -A 10 "PLUGINS" /etc/netbox/configuration.py
```

**Check logs:**
```bash
# Docker logs
docker logs netbox 2>&1 | grep -i scion

# System logs
sudo journalctl -u netbox -f | grep -i scion
```

### Common Issues

**1. Plugin not in sidebar:**
- Clear browser cache (Ctrl+F5)
- Check that `'netbox_scion'` is in PLUGINS list
- Restart NetBox services

**2. Import errors:**
```bash
# Test Python import
docker exec netbox python -c "import netbox_scion; print('OK')"
```

**3. Database migration issues:**
```bash
# Check migrations
docker exec netbox python /opt/netbox/netbox/manage.py showmigrations netbox_scion

# Run migrations manually if needed
docker exec netbox python /opt/netbox/netbox/manage.py migrate
```

**4. Version conflicts:**
- Ensure NetBox v4.0+ compatibility
- Check plugin version matches requirements.txt
- Verify no conflicting plugins

### Navigation Location

The plugin creates a **"SCION"** section in the main sidebar with:
- Organizations
- ISD-ASes
- SCION Link Assignments

Look for it in the main navigation, not under a "Plugins" submenu.

## 🔍 Verification Checklist

✅ **Installation Check:**
```bash
docker exec netbox pip show netbox-scion
```

✅ **Plugin Import:**
```bash
docker exec netbox python -c "import netbox_scion"
```

✅ **Database Migration:**
```bash
docker exec netbox python /opt/netbox/netbox/manage.py showmigrations netbox_scion
```

✅ **Web Interface:**
- Login to NetBox web interface  
- Look for "SCION" in sidebar navigation
- Access: Organizations, ISD-ASes, SCION Link Assignments

✅ **API Access:**
- `/api/plugins/scion/organizations/`
- `/api/plugins/scion/isd-ases/` 
- `/api/plugins/scion/link-assignments/`

## 📞 Support

**For issues:**
- 🐛 [GitHub Issues](https://github.com/aciupac/netbox-scion/issues)
- 💬 [GitHub Discussions](https://github.com/aciupac/netbox-scion/discussions)
- 📖 [Main README](../README.md)

**Legacy Installation Cleanup:**
If upgrading from older versions:
```bash
# Remove old installations
pip uninstall netbox-scion
pip install netbox-scion==1.3.2

# Clear Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

## 📊 Plugin Structure

```
SCION (Top-level menu):
├── Organizations
│   ├── List/Add/Edit/Delete
│   └── Export to CSV/Excel
├── ISD-ASes  
│   ├── List/Add/Edit/Delete
│   ├── Core nodes management
│   └── Organization association
└── SCION Link Assignments
    ├── List/Add/Edit/Delete
    ├── Customer management
    ├── Zendesk ticket integration
    └── Advanced filtering
```

## 🔗 API Examples

Create an organization:
```bash
curl -X POST https://your-netbox/api/plugins/scion/organizations/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"short_name": "ACME", "full_name": "ACME Corporation"}'
```

Create an ISD-AS:
```bash
curl -X POST https://your-netbox/api/plugins/scion/isd-ases/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"isd_as": "1-ff00:0:110", "organization": 1, "cores": ["core1.example.com"]}'
```

## 📝 License

Apache License 2.0

---

**For simple installation instructions, see the main [README.md](../README.md).**
