import hyprlibs
import typer

app = typer.Typer()

cmd = "google-chrome-stable"
title = "Google Chrome"
class_name = "google-chrome"
chrome_workspace = 5
make_master = True


if title == "" and class_name == "":
    print("title and class_name can't be both empty")
    exit(-1)
cur_workspace = hyprlibs.get_current_workspace(0)["id"]
windows = hyprlibs.get_windows()


def find_in_workspace(workspace):
    for win in windows:
        if win["title"] == title or win["class"] == class_name:
            if win["workspace"]["id"] == workspace:
                return win
    return None


def find_in_all():
    for win in windows:
        if win["title"] == title or win["class"] == class_name:
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
        bwin = hyprlibs.biggest_window_in_workspace(win_workspace)
        if win["address"] == bwin["address"]:
            print("already master")
        else:
            hyprlibs.exec_or_remind("hyprctl dispatch layoutmsg swapwithmaster master")
else:
    # create
    import subprocess

    subprocess.run(cmd.split(" "))
    pass
