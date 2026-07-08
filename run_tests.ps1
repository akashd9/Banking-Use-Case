$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$env:JAVA_HOME = "$env:USERPROFILE\.local\jdk17\jdk-17.0.19+10"
$env:Path = "$env:JAVA_HOME\bin;$env:Path"
$env:PYSPARK_PYTHON = (Resolve-Path ".venv\Scripts\python.exe").Path
$env:PYSPARK_DRIVER_PYTHON = $env:PYSPARK_PYTHON

& ".venv\Scripts\python.exe" -m pytest tests/ -v
