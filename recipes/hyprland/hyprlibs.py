# clear current workspace but keep current node

import json
import subprocess

__G_config = None


def exec_or_remind(command):
    try:
        out = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return out.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error: {}".format(e.stdout))

        with open("/tmp/hypr-cus.log", "a") as f:
            f.write("\n----\n{}:\n{}".format(command, e.stdout.decode("utf-8")))

            # dunst notification
            notify("error log in /tmp/hypr-cus.log")

        raise e


def get_current_window():
    out = exec_or_remind("hyprctl activewindow -j")
    return json.loads(out)


def get_current_workspace():
    out = exec_or_remind("hyprctl activeworkspace -j")
    active_workspace = json.loads(out)
    return active_workspace


def get_current_workspace_lastwindow():
    "return last window in current workspace(address)"
    active_workspace = get_current_workspace()
    lastwindow = active_workspace["lastwindow"]
    return lastwindow


def get_windows_cur_workspace():
    windows = get_windows()
    rst = []
    cur_workspace = get_current_workspace()
    for win in windows:
        if win["workspace"]["id"] == cur_workspace["id"]:
            rst.append(win)
    return rst


def get_workspaces():
    out = exec_or_remind("hyprctl workspaces -j")
    workspaces = json.loads(out)
    return workspaces


def get_windows():
    out = exec_or_remind("hyprctl clients -j")
    windows = json.loads(out)
    return windows


def biggest_window_in_workspace(workspace_id):
    windows = get_windows()
    biggest_win = None
    biggest_area = 0
    for win in windows:
        if win["workspace"]["id"] == workspace_id:
            # if win title or class is empty, skip it
            if not win["title"] or not win["class"]:
                continue
            area = win["size"][0] * win["size"][1]
            if area > biggest_area:
                biggest_area = area
                biggest_win = win
    return biggest_win or windows[0]


def master_window_in_workspace(workspace_id):
    windows = get_windows()
    master = None
    for win in windows:
        if win["workspace"]["id"] == workspace_id:
            # if win title or class is empty, skip it
            if not win["title"] or not win["class"]:
                continue
            x, y = win["at"]
            print(x, y)
            if x < 100 and y < 200:
                master = win
                break
    if not master:
        print("no master window found")
    return master


def focused_monitor():
    out = exec_or_remind("hyprctl monitors -j")
    monitors = json.loads(out)
    for mon in monitors:
        if mon["focused"]:
            return mon
    return None


def get_config():
    print("loading config")

    def get_config_from():
        import os

        home = os.path.expanduser("~")
        config_path = os.path.join(home, ".recipes", "hyprland", "config")
        with open(config_path) as f:
            config = json.load(f)
        return config

    config = get_config_from()
    return config


def is_window_match(win, rule):
    """
    rule: {"title": "xxx", "class": "xxx", ...}
    win: hyprctl clients -j returned or get_windows() returned
    """
    import string

    if "title" in rule and rule["title"] and win["title"].find(rule["title"]) == -1:
        return False
    if "class" in rule and rule["class"] and win["class"] != rule["class"]:
        return False
    return True


def notify(msg):
    exec_or_remind("notify-send -t 3000 '{}'".format(msg))


def import_util():
    import inspect
    import os
    import sys

    currentdir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)


def choose_in_dmenu(
    options: list | str, placeholder="", cmd="tofi", auto_accept_single=True
):
    import_util()
    import utils

    return utils.choose_in_dmenu(options, placeholder, cmd, auto_accept_single)
