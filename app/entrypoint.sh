#!/bin/bash
nohup streamlit run /app_py/webapp/main.py &
python3 -m uvicorn app_py.main:app --host 0.0.0.0 --port 15400
