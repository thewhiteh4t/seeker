echo '[!] Updating...'
apt-get update > install.log
echo
echo '[!] Installing Dependencies...'
echo '    Python'
apt-get -y install python &>> install.log
echo '    PHP'
apt-get -y install php &>> install.log
echo '    wget'
apt-get -y install wget &>> install.log
echo '    unzip'
apt-get -y install unzip &>> install.log
echo '    Requests'
pip install requests &>> install.log
echo
echo '[!] Downloading Ngrok...'
rm -rf ngrok*
rm -rf Ngrok/
arch=$(uname -m)
if [ $arch == "x86_64" ]; then
  wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
  unzip ngrok-stable-linux-amd64.zip
  mkdir Ngrok
  mv ngrok Ngrok/
  rm ngrok-stable-linux-amd64.zip
elif [ $arch == "x64" ]; then
  wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
  unzip ngrok-stable-linux-amd64.zip
  mkdir Ngrok
  mv ngrok Ngrok/
  rm ngrok-stable-linux-amd64.zip
elif [ $arch == "i386" ]; then
  wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip
  unzip ngrok-stable-linux-386.zip
  mkdir Ngrok
  mv ngrok Ngrok/
  rm ngrok-stable-linux-386.zip
else
  echo Error : Unable to get Architecture!
fi
echo
echo '[!] Setting Permissions...'
chmod 777 template/nearyou/php/info.txt
chmod 777 template/nearyou/php/result.txt
echo
echo '[!] Installed.'
