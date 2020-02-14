for %%i in (20,1,30) do (
    git add %%i*
    git commit -m "save"
    git push origin master
)
