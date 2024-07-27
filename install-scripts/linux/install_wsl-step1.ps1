# Function to check for administrator rights
function Test-IsAdmin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# If not running as administrator, restart the script with elevated privileges
if (-not (Test-IsAdmin)) {
    Write-Host "Administrator permissions are required. Restarting with elevated privileges..."
    Start-Process powershell "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Install WSL 2 and set Ubuntu 22.04 as default
Write-Host "Installing WSL 2.0 and setting Ubuntu 22.04 as the default distribution..."
wsl --install -d Ubuntu-22.04

# Set WSL 2 as the default version
Write-Host "Setting WSL 2 as the default version..."
wsl --set-default-version 2

# Prompt the user to restart the computer
Write-Host "Installation of WSL 2.0 with Ubuntu 22.04 is complete. Please restart your computer and run 'continue_wsl_install.ps1' to continue the installation process."
