#!/bin/bash
# Render build script for face-recognition dependencies

set -e  # Exit on error

echo "🔧 Installing system dependencies..."

# Install system packages needed for dlib and face-recognition
apt-get update
apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev

echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build completed successfully!"
