@echo off

REM 가상환경 폴더 없으면 생성
if not exist ".venv" (
    python -m venv .venv
)

REM 가상환경 활성화
call .venv\Scripts\activate
