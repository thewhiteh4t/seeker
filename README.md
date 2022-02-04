<p align="center"><img src="https://i.imgur.com/DIpuNTI.jpg"></p>

<p align="center">
    <a href="https://twitter.com/thewhiteh4t">
      <img src="https://img.shields.io/badge/-TWITTER-black?logo=twitter&style=for-the-badge">
    </a>
    &nbsp;
    <a href="https://twc1rcle.com/">
      <img src="https://img.shields.io/badge/-THE WHITE CIRCLE-black?logo=&style=for-the-badge">
    </a>
    &nbsp;
    <a href="https://thewhiteh4t.github.io/">
      <img src="https://img.shields.io/badge/-BLOG-black?logo=dialogflow&style=for-the-badge">
    </a>
</p>

<p align="center">
  <br>
  <b>Available in</b>
  <br>
  <img src="https://i.imgur.com/1wJVDV5.png">
</p>

<p>
  <a style="margin-right: 10px;" href="https://github.com/thewhiteh4t/seeker#installation">
    <img src="https://dabuttonfactory.com/button.png?t=INSTALL&f=Open+Sans&ts=15&tc=000&hp=25&vp=10&c=5&bgt=unicolored&bgc=00e2ff">
  </a>
  <a style="margin-right: 10px;" href="https://github.com/thewhiteh4t/seeker#usage">
    <img src="https://dabuttonfactory.com/button.png?t=USAGE&f=Open+Sans&ts=15&tc=000&hp=25&vp=10&c=5&bgt=unicolored&bgc=00e2ff">
  </a>
  <a href="https://github.com/thewhiteh4t/seeker#demo">
    <img src="https://dabuttonfactory.com/button.png?t=DEMO&f=Open+Sans&ts=15&tc=000&hp=25&vp=10&c=5&bgt=unicolored&bgc=00e2ff">
  </a>
</p>

Concept behind Seeker is simple, just like we host phishing pages to get credentials why not host a fake page that requests your location like many popular location based websites. Read more on <a href="https://thewhiteh4t.github.io"> thewhiteh4t's Blog </a>.Seeker Hosts a fake website which asks for Location Permission and if the target allows it, we can get :

* Longitude
* Latitude
* Accuracy
* Altitude - Not always available
* Direction - Only available if user is moving
* Speed - Only available if user is moving

Along with Location Information we also get **Device Information** without any permissions :

* Unique ID using Canvas Fingerprinting
* Device Model - Not always available
* Operating System
* Platform
* Number of CPU Cores - Approximate Results
* Amount of RAM - Approximate Results
* Screen Resolution
* GPU information
* Browser Name and Version
* Public IP Address
* Local IP Address
* Local Port

**Automatic IP Address Reconnaissance** is performed after the above information is received.

**This tool is a Proof of Concept and is for Educational Purposes Only, Seeker shows what data a malicious website can gather about you and your devices and why you should not click on random links and allow critical permissions such as Location etc.**

## How is this Different from IP GeoLocation

* Other tools and services offer IP Geolocation which is NOT accurate at all and does not give location of the target instead it is the approximate location of the ISP.

* Seeker uses HTML API and gets Location Permission and then grabs Longitude and Latitude using GPS Hardware which is present in the device, so Seeker works best with Smartphones, if the GPS Hardware is not present, such as on a Laptop, Seeker fallbacks to IP Geolocation or it will look for Cached Coordinates.  

* Generally if a user accepts location permsission, Accuracy of the information recieved is **accurate to approximately 30 meters**

* Accuracy depends on multiple factors which you may or may not control such as :
  * Device - Won't work on laptops or phones which have broken GPS
  * Browser - Some browsers block javascripts
  * GPS Calibration - If GPS is not calibrated you may get inaccurate results and this is very common

## Templates

Available Templates : 

* NearYou
* Google Drive (Suggested by @Akaal_no_one)
* WhatsApp (Suggested by @Dazmed707)
* Telegram
* Zoom (Made by @a7maadf)

## Tested On :

* Kali Linux
* BlackArch Linux
* Ubuntu
* Kali Nethunter
* Termux
* Parrot OS
* OSX - Monterey v.12.0.1

## Installation

### Kali Linux / Arch Linux / Ubuntu / Parrot OS / Termux

```bash
git clone https://github.com/thewhiteh4t/seeker.git
cd seeker/
chmod +x install.sh
./install.sh
```

### BlackArch Linux

```bash
sudo pacman -S seeker
```

### Docker

```bash
docker pull thewhiteh4t/seeker
```

### OSX
```bash
git clone https://github.com/thewhiteh4t/seeker.py
cd seeker/
python3 seeker.py
````

In order to run in tunnel mode, install ngrok by running this command in the terminal:
```bash
brew install ngrok/ngrok/ngrok

ngrok http 8080
````

## Usage

```bash
python3 seeker.py -h

usage: seeker.py [-h] [-k KML] [-p PORT] [-u] [-v]

options:
  -h, --help            show this help message and exit
  -k KML, --kml KML     KML filename
  -p PORT, --port PORT  Web server port [ Default : 8080 ]
  -u, --update          Check for updates
  -v, --version         Prints version

##################
# Usage Examples #
##################

# Step 1 : In first terminal
$ python3 seeker.py

# Step 2 : In second terminal start a tunnel service such as ngrok
$ ./ngrok http 8080

###########
# Options #
###########

# Ouput KML File for Google Earth
$ python3 seeker.py -k <filename>

# Use Custom Port
$ python3 seeker.py -p 1337
$ ./ngrok http 1337

################
# Docker Usage #
################

# Step 1
$ docker network create ngroknet

# Step 2
$ docker run --rm -it --net ngroknet --name seeker thewhiteh4t/seeker

# Step 3
$ docker run --rm -it --net ngroknet --name ngrok wernight/ngrok ngrok http seeker:8080
```

## Local Tunnels
Use
```
ssh -R 80:localhost:8080 nokey@localhost.run
```
as an alterntive to ngrok

## Demo

**YouTube**

<a href="https://youtu.be/Q91cTFwIvLc">
  <img src="https://i3.ytimg.com/vi/Q91cTFwIvLc/maxresdefault.jpg">
</a>