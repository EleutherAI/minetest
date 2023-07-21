#!/bin/bash

# Get the operating system name
OS=$(lsb_release -si)

# Check if the OS is Ubuntu
if [ "$OS" == "Ubuntu" ]; then
    # If it's Ubuntu, execute the command
    echo "You are running Ubuntu. Executing command..."
    sudo apt-get install xvfb g++ make libzmq3-dev libtool pkg-config build-essential autoconf automake libc6-dev cmake libpng-dev libjpeg-dev libxi-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-gnutls-dev libfreetype6-dev zlib1g-dev libgmp-dev libjsoncpp-dev libzstd-dev libluajit-5.1-dev protobuf-compiler patchelf
else
    # If it's not Ubuntu, print a message and exit
    echo "This script only works on Ubuntu. Exiting."
    exit 1
fi
