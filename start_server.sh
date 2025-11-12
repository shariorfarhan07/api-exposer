#!/bin/bash
# Quick start script for the Product API

echo "Starting Product API Server..."
echo "Access the API at: http://127.0.0.1:8000"
echo "Interactive docs at: http://127.0.0.1:8000/docs"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000

