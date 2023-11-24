"""
bring cur win to last workspace
"""
import hyprlibs

cur = hyprlibs.get_current_window()
hyprlibs.exec_or_remind("hyprctl dispatch workspace previous")
cur_ws = hyprlibs.get_current_workspace()

hyprlibs.exec_or_remind(f'hyprctl dispatch movetoworkspace {cur_ws["name"]},address:{ cur["address"] }')