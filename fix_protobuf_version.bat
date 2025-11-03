@echo off
echo Fixing protobuf version compatibility...
python -m pip install --upgrade "protobuf>=3.11.0,<3.21"
echo.
echo Protobuf version fixed! You can now run:
echo   python yliveticker/client_code.py
pause

