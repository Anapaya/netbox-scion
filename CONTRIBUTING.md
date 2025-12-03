# Contributing to NetBox SCION Plugin

Thank you for your interest in contributing to the NetBox SCION plugin!

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or suggest features
- Provide clear reproduction steps for bugs
- Include your NetBox and Python versions

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/netbox-scion.git`
3. Install in development mode: `pip install -e .`
4. Make your changes
5. Test your changes
6. Submit a pull request

### Building the Package
Recommended modern build (PEP 517):
```bash
python -m pip install --upgrade build
python -m build
```
Artifacts appear under `dist/`:
- `netbox_scion-X.Y.Z-py3-none-any.whl`
- `netbox-scion-X.Y.Z.tar.gz`

Legacy (still supported) invocation:
```bash
python setup.py sdist bdist_wheel
```
If you see `TypeError: canonicalize_version() got an unexpected keyword argument 'strip_trailing_zero'`, upgrade packaging tools:
```bash
python -m pip install --upgrade pip setuptools wheel packaging
```

### Local Testing
For local testing with NetBox, see the [Advanced Deployment Guide](deployment/README.md) which covers:
- Testing with local wheel files
- Custom Docker images for development
- Development environment setup
- Troubleshooting installation issues

### Production Deployment Testing
To test your changes in a production-like environment:
1. Build the package: `python setup.py bdist_wheel`
2. Copy wheel to your netbox-docker deployment
3. Add to `plugin_requirements.txt`
4. Use custom Dockerfile method (see README.md)
5. Test with `docker-compose build && docker-compose up -d`

### Code Style
- Follow Python PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments for complex logic

### Pull Request Process
1. Update documentation if needed
2. Test your changes in a NetBox environment
3. Update CHANGELOG.md
4. Submit pull request with clear description

## Questions?
Feel free to open an issue for any questions about contributing.
