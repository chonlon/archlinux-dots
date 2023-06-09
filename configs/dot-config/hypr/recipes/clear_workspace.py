import hyprlibs


cur_win = hyprlibs.get_current_window()["address"]
cur_workspace = hyprlibs.get_current_workspace(0)["id"]
windows = hyprlibs.get_windows()

config = hyprlibs.get_config()
target_rules = config["window"]["target_rules"]


for win in windows:
    if win["workspace"]["id"] == cur_workspace and win["address"] != cur_win:
        # if win title or class is empty, skip it
        if not win["title"] or not win["class"]:
            continue
        target_workspace = 9
        for rule in target_rules:
            if hyprlibs.is_window_match(win, rule):
                target_workspace = rule["workspace"]
                break
        
        print("closing: {}-{}".format(win["address"], win["title"]))
        hyprlibs.exec_or_remind("hyprctl dispatch movetoworkspacesilent {},address:{}".format(target_workspace , win["address"]))
        hyprlibs.exec_or_remind("hyprctl dispatch cyclenext")


