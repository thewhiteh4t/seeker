FROM alpine:latest
RUN apk update 
RUN apk add --no-cache \
git \
python3 \
py3-pip gcc \
python3-dev \
php openssh
WORKDIR /root
RUN git clone https://github.com/thewhiteh4t/seeker.git
WORKDIR /root/seeker/
ENTRYPOINT ["/bin/sh"]