# clear current workspace but keep current node

import json
import subprocess


def exec_or_remind(command):
    try:
        out = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return out.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print("Error: {}".format(e.stdout))

        with open("/tmp/hypr-cus.log", "a") as f:
            f.write("\n----\n{}".format(e.stdout.decode("utf-8")))

        # dunst notification
        subprocess.call(
            "dunstify -r 1234 -u critical -t 5000 -a 'Hypr' 'Error' 'error log in /tmp/hypr-cus.log'",
            shell=True,
        )

        raise e


def get_current_window():
    out = exec_or_remind("hyprctl activewindow -j")
    return json.loads(out)


def get_current_workspace(monitor_n: int):
    out = exec_or_remind("hyprctl monitors -j")
    monitors = json.loads(out)
    active_workspace = monitors[monitor_n]["activeWorkspace"]
    return active_workspace


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
    return biggest_win