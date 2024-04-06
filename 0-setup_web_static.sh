#!/usr/bin/env bash
#sets up web servers for the deployment of web_static

if ! which nginx > /dev/null 2>/dev/null; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

content=\
"
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
"

echo "$content" > /data/web_static/releases/test/index.html

ln -sfn /data/web_static/releases/test/ /data/web_static/current

if id -u ubuntu &>/dev/null; then
	sudo chown -R ubuntu:ubuntu /data/
fi

config_content=\
"
server {
	listen 80;
	listen [::]:80;
	server_name _;

	location /hbnb_static/ {
		alias /data/web_static/current/;
		index index.html htm;
	}
}
"

echo "$config_content" > /etc/nginx/sites-available/default

service nginx restart

exit 0
