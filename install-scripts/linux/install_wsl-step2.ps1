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

# Run Ubuntu for the first time to complete the installation
Write-Host "Running Ubuntu for the first time to complete the installation..."
wsl -d Ubuntu-22.04

# Update Ubuntu packages and install necessary tools
Write-Host "Updating Ubuntu packages and installing necessary tools..."
wsl -d Ubuntu-22.04 -- bash -c "
sudo apt-get update &&
sudo apt-get upgrade -y &&
sudo apt-get install -y ca-certificates apt-transport-https gnupg wget &&
wget -O - https://apt.corretto.aws/corretto.key | sudo gpg --dearmor -o /usr/share/keyrings/corretto-keyring.gpg &&
echo 'deb [signed-by=/usr/share/keyrings/corretto-keyring.gpg] https://apt.corretto.aws stable main' | sudo tee /etc/apt/sources.list.d/corretto.list &&
sudo apt-get update &&
sudo apt-get install -y java-21-amazon-corretto-jdk libxi6 libxtst6 libxrender1
"

# Print a message indicating the installation is complete
Write-Host "WSL 2.0 with Ubuntu 22.04 installation and setup complete. Please run 'linux_start.py' to start the Minecraft server."
