server {
        listen 80;
        listen [::]:80;

        root /var/www/html/wordpress/;
        index index.php;

        server_name dongjianjun.com www.dongjianjun.com;
	return 301 https://www.dongjianjun.com$request_uri;
}

server {
    listen 443 ssl http2;
    server_name www.dongjianjun.com;

    root /var/www/html/wordpress/;
    index index.php;

    # SSL parameters
    ssl_certificate /etc/letsencrypt/live/dongjianjun.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dongjianjun.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/dongjianjun.com/chain.pem;

    location = /favicon.ico {
        log_not_found off;
        access_log off;
    }

    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php7.2-fpm.sock;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires max;
        log_not_found off;
    }
}
