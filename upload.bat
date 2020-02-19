@echo off
set /a beg = 371
set /a end = 499
set /a i = %beg%

:forData
if %i% GTR %end% (
  goto over
)
git add %i%*.zip
git commit -m "save: %i%*.zip"

set /a j = 1
:forRetry
echo "%i%*: Try to push...%j%"
git push origin master
if %ERRORLEVEL% == 0 (
    set /a i = %i% + 1
    goto forData
)
set /a j = %j% + 1
goto forRetry

:over
