clear
echo '[!] Updating...'
apt-get update > install.log
echo
echo '[!] Installing Dependencies...'
echo '    Python'
apt-get -y install python &>> install.log
echo '    Apache2'
apt-get -y install apache2 &>> install.log
echo '    PHP'
apt-get -y install php-apache &>> install.log
echo '    wget'
apt-get -y install wget &>> install.log
echo '    unzip'
apt-get -y install unzip &>> install.log
echo '    Requests'
pip install requests &>> install.log
echo
echo '[!] Copying Template to /data/data/com.termux/files/usr/share/apache2/default-site/htdocs/'
cp -r ../template/nearyou/ $PREFIX/share/apache2/default-site/htdocs/
echo
echo '[!] Adding PHP 7 Support in /etc/apache2/httpd.conf'
echo 'LoadModule php7_module /data/data/com.termux/files/usr/libexec/apache2/libphp7.so' >> $PREFIX/etc/apache2/httpd.conf
echo '<FilesMatch \.php$>' >> $PREFIX/etc/apache2/httpd.conf
echo 'SetHandler application/x-httpd-php' >> $PREFIX/etc/apache2/httpd.conf
echo '</FilesMatch>' >> $PREFIX/etc/apache2/httpd.conf
echo
echo '[!] Creating seeker symlink...'
ln -s $PWD/seeker.py $PREFIX/bin/seeker
chmod 777 $PREFIX/bin/seeker
echo
echo '[!] Setting Permissions...'
chmod 777 $PREFIX/share/apache2/default-site/htdocs/nearyou/php/result.txt
chmod 777 $PREFIX/share/apache2/default-site/htdocs/nearyou/php/info.txt
echo
echo '[!] Installed...Launch by Typing seeker'
