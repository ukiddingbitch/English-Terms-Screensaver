"""Build a portable Windows screensaver in an isolated virtual environment."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import venv


def main():
    if sys.platform != "win32":
        raise SystemExit("Build the .scr on Windows (or use the GitHub Actions workflow).")
    base = Path(__file__).resolve().parent
    os.chdir(base)
    env = base / ".venv-build"
    if not (env / "Scripts" / "python.exe").exists():
        venv.create(env, with_pip=True)
    python = str(env / "Scripts" / "python.exe")
    subprocess.run([python, "-m", "pip", "install", "-r", "requirements-build.txt"], check=True)
    subprocess.run([python, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
                    "--windowed", "--name", "EnglishTermsScreensaver", "screensaver.py"], check=True)
    shutil.copy2(base / "dist" / "EnglishTermsScreensaver.exe",
                 base / "dist" / "EnglishTermsScreensaver.scr")


if __name__ == "__main__":
    main()
