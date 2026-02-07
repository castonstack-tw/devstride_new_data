#!/bin/bash
# Run the Streamlit dashboard

export PATH=$PATH:/sessions/eager-gallant-maxwell/.local/bin

echo "Starting DevStride Analytics Dashboard..."
echo "The dashboard will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run streamlit_dashboard.py
