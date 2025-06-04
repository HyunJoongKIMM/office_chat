@echo off
chcp 65001 > nul
cd /d C:\Users\Evolvesoft\Desktop\chat\office_chat
:loop
echo 서버를 시작합니다.
py -3 server.py
echo 서버가 종료됐습니다. 5초 후에 재시작합니다...
timeout /t 5
goto loop
