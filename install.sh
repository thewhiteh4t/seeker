echo '[!] Updating...'
sudo apt-get update > install.log
echo
echo '[!] Installing Dependencies...'
echo '    Python3'
sudo apt-get -y install python3 python3-pip &>> install.log
echo '    PHP'
sudo apt-get -y install php &>> install.log
echo '    ssh'
sudo apt-get -y install ssh &>> install.log
echo '    Requests'
sudo pip3 install requests &>> install.log
echo
echo '[!] Setting Permissions...'
chmod 777 template/nearyou/php/info.txt
chmod 777 template/nearyou/php/result.txt
echo
echo '[!] Installed.'
