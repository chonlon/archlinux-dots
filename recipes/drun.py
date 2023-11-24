import typer
import utils
import os

def open_in_broswer(url):
  import webbrowser
  webbrowser.open(url, autoraise=True)

def poweroff():
  if utils.confirm_in_dmenu():
    utils.run_or_exit("poweroff")

def reboot():
  if utils.confirm_in_dmenu():
    utils.run_or_exit("reboot")

def rerun_copyq():
  cmd = f"just -f ~/.recipes/autostart/justfile copyq"
  utils.run_or_exit(cmd)

def rerun_waybar():
  cmd = f"just -f ~/.recipes/autostart/justfile waybar"
  utils.run_or_exit(cmd)

def run_vscode():
  code = "code"
  dir = utils.select_zoxide_path(50)
  if dir and len(dir)> 0:
    cmd = f"{code} {dir}"
    utils.run_or_exit(cmd)

def code_mvd():
  dic = {
    "hypr": "~/.config/hypr",
    "recipe": "~/.recipes",
    "smt": "~/3_lon/Small-Test-Projects"
  }
  code = "code"
  dir = utils.select_zoxide_path(15)
  if dir and len(dir)> 0:
    cmd = f"{code} {dir}"
    utils.run_or_exit(cmd)

def hypr_prop():
  cmd = "sh ~/.config/hypr/recipes/contrib/hyprprop/hyprprop"
  out = utils.run_command(cmd)
  utils.to_clipboard(out)

def hypr_wiki():
  url = "https://wiki.hyprland.org"
  open_in_broswer(url)

def hypr_release():
  url = "https://github.com/hyprwm/Hyprland/releases"
  open_in_broswer(url)  

def lock():
  cmd = "swaylock -i $HOME/.config/hypr/wallpapers/632051.png"
  utils.run_or_exit(cmd)

def logout():
  cmd = "hyprctl dispatch exit"
  utils.run_or_exit(cmd)
  
cmds = {
  "pf": poweroff,
  "cc": code_mvd, # run code in most value 
  "reboot": reboot,
  "copyq": rerun_copyq, # rerun copyq
  "waybar": rerun_waybar, # rerun waybar
  "code": run_vscode, # create a vscode
  "lock": lock,
  "logout": logout,
  "hypr prop": hypr_prop, # get hyprprop
  "hypr wiki": hypr_wiki,
  "hypr release": hypr_release,
  # make broswers wayland or x11
}

choosen = utils.choose_in_dmenu(cmds.keys())
if choosen and len(choosen):
  func = cmds.get(choosen)
  if func:
    func()