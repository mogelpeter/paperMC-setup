# Funktion zur Überprüfung von Administratorrechten
function Test-IsAdmin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Wenn das Skript nicht mit Administratorrechten ausgeführt wird, neu starten mit erhöhten Rechten
if (-not (Test-IsAdmin)) {
    Write-Host "Administratorrechte sind erforderlich. Neustart mit erhöhten Rechten..."
    Start-Process powershell "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Überprüfen, ob Python 3 installiert ist
try {
    $python_version = python --version 2>&1
} catch {
    $python_version = $null
}

if ($python_version -match "Python 3") {
    Write-Host "Python 3 ist bereits installiert. Version: $python_version"
} else {
    Write-Host "Python 3 ist nicht installiert. Herunterladen und installieren von Python 3..."
    $python_installer = "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe"
    $python_installer_path = "$env:TEMP\python_installer.exe"
    Invoke-WebRequest -Uri $python_installer -OutFile $python_installer_path
    Start-Process -FilePath $python_installer_path -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item -Path $python_installer_path
}

# Überprüfen, ob Amazon Corretto 21 installiert ist
$java_path = "C:\Program Files\Amazon Corretto\jdk21.0.4_7\bin\java.exe"
if (Test-Path $java_path) {
    Write-Host "Amazon Corretto 21 ist bereits installiert."
} else {
    Write-Host "Amazon Corretto 21 ist nicht installiert. Herunterladen und installieren von Amazon Corretto 21..."
    $corretto_installer = "https://corretto.aws/downloads/latest/amazon-corretto-21-x64-windows-jdk.msi"
    $corretto_installer_path = "$env:TEMP\corretto_installer.msi"
    Invoke-WebRequest -Uri $corretto_installer -OutFile $corretto_installer_path
    Start-Process msiexec.exe -ArgumentList "/i", $corretto_installer_path, "/quiet" -Wait
    Remove-Item -Path $corretto_installer_path
}

Write-Host "Installation von Python 3 und Amazon Corretto 21 abgeschlossen."

# Installationen überprüfen
Write-Host "Überprüfung der Python-Installation..."
python --version

Write-Host "Überprüfung der Amazon Corretto-Installation..."
& $java_path -version
