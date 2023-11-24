"""
create vscode if no vscode
choose one if multi vscode
"""
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import hyprlibs
import utils

cmd = "code"
title = "Visual Studio Code"
class_name = "Code"

def run(cmd,title,class_name):
    make_master = True

    if title == "" and class_name == "":
        print("title and class_name can't be both empty")
        exit(-1)
    cur_workspace = hyprlibs.get_current_workspace()["id"]
    windows = hyprlibs.get_windows()

    def find_in_all():
        wins = []
        for win in windows:
            if win["title"].find(title) > 0 or win["class"] == class_name:
                wins.append(win)
        return wins


    def find_vscode():
        wins = (
            find_in_all()
        )
        return wins

    wins = find_vscode()

    if wins and len(wins) > 0:
        if len(wins) == 1:
          win = wins[0]
        else:
          wins_t = [win["title"].removesuffix(" - Visual Studio Code") for win in wins]
          win_t = utils.choose_in_dmenu(wins_t, "choose vscode")
          if not win_t or len(win_t) == 0:
            exit(0)
          for _win in wins:
            if win_t in _win["title"]:
              win = _win
        # focus
        print("focusing: {}-{}".format(win["address"], win["title"]))
        win_addr = win["address"]
        hyprlibs.exec_or_remind("hyprctl dispatch focuswindow address:{}".format(win_addr))

        if make_master:
            win_workspace = win["workspace"]["id"]
            bwin = hyprlibs.biggest_window_in_workspace(win_workspace)
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
      
run(cmd, title, class_name)