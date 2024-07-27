# Prebuild paperMC 1.20.6 Minecraft server


# Windows Installation Guide

1. Open `Powershell.exe` and run:
    ```sh
    .\windows-setup.ps1
    ```
2. Restart your PC.
3. Open `cmd.exe`.
4. Navigate to the server folder (make sure it is on the Desktop):
    ```sh
    cd "C:\Users\XXX\Desktop\paperMC"
    ```
5. Run the Python script:
    ```sh
    python windows.py
    ```
    If the regular Python command does not work, try:
    ```sh
    python3 windows.py
    ```

---

*Note: In step 4, ensure that the folder with the server is indeed on the Desktop.*


# Linux Installation Guide + How to install Ubuntu on Windows 

## Install Windows Linux Subsystem + Ubuntu 22.04 on your Windows PC:

1. Open `Powershell.exe` and enter:
    ```sh
    .\install_wsl-step1.ps1
    ```
2. You will likely need to restart your PC after step 1. Continue with the file from step 3.
3. Open `Powershell.exe` and enter:
    ```sh
    .\install_wsl-step2.ps1
    ```

---

## Install everything needed for the Ubuntu installation:

1. Make the install script executable:
    ```sh
    chmod +x install.sh
    ```
2. Run the install script:
    ```sh
    ./install.sh
    ```
3. Run the Python script:
    ```sh
    python3 linux.py
    ```

---
