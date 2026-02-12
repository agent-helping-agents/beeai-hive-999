# AI Development Framework

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/BoozeLee/ai-development-framework)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-green?style=for-the-badge)](https://github.com/BoozeLee/ai-development-framework/actions)

A comprehensive AI development and orchestration framework with multiple specialized environments and tools.

**Repository**: https://github.com/BoozeLee/ai-development-framework

## 🚀 Features

- **Multi-Environment Setup**: Separate environments for AI, neuromorphic computing, and research
- **AI Orchestration**: Advanced AI orchestrator with crew management
- **Database Integration**: DuckDB and AWS Athena clients
- **Deployment Ready**: Docker and production deployment scripts
- **Development Tools**: Cursor IDE integration and development utilities

## 📁 Project Structure

```
ai-development/
├── config/                 # Configuration files
├── tools/                  # Utility tools and scripts
├── environments/           # Virtual environments (gitignored)
├── *.py                    # Python source files
├── *.sh                    # Shell scripts
├── *.md                    # Documentation
└── docker-compose.yml      # Docker configuration
```

## 🛠️ Quick Start

### 1. Activate Environments
```bash
# AI Main Environment
./activate-ai.sh

# Neuromorphic Computing Environment
./activate-neuro.sh

# Research Environment
./activate-research.sh
```

### 2. Run AI Orchestrator
```bash
python advanced_ai_orchestrator.py
```

### 3. Test Database Connections
```bash
python test_duckdb.py
python test_athena.py
```

## 🔧 Installation

### Prerequisites
- Python 3.11+
- Docker (for containerized deployment)
- AWS CLI (for Athena integration)

### Setup
```bash
# Install dependencies
./setup_complete.sh

# Configure API keys
python setup_api_keys.py

# Setup databases
./setup_databases.sh
```

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or use the deployment script
./deploy_production.py
```

## 📊 Database Integration

### DuckDB
- Local analytics database
- Fast columnar storage
- SQL interface

### AWS Athena
- Serverless query service
- S3 integration
- Cost-effective analytics

## 🔒 Security

- API key management via `setup_api_keys.py`
- Production-ready security configurations
- Audit logging capabilities

## 📈 Monitoring

- Production reports generation
- Performance monitoring
- Error tracking and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in the `*.md` files
- Review the usage guides
- Examine the test files for examples

## 🔄 Version History

- **v1.0.0**: Initial release with AI orchestration framework
- Multi-environment support
- Database integration
- Production deployment capabilities
