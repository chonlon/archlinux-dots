import hyprlibs


cur_win = hyprlibs.get_current_window()["address"]
cur_workspace = hyprlibs.get_current_workspace(0)["id"]
windows = hyprlibs.get_windows()


for win in windows:
    if win["workspace"]["id"] == cur_workspace and win["address"] != cur_win:
        # if win title or class is empty, skip it
        if not win["title"] or not win["class"]:
            continue
        
        print("closing: {}-{}".format(win["address"], win["title"]))
        hyprlibs.exec_or_remind("hyprctl dispatch movetoworkspacesilent {},address:{}".format(9 , win["address"]))
        hyprlibs.exec_or_remind("hyprctl dispatch cyclenext")


