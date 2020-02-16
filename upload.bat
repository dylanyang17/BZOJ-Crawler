for /l %%i in (35,1,39) do (
    git add %%i*
    git commit -m "save: %%i*"
    git push origin master
)
