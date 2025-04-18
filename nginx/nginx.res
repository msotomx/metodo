upstream appsite {
    server web:3762;
}

server {

    listen 80;

    client_max_body_size 14M;

    location / {
        proxy_pass http://appsite;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /static/ {
        alias /usr/src/app/staticfiles/;
    }

    location /media/ {
        alias /usr/src/app/media/;
    }

}