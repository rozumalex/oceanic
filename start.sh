#!/bin/bash
# Use this script to start the application with hot reload.

uvicorn server:app --port 8000 --reload --log-level info
