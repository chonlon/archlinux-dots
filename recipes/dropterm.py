# this script is used to toggle a floating terminal in bspwm
# the terminal is named "dropdown-kitty"
# it will be hidden when it is not focused or this script is run again

import argparse
import os

# import subprocess
import time


width = 2550
height = 1440
left = 0
top = 0

# drop down kitty in bspwm
name = "dropdown-kitty"
zellij_command = "zellij -l compact attach -c --index 0"
kitty_command = f"kitty --name {name} -o font_size=20 -o 'background_opacity 0.75' -e {zellij_command}"


def hideNode(id: str):
    """
    hide the dropterm
    """
    os.system(f"bspc node {id} -g hidden=on")


def showNode(id: str):
    #  reset node size
    os.system(f"bspc node {id} -z {width} {height} {left} {top}")
    # show
    os.system(f"bspc node {id} -g hidden=off")


def queryDropTerm():
    """
    query by name if the dropterm is running
    return none if not running
    """
    id = os.popen(f"xdo id -n {name}").read().strip()
    return id


def nodeIsCopyq(id: str):
    """
    check if id is copyq
    """
    class_name = os.popen(f"xprop -id {id} | grep WM_CLASS").read().strip()
    return "copyq" in class_name or "CopyQ" in class_name


def watchDropTerm(id: str):
    """
    watch the dropterm, when it is not foucsed, hide it, and exit script
    """
    watchCmd = "bspc subscribe node_focus"
    process = os.popen(watchCmd)
    while True:
        output = process.readline()
        newly_focused = output.split()[-1]
        if (
            not id == newly_focused
            and not nodeIsTiled(id)
            and not nodeIsCopyq(newly_focused)
        ):
            hideNode(id)
            break


def runDropTerm():
    """
    run the dropterm
    """
    # set rule
    rule = f"bspc rule -a kitty:{name} state=floating sticky=true center=true rectangle={width}x{height}+{left}+{top}"
    os.system(rule)
    out = os.popen(kitty_command).read()
    print("kitty:", out)


def nodeIsHidden(id: str):
    """
    check if the dropterm is hidden
    """
    bspc_query = f"bspc query -N -n {id}.hidden"
    return os.popen(bspc_query).read().strip() == id


def nodeIsTiled(id: str):
    """
    check if the dropterm is tiled
    """
    bspc_query = f"bspc query -N -n {id}.tiled"
    return os.popen(bspc_query).read().strip() == id


def focusNode(id: str):
    os.system(f"bspc node {id} -f")


dropTermId = queryDropTerm()
if dropTermId:
    print("dropTermId: ", dropTermId)
    if nodeIsHidden(dropTermId):
        showNode(dropTermId)
        focusNode(dropTermId)
        watchDropTerm(dropTermId)
    else:
        hideNode(dropTermId)
else:
    runDropTerm()
    time.sleep(1)
    startupId = None
    while not startupId:
        startupId = queryDropTerm()
    print("startupId: ", startupId)
    watchDropTerm(startupId)
