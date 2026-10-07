uv python list
uv python cpython-3.10.20-windows-x86_64-none
uv python install cpython-3.10.20-windows-x86_64-none
uv python list
uv venv env --python cpython-3.10.20-windows-x86_64-none
C:\Users\ranjini.chaudhary\AI_Trip_Planner\env\Scripts\activate.bat
uv pip list
cls
uv pip install langchain
uv pip list
doskey/history
uv add pandas

# To run front-end

streamlit run streamlit_app.py

# To run backend

uvicorn main:app --reload --port 8000