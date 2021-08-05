#!/bin/bash
echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Getting updates"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
apt-get --yes update
apt-get --yes upgrade
echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Update completed"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
echo ""

echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Installing Python 3"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
apt-get --yes install python3 
echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Python 3 installation completed"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
echo ""

echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Installing PIP"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
apt-get --yes install python3-pip
echo "---------------------------------------------"
echo "---------------------------------------------"
echo "PIP installation completed"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
echo ""

echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Installing requirements"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
pip install -r requirements.txt
echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Requirements installation completed"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
echo ""

echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Setting PythonPath environment variable"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
export PythonPath=$(pwd)
echo "---------------------------------------------"
echo "---------------------------------------------"
echo "PythonPath environmental variable set: "$(pwd)
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
echo ""

echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Installing Docker"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
apt --yes install docker.io
sudo snap install docker
groupadd docker
usermod -aG docker ${USER}
echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Docker installation completed"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
echo ""


echo "---------------------------------------------"
echo "---------------------------------------------"
echo "Installing IBeam Docker Image"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
docker pull voyz/ibeam
echo "---------------------------------------------"
echo "---------------------------------------------"
echo "IBeam Docker Image installation comepleted"
echo "---------------------------------------------"
echo "---------------------------------------------"
echo ""
echo ""
