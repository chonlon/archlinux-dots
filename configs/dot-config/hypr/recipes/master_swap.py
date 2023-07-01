# swap cur with master


import hyprlibs



cur = hyprlibs.get_current_window()
cur_workspace = hyprlibs.get_current_workspace(0)["id"]
master = hyprlibs.master_window_in_workspace(cur_workspace)


# # rt_win = master_window_in_workspace(cur_workspace)
if cur["address"] != master["address"]:
  for i in range(10):
    hyprlibs.exec_or_remind("hyprctl dispatch movewindow u")
hyprlibs.exec_or_remind("hyprctl dispatch layoutmsg swapwithmaster master")