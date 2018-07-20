# Seeker

## Introduction
Seeker utilizes **HTML5, Javascript, JQuery and PHP** to grab **Device Information** and **GeoLocation** with High Accuracy.

**This tool is purely a Proof of Concept and is for Educational Purposes Only, Seeker shows what data a malicious website can gather about you and your devices and why you should not click on random links and allow critical permissions such as Location etc.**

* Other tools and services offer IP Geolocation which is not very accurate and does not give location of user.

* Generally if a user accepts location permsission, Accuracy of the information recieved is **accurate to approximately 30 meters**.

**Note** : On iPhone due to some reason location accuracy is approximately 65 meters.

It Hosts a fake website on **Apache Server** and uses **Ngrok** to generate a SSL link which asks for Location Permission and if the user allows it, we can get :

* Longitude
* Latitude
* Accuracy
* Altitude - Not always available
* Direction - Only available if user is moving
* Speed - Only available if user is moving

Along with Location Information we can also get **Device Information** without any permissions :

* Operating System
* Platform
* Number of CPU Cores
* Amount of RAM - Approximate Results
* Screen Resolution
* GPU information
* Browser Name and Version
* Public IP Address

## Tested On :

* Kali Linux 2018.2
* Ubuntu 18.04

## Requirements

Supports both **Python2** and **Python3**.

Seeker uses common standard python modules :

* os
* time
* json
* requests
* subprocess

## Installation

```bash
git clone https://github.com/thewhiteh4t/seeker.git
cd seeker/
chmod 777 install.sh
./install.sh

#After Installation just type seeker in console
```

## PoC

Youtube - https://www.youtube.com/watch?v=ggUGPq4cjSM

## Screenshots
![example](https://raw.githubusercontent.com/thewhiteh4t/seeker/master/screenshots/seeker1.png) ![example](https://raw.githubusercontent.com/thewhiteh4t/seeker/master/screenshots/seeker2.png)
