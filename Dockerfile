FROM ubuntu
WORKDIR seeker/
RUN echo "Asia/Singapore" > /etc/timezone
RUN apt-get update > install.log
RUN apt-get -y install tzdata >> install.log
RUN dpkg-reconfigure -f noninteractive tzdata >> install.log
RUN apt-get -y install python \
python-pip \
apache2 \
php >> install.log
RUN pip install requests >> install.log
ADD . /seeker
RUN cp -r template/nearyou/ /var/www/html/
RUN chmod 777 /var/www/html/nearyou/php/info.txt
RUN chmod 777 /var/www/html/nearyou/php/result.txt
CMD ["./seeker.py"]
