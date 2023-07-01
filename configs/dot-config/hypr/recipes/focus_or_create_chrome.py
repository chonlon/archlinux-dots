import hyprlibs
import typer

app = typer.Typer()

cmd = "google-chrome-stable"
title = "google chrome"
class_name = "google-chrome"
chrome_workspace = 5
make_master = True


if title == "" and class_name == "":
    print("title and class_name can't be both empty")
    exit(-1)
cur_workspace = hyprlibs.get_current_workspace()["id"]
windows = hyprlibs.get_windows()


def find_in_workspace(workspace):
    for win in windows:
        if win["title"].lower() == title or win["class"].lower() == class_name:
            if win["workspace"]["id"] == workspace:
                return win
    return None


def find_in_all():
    for win in windows:
        if win["title"].lower() == title or win["class"].lower() == class_name:
            return win
    return None


def find_chrome():
    win = (
        find_in_workspace(cur_workspace)
        or find_in_workspace(chrome_workspace)
        or find_in_all()
    )
    return win


win = find_chrome()

if win is not None:
    # focus
    print("focusing: {}-{}".format(win["address"], win["title"]))
    win_addr = win["address"]
    hyprlibs.exec_or_remind("hyprctl dispatch focuswindow address:{}".format(win_addr))

    if make_master:
        win_workspace = win["workspace"]["id"]
        bwin = hyprlibs.master_window_in_workspace(win_workspace)
        if win["address"] == bwin["address"]:
            print("already master")
            if win["workspace"]["id"] == cur_workspace:
                print("swapping with master")
                hyprlibs.exec_or_remind("hyprctl dispatch workspace prev")
        else:
            hyprlibs.exec_or_remind("hyprctl dispatch layoutmsg swapwithmaster master")
else:
    # create
    import subprocess

    subprocess.run(cmd.split(" "))
    pass
