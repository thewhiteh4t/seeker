FROM alpine:latest
RUN apk update 
RUN apk add --no-cache \
git \
bash \
musl-dev \
linux-headers \
python3 \
py3-pip gcc \
python3-dev \
php php-json openssh
RUN pip3 install --break-system-packages requests packaging psutil
WORKDIR /root/seeker
COPY . .
EXPOSE 8080
ENTRYPOINT ["/root/seeker/seeker.py"]
