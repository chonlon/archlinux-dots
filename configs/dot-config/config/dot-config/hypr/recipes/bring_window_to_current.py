import os
import subprocess
import hyprlibs

# dir="$HOME/.config/rofi/launchers/"
home = os.path.expanduser('~/.config/rofi/launchers/')
theme='style-5'

## Run
"""
echo -e "a\nb\nc" | rofi \
    -dmenu \
    -theme ${dir}/${theme}.rasi
"""

def get_win_name(win):
    return f'{win["class"]}: {win["title"]}'.lower()

cur_workspace = hyprlibs.get_current_workspace(0)["id"]
windows = hyprlibs.get_windows()


windows_excur_names = []

for win in windows:
    if win["workspace"]["id"] != cur_workspace:
        # if win title or class is empty, skip it
        if not win["title"] or not win["class"]:
            continue
        name = get_win_name(win)
        windows_excur_names.append(name)
        
        
rofi_choices = '\n'.join(windows_excur_names)
rofi_cmd = f'echo "{rofi_choices}" | rofi -dmenu -theme {home}{theme}.rasi'

rofi_out = subprocess.check_output(rofi_cmd, shell=True).decode('utf-8').strip()

for win in windows:
    # match window name
    name = get_win_name(win)
    # 就算有两个窗口名字计算一样，只取第一个。
    if win["workspace"]["id"] != cur_workspace and name == rofi_out:
        # move window to current workspace
        hyprlibs.exec_or_remind(f'hyprctl dispatch movetoworkspacesilent {cur_workspace},address:{win["address"]}')
        # refocus to first window in current workspace
        hyprlibs.exec_or_remind("hyprctl dispatch focuswindow address:{}".format(win["address"]))
        break