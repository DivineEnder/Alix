@echo off

if "%1"=="-a" goto :listAll
goto :list

:listAll
dir /a
goto end

:list
dir /B
goto end

:end