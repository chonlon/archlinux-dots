
# move node to current desktop and focus
move-node-to-current node:
	bspc node {{node}} -d focused
	bspc node {{node}} -f