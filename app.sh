#!/bin/bash
# Start Flask backend on port 8080
python3 app.py &

# Wait a second to make sure backend starts
sleep 2

# Start Streamlit on port 7860 (Hugging Face expects this)
streamlit run dashb.py --server.port 7860 --server.address 0.0.0.0
