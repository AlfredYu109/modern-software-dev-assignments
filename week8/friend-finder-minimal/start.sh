#!/bin/bash

echo "Friend Finder Lite - Starting Application"
echo "=========================================="
echo ""

if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install Flask flask-cors
    echo ""
fi

echo "Starting Flask server..."
echo "Open your browser to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
