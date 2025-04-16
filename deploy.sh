#!/bin/bash
# ¡Excelente! Aquí tienes un script automatizado paso a paso para desplegar 
# tu sitio Django con Docker, Nginx y certificados SSL en un servidor
# (como DigitalOcean). Este script asume que ya clonaste el repo y estás
# en la carpeta del proyecto.

DOMAIN="hijosfelices.com.mx"
EMAIL="msoto.stop@gmail.com"  # Cambia esto por tu correo real
NGINX_CONF_PATH="./nginx/nginx.conf"

echo "🚀 Iniciando despliegue para $DOMAIN..."

# Paso 1: Instalar Certbot si no está
if ! command -v certbot &> /dev/null; then
    echo "🔧 Instalando Certbot..."
    sudo apt update
    sudo apt install certbot python3-certbot-nginx -y
fi

# Paso 2: Verificar si los certificados ya existen
if [ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "🔐 Generando certificados SSL para $DOMAIN..."
    sudo certbot certonly --nginx -d $DOMAIN --agree-tos --non-interactive --email $EMAIL
else
    echo "✅ Certificados ya existen, omitiendo generación."
fi

# Paso 3: Verificar archivo nginx.conf
if [ ! -f "$NGINX_CONF_PATH" ]; then
    echo "⚠️ Archivo nginx.conf no encontrado en $NGINX_CONF_PATH"
    exit 1
fi

# Paso 4: Construir e iniciar contenedores
echo "🐳 Construyendo e iniciando contenedores..."
docker compose up --build -d

# Paso 5: Recargar configuración de Nginx en el contenedor
echo "🔁 Reiniciando Nginx dentro del contenedor..."
docker exec metodo.proxy nginx -s reload || echo "⚠️ No se pudo recargar Nginx (¿contenedor levantado?)"

# Paso 6: Agregar cronjob de renovación si no existe
CRONJOB="0 3 1 * * certbot renew --quiet && docker restart metodo.proxy"
(crontab -l 2>/dev/null | grep -F "$CRONJOB") || (
    echo "🕒 Agregando tarea cron para renovación automática de certificados..."
    (crontab -l 2>/dev/null; echo "$CRONJOB") | crontab -
)

echo "✅ Despliegue completado. Visita: https://$DOMAIN"
