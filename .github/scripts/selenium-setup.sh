#!/bin/sh

# Install the official Firefox Beta PPA
sudo apt-add-repository ppa:mozillateam/firefox-next

# Run apt-get update
sudo apt-get update

# Install firefox and xvfb (the X windows virtual framebuffer) packages
sudo apt-get install firefox xvfb

# Run Xvfb in the background and specify a display number
Xvfb :10 -ac &

# Set the DISPLAY variable to the number you chose
export DISPLAY=:10

# Get the latest version of geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz

# Unzip the geckodriver download and make it executable
tar -xzf geckodriver-v0.27.0-linux64.tar.gz
chmod +x geckodriver