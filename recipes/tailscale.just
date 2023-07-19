run:
	docker run -d --name=tailscaled -v /var/lib:/var/lib -v /dev/net/tun:/dev/net/tun --network=host --cap-add=NET_ADMIN --cap-add=NET_RAW --privileged tailscale/tailscale

run-it:
	docker run -it --name=tailscaled -v /var/lib:/var/lib -v /dev/net/tun:/dev/net/tun --network=host --cap-add=NET_ADMIN --cap-add=NET_RAW --privileged tailscale/tailscale

start: run up

stop:
	docker rm -f tailscaled

up:
	docker exec tailscaled tailscale up

status:
	docker exec tailscaled tailscale status

web:
	docker exec tailscaled tailscale web