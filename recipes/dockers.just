
# init alist by default
alist-start:
    docker run -d --restart=always \
        -v /etc/alist:/opt/alist/data \
        -v $HOME/6_data:/mnt \
        -p 5244:5244 -e PUID=0 -e PGID=0 -e UMASK=022 \
        --name="alist" xhofe/alist:latest

alist-password:
    docker exec -it alist ./alist admin

alist-stop:
    docker rm alist -f

frp-start:
    docker run --restart=always \
        --network host  -itd \
        -v $HOME/5_app/frp/frpc.ini:/etc/frp/frpc.ini \
        --name frpc snowdreamtech/frpc

frp-stop:
    docker rm frpc -f
