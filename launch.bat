
IF NOT EXIST venv (
    python -m venv venv
)
powershell -Command "& {Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; .\venv\Scripts\activate; pip install -r requirements.txt}"
powershell -Command "& {.\venv\Scripts\activate; python src/main.py}"
pause