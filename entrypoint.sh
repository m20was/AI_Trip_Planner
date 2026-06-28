#!/bin/bash
# Start FastAPI backend in the background and bind to localhost
python -m uvicorn main:app --host 127.0.0.1 --port 8000 &

# Start Streamlit frontend in the foreground
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
