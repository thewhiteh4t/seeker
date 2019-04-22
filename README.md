<p align="center"><img src="https://i.imgur.com/iLLX7A8.png"></p>
<h4 align="center">
Get Accurate Location using a Fake Website
</h4>

<p align="center">
<img src="https://img.shields.io/badge/Python-3-brightgreen.svg?style=plastic">
<img src="https://img.shields.io/badge/Python-2-brightgreen.svg?style=plastic">
<img src="https://img.shields.io/badge/Docker-✔-blue.svg?style=plastic">
<img src="https://img.shields.io/badge/Termux-✔-red.svg?style=plastic">
<img src="https://img.shields.io/badge/NetHunter-✔-red.svg?style=plastic">
</p>

Concept behind Seeker is simple, just like we host phishing pages to get credentials why not host a fake page that requests your loction just like many popular location based websites.

Seeker Hosts a fake website on **In Built PHP Server** and uses **Ngrok**, website asks for Location Permission and if the user allows it, we can get :

* Longitude
* Latitude
* Accuracy
* Altitude - Not always available
* Direction - Only available if user is moving
* Speed - Only available if user is moving

Along with Location Information we also get **Device Information** without any permissions :

* Operating System
* Platform
* Number of CPU Cores
* Amount of RAM - Approximate Results
* Screen Resolution
* GPU information
* Browser Name and Version
* Public IP Address

**This tool is a Proof of Concept and is for Educational Purposes Only, Seeker shows what data a malicious website can gather about you and your devices and why you should not click on random links and allow critical permissions such as Location etc.**

* Other tools and services offer IP Geolocation which is not very accurate and does not give location of user.

* Generally if a user accepts location permsission, Accuracy of the information recieved is **accurate to approximately 30 meters**.

**Note** : On iPhone due to some reason location accuracy is approximately 65 meters.

## Tested On :

* Kali Linux 2018.2
* Ubuntu 18.04
* Arch Linux based Distro
* Termux
* Kali Linux (WSL)
* Parrot OS
* Zorin OS

## Installation

### Ubuntu/Kali Linux

```bash
git clone https://github.com/thewhiteh4t/seeker.git
cd seeker/
chmod 777 install.sh
./install.sh

# OR using Docker

# Install docker

curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Build Seeker
cd seeker/
docker build -t seeker .

# Launch seeker
docker run -t --rm seeker

# OR Pull from DockerHub
docker pull thewhiteh4t/seeker
docker run -t seeker
```

### Arch Linux Based Distro

```bash
# Install docker

pacman -Syy
pacman -S docker
systemctl start docker.service

# Build Seeker
cd seeker/
docker build -t seeker .

# Launch seeker
docker run -t --rm seeker
```
### Termux

```bash
cd seeker/termux
chmod 777 install.sh
./install.sh
```

> If you are unable to get ngrok url that means ngrok is unable to resolve dns, switch to Mobile Data instead of WiFi and it should work, this is a problem with ngrok.

## Demo

Youtube - https://www.youtube.com/watch?v=ggUGPq4cjSM
