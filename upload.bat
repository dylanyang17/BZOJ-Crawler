for /l %%i in (30,1,39) do (
    git add %%i*
    git commit -m "save: %%i*"
    git push origin master
)
