#!/bin/bash

# Ensure the script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

# Update and upgrade the system
echo "Updating and upgrading the system..."
sudo apt-get update && sudo apt-get upgrade -y

# Install required tools
echo "Installing required tools..."
sudo apt-get install -y ca-certificates apt-transport-https gnupg wget

# Import the Amazon Corretto public key and add the apt repository
echo "Importing Amazon Corretto public key and adding the apt repository..."
wget -O - https://apt.corretto.aws/corretto.key | sudo gpg --dearmor -o /usr/share/keyrings/corretto-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/corretto-keyring.gpg] https://apt.corretto.aws stable main" | sudo tee /etc/apt/sources.list.d/corretto.list

# Update the package list
echo "Updating the package list..."
sudo apt-get update

# Install Java 21 and other dependencies
echo "Installing Java 21 and other dependencies..."
sudo apt-get install -y java-21-amazon-corretto-jdk libxi6 libxtst6 libxrender1

# Verify the installation
echo "Verifying the Java installation..."
java --version

echo "Installation complete."
