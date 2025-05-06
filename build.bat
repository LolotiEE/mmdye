@echo off
call pyinstaller main.py --onefile --noconsole --icon=icon.ico --upx-dir E:\ProgramFiles\upx-5.0.1-win64 --exclude-module tkinter --exclude-module test --name=dye