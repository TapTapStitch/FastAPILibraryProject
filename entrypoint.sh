#!/bin/sh

# Start the FastAPI application using Uvicorn with live reload enabled
uvicorn app.main:app --reload
