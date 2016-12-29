@ECHO OFF

for /f "delims=" %%x in (%ALIX_HOME%.env) do (set "%%x")

%PY3_EXEC_PATH% %ALIX_PATH%/alix.py %*