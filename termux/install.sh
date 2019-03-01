clear
echo '[!] Updating...'
apt-get update > install.log
echo
echo '[!] Installing Dependencies...'
echo '    Python'
apt-get -y install python &>> install.log
echo '    PHP'
apt-get -y install php-apache &>> install.log
echo '    wget'
apt-get -y install wget &>> install.log
echo '    unzip'
apt-get -y install unzip &>> install.log
echo '    Requests'
pip install requests &>> install.log
echo
echo '[!] Downloading Ngrok...'
case `dpkg --print-architecture` in
aarch64 | arm64)
  wget https://bin.equinox.io/a/nmkK3DkqZEB/ngrok-2.2.8-linux-arm64.zip;
  unzip ngrok-2.2.8-linux-arm64.zip;
  mv ngrok $PREFIX/bin;
  rm ngrok-2.2.8-linux-arm64.zip ;;
armhf | armv7l | arm)
  wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip;
  unzip ngrok-stable-linux-arm.zip;
  mv ngrok $PREFIX/bin;
  rm ngrok-stable-linux-arm.zip ;;
*)
  echo Error : Unable to get Architecture! ;;
esac
echo
echo '[!] Setting Permissions...'
chmod 777 ../template/nearyou/php/result.txt
chmod 777 ../template/nearyou/php/info.txt
chmod +x $PREFIX/bin/ngrok
echo
echo '[!] Installed.'
