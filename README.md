# NetBox SCION Plugin

A comprehensive NetBox plugin for managing SCION (Scalability, Control, and Isolation On Next-generation networks) infrastructure.

[![PyPI](https://img.shields.io/pypi/v/netbox-scion)](https://pypi.org/project/netbox-scion/)
[![Python Version](https://img.shields.io/pypi/pyversions/netbox-scion)](https://pypi.org/project/netbox-scion/)
[![License](https://img.shields.io/github/license/anapaya/netbox-scion)](https://github.com/anapaya/netbox-scion/blob/main/LICENSE)

## ✨ Features

- **Organizations:** Manage SCION operators with metadata and descriptions
- **ISD-ASes:** Track Isolation Domain and Autonomous System identifiers with appliances (CORE/EDGE)
- **Link Assignments:** Interface management with customer information and Zendesk integration
- **REST API:** Full CRUD operations with filtering and pagination
- **Export:** CSV and Excel export capabilities
- **Advanced Filtering:** Search, dropdown filters, and tag-based filtering on all list pages

## 📦 Installation

```bash
pip install netbox-scion==1.3.3
```

## 🚀 Quick Start

### Prerequisites
- NetBox v4.0+ (Docker or system installation)
- Python 3.8+

### Basic Installation

Choose the method that matches your NetBox deployment:

#### Docker Installation (Recommended)

For [netbox-docker](https://github.com/netbox-community/netbox-docker) deployments:

```bash
# 1. Add plugin to plugin_requirements.txt
echo "netbox-scion==1.3.3" >> plugin_requirements.txt

# 2. Add to configuration/plugins.py
PLUGINS = ['netbox_scion']

# 3. Rebuild containers
docker-compose build
docker-compose up -d
```

#### System Installation

For native NetBox installations:

```bash
# 1. Install in NetBox virtual environment
source /opt/netbox/venv/bin/activate
pip install netbox-scion==1.3.3

# 2. Add to configuration.py
PLUGINS = ['netbox_scion']

# 3. Run migrations and restart
cd /opt/netbox/netbox
python manage.py migrate
sudo systemctl restart netbox netbox-rq
```

### Verification

Check the plugin is installed:
```bash
pip show netbox-scion  # or: docker exec netbox pip show netbox-scion
```

Then access NetBox and look for the "SCION" section in the sidebar.

### Advanced Installation

For detailed setup, custom Docker builds, local development, or troubleshooting, see the [**Advanced Deployment Guide**](deployment/README.md)

## 🔧 API Access

The plugin provides a full REST API with CRUD operations, filtering, and pagination:

- **Organizations:** `/api/plugins/scion/organizations/`
- **ISD-ASes:** `/api/plugins/scion/isd-ases/`
- **Link Assignments:** `/api/plugins/scion/link-assignments/`

**📖 Complete API Documentation:** See [**API.md**](API.md) for comprehensive documentation including:
- Authentication methods
- Request/response examples
- Filtering and search
- Error handling
- Python code examples

## 🎯 Navigation

The plugin adds a "SCION" section to the NetBox sidebar with:
- Organizations
- ISD-ASes  
- SCION Link Assignments

## 📁 Development

### For Plugin Users
**You don't need to clone this repository!** Simply install via pip using the instructions above.

### For Contributors & Developers

Only clone this repository if you want to:
- Contribute code changes
- Customize the plugin
- Use local development builds
- Test unreleased features

```bash
# Clone and setup for development
git clone https://github.com/anapaya/netbox-scion.git
cd netbox-scion

# Install in development mode
pip install -e .

# For advanced deployment scenarios
cp -r deployment/* /path/to/your/netbox-docker/
```

See [**deployment/README.md**](deployment/README.md) for advanced installation methods including custom Docker images and local wheel files.

### Project Structure
```
netbox_scion/
├── __init__.py              # Plugin configuration
├── models.py                # Data models
├── forms.py                 # Web forms
├── views.py                 # Web views
├── urls.py                  # URL routing
├── api/                     # REST API
├── templates/               # HTML templates
├── migrations/              # Database migrations
└── static/                  # CSS/JS assets
```

### Local Development
```bash
# Install in development mode
pip install -e .

# Run migrations
python manage.py migrate

# Create wheel package
python setup.py bdist_wheel
```

## 🐛 Troubleshooting

### Quick Fixes

**Plugin not appearing?**
- Check installation: `pip show netbox-scion` (or `docker exec netbox pip show netbox-scion`)
- Ensure `'netbox_scion'` is in your `PLUGINS` list
- Restart NetBox services

**For detailed troubleshooting, deployment issues, and advanced configuration, see our [**Advanced Deployment Guide**](deployment/README.md).**

### Getting Help
- 🐛 **Bug reports:** [GitHub Issues](https://github.com/anapaya/netbox-scion/issues)
- 💬 **Questions:** [GitHub Discussions](https://github.com/anapaya/netbox-scion/discussions)
- 📚 **Detailed docs:** [deployment/README.md](deployment/README.md)

## 📝 License

Apache License 2.0
>>>>>>> 5a4fa61 (netbox_plugin: initial PR in Anapaya REPO)
