# TrustedInstaller Launcher

A Windows desktop launcher for starting CMD, PowerShell, Task Manager, or
another executable with TrustedInstaller privileges.

The app is written in Python with Tkinter and uses
[gsudo](https://github.com/gerardog/gsudo) for privilege elevation.

## Features

- Open a TrustedInstaller CMD window
- Open a TrustedInstaller PowerShell window
- Start Task Manager with TrustedInstaller privileges
- Run an arbitrary command with TrustedInstaller privileges
- Run a selected executable with TrustedInstaller privileges
- Clean up leftover gsudo services and scheduled tasks
- Display the current privilege level

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- [gsudo](https://github.com/gerardog/gsudo) available on `PATH`

TrustedInstaller operations require administrator access and can trigger a
Windows UAC prompt.

## Run from source

```powershell
python -m pip install -r requirements.txt
python TI_Launcher.py
```

## Build a standalone executable

```powershell
.\build.ps1
```

The executable is written to `dist\TI_Launcher.exe`.

## Download

The prebuilt executable is published as a GitHub Release asset. Verify its
SHA-256 checksum before running it:

```text
3A796A03F089683244991F487FB3B5CE2AC9DA6F9828DC0AE4FE2D8535451960
```

Windows SmartScreen may warn about an unsigned executable. You can run the
source directly if you prefer to inspect it first.

## Security notice

This tool intentionally runs commands with very high Windows privileges.
Only run commands and executables that you trust. Review commands before
executing them, and do not use this tool to bypass security boundaries on
systems you do not own or administer.

## License

MIT License. See [LICENSE](LICENSE).
