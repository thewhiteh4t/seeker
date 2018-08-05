echo '[!] Updating...'
apt-get update > install.log
echo
echo '[!] Installing Dependencies...'
echo '    Python'
apt-get -y install python &>> install.log
echo '    Apache2'
apt-get -y install apache2 &>> install.log
echo '    PHP'
apt-get -y install php &>> install.log
echo '    wget'
apt-get -y install wget &>> install.log
echo '    unzip'
apt-get -y install unzip &>> install.log
echo '    Requests'
pip install requests &>> install.log
echo
echo '[!] Copying Template to /var/www/html/'
rm -rf /var/www/html/nearyou/
cp -r template/nearyou/ /var/www/html/
echo
echo '[!] Creating seeker symlink...'
echo
ln -s $PWD/seeker.py /usr/local/bin/seeker
chmod 777 /usr/local/bin/seeker
echo
echo '[!] Setting Permissions...'
chmod 777 /var/www/html/nearyou/php/info.txt
chmod 777 /var/www/html/nearyou/php/result.txt
echo
echo '[!] Installed...Launch by Typing seeker'
