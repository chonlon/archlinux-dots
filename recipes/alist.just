
# init alist by default
init:
    docker run -d --restart=always \
        -v /etc/alist:/opt/alist/data \
        -v $HOME/6_data:/mnt \
        -p 5244:5244 -e PUID=0 -e PGID=0 -e UMASK=022 \
        --name="alist" xhofe/alist:latest

password:
    docker exec -it alist ./alist admin

clean-alist-container:
    docker rm alist -f
