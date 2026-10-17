$ErrorActionPreference = "Stop"

python -m pip install --upgrade pyinstaller
python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name TI_Launcher `
    TI_Launcher.py
