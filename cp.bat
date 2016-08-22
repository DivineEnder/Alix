@ECHO OFF
(parseDest.py %1 %2 %cd%) > Output
(
  Set /p src=
  Set /p dest=
) < Output
ECHO %src%
ECHO %dest%
xcopy "%src%" "%dest%" /O /X /E /H /K
DEL Output
