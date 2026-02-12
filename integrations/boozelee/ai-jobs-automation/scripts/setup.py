# AI Jobs Automation - Setup Script

import os
import sys
from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ai-jobs-automation',
    version='0.1.0',
    description='Legal and ethical automation for AI job applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Bakery Street Project',
    author_email='support@bakery-street-project.com',
    url='https://github.com/yourusername/ai-jobs-automation',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Office/Business',
        'Topic :: Utilities',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ai-jobs-automation=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt', '*.json'],
    },
    keywords='ai jobs automation productivity career',
    project_urls={
        'Source': 'https://github.com/yourusername/ai-jobs-automation',
        'Tracker': 'https://github.com/yourusername/ai-jobs-automation/issues',
        'Documentation': 'https://github.com/yourusername/ai-jobs-automation/wiki',
    },
)

# WATERMARK: PRIMAX-AI-BSP-2025
© 2025 Bakery Street Project