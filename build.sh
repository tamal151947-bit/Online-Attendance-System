#!/bin/bash
# Render build script - optimized for memory efficiency

set -e  # Exit on error

echo "📦 Installing Python packages with pre-built wheels..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "✅ Build completed successfully!"
