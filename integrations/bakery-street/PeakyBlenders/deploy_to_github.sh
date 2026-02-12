#!/bin/bash

# PEAKY BLENDERS - GitHub Deployment Script
# Run this script to deploy your project to GitHub

echo "🚀 PEAKY BLENDERS - GitHub Deployment Script"
echo "By order of the Peaky Blenders"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
fi

# Add all files
echo "📦 Adding files to Git..."
git add .

# Commit changes
echo "💾 Creating initial commit..."
git commit -m "🎉 Initial release: PEAKY BLENDERS v1.0.0

Advanced AI Framework for Systemic Risk Analysis

Features:
✅ SNN/GNN Hybrid Architecture
✅ Predictive Anomaly Detection
✅ Explainable AI
✅ RESTful API
✅ Security & Audit Modules
✅ Docker Support
✅ CI/CD Pipeline

By order of the Peaky Blenders 🚀"

echo ""
echo "🎯 Next Steps:"
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: peaky-blenders"
echo "   - Description: Advanced AI Framework for Systemic Risk Analysis"
echo "   - Make it Public"
echo "   - Don't initialize with README, .gitignore, or license"
echo ""
echo "2. Add your GitHub remote:"
echo "   git remote add origin https://github.com/Booze-Lee/peaky-blenders.git"
echo ""
echo "3. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "4. Update badge URLs in README.md:"
echo "   - Replace 'your-username' with your actual GitHub username"
echo ""
echo "5. Create a release:"
echo "   - Go to GitHub repository"
echo "   - Click 'Releases' → 'Create a new release'"
echo "   - Tag: v1.0.0"
echo "   - Title: PEAKY BLENDERS v1.0.0 - Initial Release"
echo "   - Copy CHANGELOG.md content"
echo ""
echo "🎉 Your PEAKY BLENDERS framework is ready for deployment!"
echo "=========================================="
