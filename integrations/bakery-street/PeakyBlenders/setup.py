#!/usr/bin/env python3
"""
PEAKY BLENDERS - Setup Script
Advanced AI Framework for Systemic Risk Analysis
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="peaky-blenders",
    version="1.0.0",
    author="PEAKY BLENDERS Team",
    author_email="info@peaky-blenders.org",
    description="Advanced AI Framework for Systemic Risk Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Booze-Lee/peaky-blenders",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Security",
    ],
    keywords="ai machine-learning systemic-risk financial-analysis regulatory-compliance",
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "docs": ["sphinx", "sphinx-rtd-theme"],
        "test": ["pytest", "pytest-cov"],
    },
    entry_points={
        "console_scripts": [
            "peaky-blenders=run_engine:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/Booze-Lee/peaky-blenders/issues",
        "Source": "https://github.com/Booze-Lee/peaky-blenders",
        "Documentation": "https://Booze-Lee.github.io/peaky-blenders/",
    },
)
