#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

echo "**************************************************"
echo " Setting up TDD/BDD Final Project Environment"
echo "**************************************************"

echo "*** Installing Python 3.9 and Virtual Environment"
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive 





# activate venv then 
echo "*** Installing Selenium and Chrome for BDD"
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y sqlite3 ca-certificates chromium-driver 
sudo chmod +x /usr/bin/chromedriver

echo "*** Installing Python dependencies..."
if [[ -f "requirements.txt" ]]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

echo "*** Establishing .env file"
if [[ -f "dot-env-example" ]]; then
    cp dot-env-example .env
else
    echo "dot-env-example file not found. Skipping .env setup."
fi

echo "*** Starting the Postgres Docker container..."
if [[ -f "Makefile" ]]; then
    make db
else
    echo "Makefile not found. Skipping database setup."
fi

echo "*** Checking the Postgres Docker container..."
docker ps

echo "**************************************************"
echo " TDD/BDD Final Project Environment Setup Complete"
echo "**************************************************"
echo ""
echo "Use 'exit' to close this terminal and open a new one to initialize the environment"
echo ""
