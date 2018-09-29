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
echo '[!] Creating seeker symlink...'
ln -s $PWD/seeker.py $PREFIX/bin/seeker
chmod 777 $PREFIX/bin/seeker
echo
echo '[!] Setting Permissions...'
chmod 777 ../template/nearyou/php/result.txt
chmod 777 ../template/nearyou/php/info.txt
echo
echo '[!] Installed...Launch by Typing seeker'
