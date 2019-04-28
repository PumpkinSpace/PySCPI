echo off

set filename = nothing

for %%f in (dist\installer\*.exe) DO (
    start "" "%%f"
    goto end
)

:end