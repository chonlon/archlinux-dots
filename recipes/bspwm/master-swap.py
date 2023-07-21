# this script works with bspwm

# swap current node with biggest node in current desktop
# if current node is biggest node, swap with prev focused node

# focus biggest node after swap

import os

current_node = os.popen("bspc query -N -n focused").read().strip()
desktop = os.popen("bspc query -D -d focused").read().strip()
biggest_node = os.popen("bspc query -N -n biggest.tiled.local").read().strip()

if current_node == biggest_node:
    prev_node = os.popen("bspc query -N -n last.tiled.local").read().strip()
    os.system("bspc node " + current_node + " -s " + prev_node)
    os.system("bspc node " + prev_node + " -f")
else:
    os.system("bspc node " + current_node + " -s " + biggest_node)
    os.system("bspc node " + biggest_node + " -f")
    os.system("bspc node " + current_node + " -f")
    