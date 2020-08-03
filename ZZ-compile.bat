venv\scripts\activate & ^
pip3 install -r requirements.txt & ^
pyinstaller ^
--noconsole ^
--noconfirm ^
--onefile ^
--icon=icon.ico ^
client.py