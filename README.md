<pre>
                      __                 
  ______ ____   ____ |  | __ ___________
 /  ___// __ \_/ __ \|  |/ // __ \_  __ \
 \___ \\  ___/\  ___/|    <\  ___/|  | \/
/____  >\___  >\___  >__|_ \\___  >__|   
     \/     \/     \/     \/    \/       
</pre>

## Introduction
Seeker utilizes **HTML5, Javascript, JQuery and PHP** to grab **Device Information** and **GeoLocation** with High Accuracy.

It Generates a fake website which asks for Location Permission and if the user allows it, we can get :

* Longitude
* Latitude
* Accuracy
* Altitude
* Direction
* Speed

Along with Location Information we can also get **Device Information** without any permissions :

* Operating System
* Platform
* Number of CPU Cores
* Amount of RAM
* Screen Resolution
* GPU information
* Browser Name and Version
* Public IP Address

## Tested On :

* Kali Linux 2018.2
* Ubuntu 18.04

## Requirements

Supports both Python2 and Python3

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
