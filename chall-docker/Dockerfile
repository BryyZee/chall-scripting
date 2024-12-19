#Utiliser l'image de base Nginx
FROM nginx:alpine

RUN apk add --no-cache shadow

RUN useradd -m docker-ctf && \
    echo "docker-ctf:alejandro" | chpasswd

RUN mkdir -p /var/www/site-chall-docker
RUN echo "N4ninanNan4 naNinaNaNA" | base64 > /lib/security/pam_filter/alejandro.txt

# Copier le fichier de configuration Nginx personnalisé
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY site-chall-docker /var/www/site-chall-docker

# Exposer le port 8080
EXPOSE 8080
# Démarrer Nginx en mode premier plan
CMD ["nginx", "-g", "daemon off;"]
