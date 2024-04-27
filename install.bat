@echo off

REM Check if conda is installed
conda --version >nul 2>nul
if %errorlevel% equ 0 (
    REM Create a new conda environment with Python 3.10 in a directory named env within your project's directory
    call conda create --prefix ./env python=3.10 -y

    REM Activate the new environment
    call conda activate ./env

    REM Install the requirements using conda
    call conda install pytorch==2.0.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia

    REM Install the requirements using pip
    pip install git+https://github.com/m-bain/whisperx.git
) else (
    echo "Conda is not installed. Please install Conda and try again."
    echo "You can download Conda from https://docs.conda.io/en/latest/miniconda.html"
)

REM Pause the script before closing the terminal window
pause